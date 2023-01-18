"""
Module providing testcases for the app endpoints.
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_utils.database import Base
from utils import create_db_folder
from app import app, get_db
import generate_test_db


DATABASE_URL = "sqlite:///./test.db"
TEST_DB_URL = os.path.join(os.getcwd(), "test.db")
DB_TEST_ENTRIES = [
    ('luximmo', 'https://luximmo.bg/23', 246483,
     'Двустаен', 84, 'Люлин 3', 'some_image', 'SOME_DATE'),
    ('bezkomisiona', 'https://bezkomisiona.bg/61', 170294,
     'Мезонет', 185, 'Слатина', 'some_image', 'SOME_DATE'),
    ('superimoti', 'https://superimoti.bg/64', 210395,
     'Двустаен', 195, 'Горубляне', 'some_image', 'SOME_DATE'),
    ('addressbg', 'https://addressbg.bg/66', 57644,
     'Едностаен', 142, 'Младост 4', 'some_image', 'SOME_DATE'),
    ('avista', 'https://avista.bg/96', 216479, 'Двустаен',
     125, 'Младост 2', 'some_image', 'SOME_DATE'),
    ('superimoti', 'https://superimoti.bg/66', 61497,
     'Студио', 193, 'Илинден', 'some_image', 'SOME_DATE'),
    ('bezkomisiona', 'https://bezkomisiona.bg/30', 98228,
     'Тристаен', 99, 'Овча купел 2', 'some_image', 'SOME_DATE'),
    ('bezkomisiona', 'https://bezkomisiona.bg/57', 289343,
     'Студио', 68, 'Люлин', 'some_image', 'SOME_DATE'),
    ('era', 'https://era.bg/69', 131733, 'Мезонет',
     163, 'Света троица', 'some_image', 'SOME_DATE'),
    ('ues', 'https://ues.bg/80', 177669, 'Мезонет',
     192, 'Обеля 2', 'some_image', 'SOME_DATE'),
    ('arcoreal', 'https://arcoreal.bg/25', 234161,
     'Двустаен', 81, 'Връбница 2', 'some_image', 'SOME_DATE'),
    ('mirelabg', 'https://mirelabg.bg/76', 232870,
     'Мезонет', 155, 'Левски', 'some_image', 'SOME_DATE'),
    ('ues', 'https://ues.bg/35', 296825, 'Многостаен',
     88, 'Люлин 9', 'some_image', 'SOME_DATE'),
    ('addressbg', 'https://addressbg.bg/61', 126041,
     'Мезонет', 94, 'Център', 'some_image', 'SOME_DATE'),
    ('bezkomisiona', 'https://bezkomisiona.bg/46', 280778,
     'Многостаен', 193, 'Младост 1A', 'some_image', 'SOME_DATE'),
    ('yavlena', 'https://yavlena.bg/97', 282492,
     'Студио', 56, 'Славия', 'some_image', 'SOME_DATE'),
    ('avista', 'https://avista.bg/14', 293794, 'Едностаен',
     75, 'Република 2', 'some_image', 'SOME_DATE'),
    ('superimoti', 'https://superimoti.bg/77', 98964, 'Многостаен',
     123, 'Димитър Миленков', 'some_image', 'SOME_DATE'),
    ('home2u', 'https://home2u.bg/64', 173626, 'Тристаен',
     61, 'Хиподрума', 'some_image', 'SOME_DATE'),
    ('era', 'https://era.bg/30', 242059, 'Едностаен',
     127, 'Стрелбище', 'some_image', 'SOME_DATE'),
    ('galardo', 'https://galardo.bg/49', 215036, 'Едностаен',
     172, 'Дружба 2', 'some_image', 'SOME_DATE'),
    ('yourhome', 'https://yourhome.bg/83', 295392, 'Многостаен',
     97, 'Овча купел 1', 'some_image', 'SOME_DATE'),
    ('bulgarianproperties', 'https://bulgarianproperties.bg/10',
     193864, 'Мезонет', 123, 'Света троица', 'some_image', 'SOME_DATE'),
    ('bezkomisiona', 'https://bezkomisiona.bg/29', 237987,
     'Многостаен', 72, 'Люлин 6', 'some_image', 'SOME_DATE'),
    ('yavlena', 'https://yavlena.bg/11', 299179, 'Мезонет',
     120, 'Дървеница', 'some_image', 'SOME_DATE'),
    ('luximmo', 'https://luximmo.bg/45', 192682, 'Едностаен',
     166, 'Банишора', 'some_image', 'SOME_DATE'),
    ('home2u', 'https://home2u.bg/83', 268885, 'Двустаен',
     199, 'Градина', 'some_image', 'SOME_DATE'),
    ('home2u', 'https://home2u.bg/20', 240912, 'Мезонет',
     156, 'Експериментален', 'some_image', 'SOME_DATE'),
    ('imotbg', 'https://imotbg.bg/87', 98807, 'Едностаен',
     106, 'Белите Брези', 'some_image', 'SOME_DATE'),
    ('novdom1', 'https://novdom1.bg/74', 255456, 'Мезонет',
     111, 'Зона Б-5-3', 'some_image', 'SOME_DATE'),
]

engine = create_engine(DATABASE_URL,
                       connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

create_db_folder()
Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    Overrides the original database with the test one
    """
    try:
        database = TestingSessionLocal()
        yield database
    finally:
        database.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def populate_test_db():
    """
    Helper method to populate the test database
    """
    conn = generate_test_db.create_connection(TEST_DB_URL)
    with conn:
        # Add entries
        for entry in DB_TEST_ENTRIES:
            generate_test_db.add_entry(
                conn, generate_test_db.Tables.NEW_ADS.value, entry)
            generate_test_db.add_entry(
                conn, generate_test_db.Tables.ADS.value, entry)


# Module level setup and teardown, executed once at the beginnning and end of the module
def setup_module():
    """
    setup any state specific to the execution of the given module.
    """
    populate_test_db()


def teardown_module():
    """
    teardown any state that was previously setup with a setup_module
    method.
    """
    if os.path.exists(TEST_DB_URL):
        os.remove(TEST_DB_URL)


class TestBasicAppEndpoints():
    """
    Basic tests checking that all required endpoints are present.
    """

    def test_default_endpoint(self):
        """
        Test that the start page endpoint is accessible
        """
        response = client.get("/")
        assert response.is_success
        assert response.template.name == "index.html"

    def test_data_endpoint(self):
        """
        Test that the data page endpoint is accessible
        """
        response = client.get("/data")
        assert response.is_success
        assert response.template.name == "data.html"

    def test_new_ads_endpoint(self):
        """
        Test that the new-ads page endpoint is accessible
        """
        response = client.get("/new-ads")
        assert response.is_success
        assert response.template.name == "ads.html"

    def test_all_ads_endpoint(self):
        """
        Test that the all-ads page endpoint is accessible
        """
        response = client.get("all-ads")
        assert response.is_success
        assert response.template.name == "ads.html"

    def test_download_new_ads_endpoint(self):
        """
        Test that the download-new-ads page endpoint is accessible
        """
        response = client.get("/download-new-ads")
        assert response.is_success
        with pytest.raises(AttributeError):
            # Should not have such an attribute
            response.template.name  # pylint: disable=W0104

    def test_download_all_ads_endpoint(self):
        """
        Test that the download-all-ads page endpoint is accessible
        """
        response = client.get("/download-all-ads")
        assert response.is_success
        with pytest.raises(AttributeError):
            # Should not have such an attribute
            response.template.name  # pylint: disable=W0104


# The all-ads and new-ads endpoind behave the same way as their download counterparts.
# They just show the content in an HTML response format instead of csv
# basic tests will be enough to show the correct numbers and behavior is present
class TestNewAds:
    """
    Test cases covering the behaviour of the new-ads end point
    """

    @classmethod
    def setup_class(cls):
        """
        setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.endpoint = "new-ads"

    def _verify_endpoint(self, response, expected_listings):
        """
        Utility method to perform the needed assertions
        """
        ad_list_len = len(response.context['ad_list'])
        show_summary = response.context['show_summary']
        summary_data = response.context['summary_data']
        assert response.is_success
        assert show_summary
        assert ad_list_len == expected_listings
        assert sum(summary_data.values()) == ad_list_len

    def _verify_invalid_endpoint_params(self, response):
        """
        Utility method to verify the behaviour of the endpoint with invalid params.
        """
        assert not response.is_success
        assert response.is_error
        assert response.is_client_error
        assert response.status_code == 422
        assert response.reason_phrase == "Unprocessable Entity"

    def test_read_no_filters(self):
        """
        Showing the data without filters should be sorted.
        """
        response = client.get(f"/{self.endpoint}")
        self._verify_endpoint(response, expected_listings=len(DB_TEST_ENTRIES))

    def test_read_with_limit(self):
        """
        Test data filtering based on the limit query parameter
        """
        response = client.get(f"/{self.endpoint}?limit=2")
        self._verify_endpoint(response, expected_listings=2)

    def test_location_filter(self):
        """
        Test data filtering based on the location query parameter
        """
        response = client.get(f"/{self.endpoint}?location=Младост 4")
        self._verify_endpoint(response, expected_listings=1)

    def test_price_filter(self):
        """
        Test data filtering based on the price query parameter
        """
        response = client.get(f"/{self.endpoint}?price=100000")
        self._verify_endpoint(response, expected_listings=5)

    def test_size_filter(self):
        """
        Test data filtering based on the home_size query parameter
        """
        response = client.get(f"/{self.endpoint}?home_size=100")
        self._verify_endpoint(response, expected_listings=19)

    def test_source_filter(self):
        """
        Test data filtering based on the source_name query parameter
        """
        response = client.get(f"/{self.endpoint}?source_name=bezkomisiona")
        self._verify_endpoint(response, expected_listings=5)

    def test_type_filter(self):
        """
        Test data filtering based on the home_type query parameter
        """
        response = client.get(f"/{self.endpoint}?home_type=Двустаен")
        self._verify_endpoint(response, expected_listings=5)

    def test_combo_filters(self):
        """
        Test data filtering based on the multiple query parameters
        """
        response = client.get(
            f"/{self.endpoint}?home_type=Двустаен&source_name=home2u")
        self._verify_endpoint(response, expected_listings=1)

    def test_all_filters_applied(self):
        """
        Test data filtering when all query parameters are added
        """
        other_params = "home_type=Многостаен&price=300000&home_size=70&location=Младост 1A"
        response = client.get(
            f"/{self.endpoint}?source_name=bezkomisiona&{other_params}")
        self._verify_endpoint(response, expected_listings=1)

    # Bad weather testcases
    def test_invalid_query_parameter(self):
        """
        Test data filtering with invalid parameter passed.
        """
        response = client.get(f"/{self.endpoint}?locc=Младост 1D")
        self._verify_endpoint(response, expected_listings=len(DB_TEST_ENTRIES))

    def test_invalid_location_filter(self):
        """
        Invalid location filter passed should return an error and invalid response
        """
        response = client.get(f"/{self.endpoint}?location=Младост 1D")
        self._verify_invalid_endpoint_params(response)

    def test_invalid_source_filter(self):
        """
        Invalid source filter passed should return an error and invalid response
        """
        response = client.get(f"/{self.endpoint}?source_name=invalid")
        self._verify_invalid_endpoint_params(response)

    def test_invalid_type_filter(self):
        """
        Invalid home_type filter passed should return an error and invalid response
        """
        response = client.get(f"/{self.endpoint}?home_type=Dvustaen")
        self._verify_invalid_endpoint_params(response)

    def test_invalid_size_filter(self):
        """
        Invalid home_size filter passed should return an error and invalid response
        """
        response = client.get(f"/{self.endpoint}?home_size=big")
        self._verify_invalid_endpoint_params(response)

    def test_invalid_price_filter(self):
        """
        Invalid price filter passed should return an error and invalid response
        """
        response = client.get(f"/{self.endpoint}?price=123d")
        self._verify_invalid_endpoint_params(response)

    def test_all_filters_invalid_location(self):
        """
        Invalid location filter passed along with all other all other correct parameters should
        an return error and an invalid response
        """
        other_params = "home_type=Многостаен&price=300000&home_size=70&location=Младост 1D"
        response = client.get(
            f"/{self.endpoint}?source_name=bezkomisiona&{other_params}")
        self._verify_invalid_endpoint_params(response)


class TestAllAds(TestNewAds):
    """
    Test cases covering the behaviour of the all-ads endpoint
    Note: The behaviour should be the same as the new-ads endpoint
    Difference is that summary table will not be shown
    """
    @classmethod
    def setup_class(cls):
        """
        setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.endpoint = "all-ads"

    def _verify_endpoint(self, response, expected_listings):
        """
        Utility method to perform the needed assertions
        """
        ad_list_len = len(response.context['ad_list'])
        show_summary = response.context['show_summary']

        assert response.is_success
        assert not show_summary
        assert ad_list_len == expected_listings
        with pytest.raises(KeyError):
            _ = response.context['summary_data']


class TestDownloadNewAds:
    """
    Testing the behavior of the download-new-ads endpoint.
    """

    @classmethod
    def setup_class(cls):
        """
        setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.endpoint = "download-new-ads"

    def test_read_no_filters(self):
        """
        Showing the data without filters should be sorted.
        """
        response = client.get(f"/{self.endpoint}")
        expected = """
id,Свалено от,Цена,Квартал,Големина в кв.м.,Тип на имота,URL,Снимка,Намерено на дата
4,addressbg,57644,Младост 4,142,Едностаен,https://addressbg.bg/66,some_image,SOME_DATE
6,superimoti,61497,Илинден,193,Студио,https://superimoti.bg/66,some_image,SOME_DATE
7,bezkomisiona,98228,Овча купел 2,99,Тристаен,https://bezkomisiona.bg/30,some_image,SOME_DATE
29,imotbg,98807,Белите Брези,106,Едностаен,https://imotbg.bg/87,some_image,SOME_DATE
18,superimoti,98964,Димитър Миленков,123,Многостаен,https://superimoti.bg/77,some_image,SOME_DATE
14,addressbg,126041,Център,94,Мезонет,https://addressbg.bg/61,some_image,SOME_DATE
9,era,131733,Света троица,163,Мезонет,https://era.bg/69,some_image,SOME_DATE
2,bezkomisiona,170294,Слатина,185,Мезонет,https://bezkomisiona.bg/61,some_image,SOME_DATE
19,home2u,173626,Хиподрума,61,Тристаен,https://home2u.bg/64,some_image,SOME_DATE
10,ues,177669,Обеля 2,192,Мезонет,https://ues.bg/80,some_image,SOME_DATE
26,luximmo,192682,Банишора,166,Едностаен,https://luximmo.bg/45,some_image,SOME_DATE
23,bulgarianproperties,193864,Света троица,123,Мезонет,https://bulgarianproperties.bg/10,some_image,SOME_DATE
3,superimoti,210395,Горубляне,195,Двустаен,https://superimoti.bg/64,some_image,SOME_DATE
21,galardo,215036,Дружба 2,172,Едностаен,https://galardo.bg/49,some_image,SOME_DATE
5,avista,216479,Младост 2,125,Двустаен,https://avista.bg/96,some_image,SOME_DATE
12,mirelabg,232870,Левски,155,Мезонет,https://mirelabg.bg/76,some_image,SOME_DATE
11,arcoreal,234161,Връбница 2,81,Двустаен,https://arcoreal.bg/25,some_image,SOME_DATE
24,bezkomisiona,237987,Люлин 6,72,Многостаен,https://bezkomisiona.bg/29,some_image,SOME_DATE
28,home2u,240912,Експериментален,156,Мезонет,https://home2u.bg/20,some_image,SOME_DATE
20,era,242059,Стрелбище,127,Едностаен,https://era.bg/30,some_image,SOME_DATE
1,luximmo,246483,Люлин 3,84,Двустаен,https://luximmo.bg/23,some_image,SOME_DATE
30,novdom1,255456,Зона Б-5-3,111,Мезонет,https://novdom1.bg/74,some_image,SOME_DATE
27,home2u,268885,Градина,199,Двустаен,https://home2u.bg/83,some_image,SOME_DATE
15,bezkomisiona,280778,Младост 1A,193,Многостаен,https://bezkomisiona.bg/46,some_image,SOME_DATE
16,yavlena,282492,Славия,56,Студио,https://yavlena.bg/97,some_image,SOME_DATE
8,bezkomisiona,289343,Люлин,68,Студио,https://bezkomisiona.bg/57,some_image,SOME_DATE
17,avista,293794,Република 2,75,Едностаен,https://avista.bg/14,some_image,SOME_DATE
22,yourhome,295392,Овча купел 1,97,Многостаен,https://yourhome.bg/83,some_image,SOME_DATE
13,ues,296825,Люлин 9,88,Многостаен,https://ues.bg/35,some_image,SOME_DATE
25,yavlena,299179,Дървеница,120,Мезонет,https://yavlena.bg/11,some_image,SOME_DATE
"""
        assert response.text.replace("\r", "").strip() == expected.strip()

    def test_read_with_limit(self):
        """
        Test data filtering based on the limit query parameter
        """
        response = client.get(f"/{self.endpoint}?limit=2")
        expected = """
id,Свалено от,Цена,Квартал,Големина в кв.м.,Тип на имота,URL,Снимка,Намерено на дата
4,addressbg,57644,Младост 4,142,Едностаен,https://addressbg.bg/66,some_image,SOME_DATE
6,superimoti,61497,Илинден,193,Студио,https://superimoti.bg/66,some_image,SOME_DATE
"""
        assert response.text.replace("\r", "").strip() == expected.strip()

    def test_location_filter(self):
        """
        Test data filtering based on the location query parameter
        """
        response = client.get(f"/{self.endpoint}?location=Младост 4")
        expected = """
id,Свалено от,Цена,Квартал,Големина в кв.м.,Тип на имота,URL,Снимка,Намерено на дата
4,addressbg,57644,Младост 4,142,Едностаен,https://addressbg.bg/66,some_image,SOME_DATE
"""
        assert response.text.replace("\r", "").strip() == expected.strip()

    def test_price_filter(self):
        """
        Test data filtering based on the price query parameter
        """
        response = client.get(f"/{self.endpoint}?price=100000")
        expected = """
id,Свалено от,Цена,Квартал,Големина в кв.м.,Тип на имота,URL,Снимка,Намерено на дата
4,addressbg,57644,Младост 4,142,Едностаен,https://addressbg.bg/66,some_image,SOME_DATE
6,superimoti,61497,Илинден,193,Студио,https://superimoti.bg/66,some_image,SOME_DATE
7,bezkomisiona,98228,Овча купел 2,99,Тристаен,https://bezkomisiona.bg/30,some_image,SOME_DATE
29,imotbg,98807,Белите Брези,106,Едностаен,https://imotbg.bg/87,some_image,SOME_DATE
18,superimoti,98964,Димитър Миленков,123,Многостаен,https://superimoti.bg/77,some_image,SOME_DATE
"""
        assert response.text.replace("\r", "").strip() == expected.strip()

    def test_size_filter(self):
        """
        Test data filtering based on the home_size query parameter
        """
        response = client.get(f"/{self.endpoint}?home_size=100")
        expected = """
id,Свалено от,Цена,Квартал,Големина в кв.м.,Тип на имота,URL,Снимка,Намерено на дата
29,imotbg,98807,Белите Брези,106,Едностаен,https://imotbg.bg/87,some_image,SOME_DATE
30,novdom1,255456,Зона Б-5-3,111,Мезонет,https://novdom1.bg/74,some_image,SOME_DATE
25,yavlena,299179,Дървеница,120,Мезонет,https://yavlena.bg/11,some_image,SOME_DATE
18,superimoti,98964,Димитър Миленков,123,Многостаен,https://superimoti.bg/77,some_image,SOME_DATE
23,bulgarianproperties,193864,Света троица,123,Мезонет,https://bulgarianproperties.bg/10,some_image,SOME_DATE
5,avista,216479,Младост 2,125,Двустаен,https://avista.bg/96,some_image,SOME_DATE
20,era,242059,Стрелбище,127,Едностаен,https://era.bg/30,some_image,SOME_DATE
4,addressbg,57644,Младост 4,142,Едностаен,https://addressbg.bg/66,some_image,SOME_DATE
12,mirelabg,232870,Левски,155,Мезонет,https://mirelabg.bg/76,some_image,SOME_DATE
28,home2u,240912,Експериментален,156,Мезонет,https://home2u.bg/20,some_image,SOME_DATE
9,era,131733,Света троица,163,Мезонет,https://era.bg/69,some_image,SOME_DATE
26,luximmo,192682,Банишора,166,Едностаен,https://luximmo.bg/45,some_image,SOME_DATE
21,galardo,215036,Дружба 2,172,Едностаен,https://galardo.bg/49,some_image,SOME_DATE
2,bezkomisiona,170294,Слатина,185,Мезонет,https://bezkomisiona.bg/61,some_image,SOME_DATE
10,ues,177669,Обеля 2,192,Мезонет,https://ues.bg/80,some_image,SOME_DATE
6,superimoti,61497,Илинден,193,Студио,https://superimoti.bg/66,some_image,SOME_DATE
15,bezkomisiona,280778,Младост 1A,193,Многостаен,https://bezkomisiona.bg/46,some_image,SOME_DATE
3,superimoti,210395,Горубляне,195,Двустаен,https://superimoti.bg/64,some_image,SOME_DATE
27,home2u,268885,Градина,199,Двустаен,https://home2u.bg/83,some_image,SOME_DATE
"""
        assert response.text.replace("\r", "").strip() == expected.strip()

    def test_source_filter(self):
        """
        Test data filtering based on the source_name query parameter
        """
        response = client.get(f"/{self.endpoint}?source_name=bezkomisiona")
        expected = """
id,Свалено от,Цена,Квартал,Големина в кв.м.,Тип на имота,URL,Снимка,Намерено на дата
2,bezkomisiona,170294,Слатина,185,Мезонет,https://bezkomisiona.bg/61,some_image,SOME_DATE
7,bezkomisiona,98228,Овча купел 2,99,Тристаен,https://bezkomisiona.bg/30,some_image,SOME_DATE
8,bezkomisiona,289343,Люлин,68,Студио,https://bezkomisiona.bg/57,some_image,SOME_DATE
15,bezkomisiona,280778,Младост 1A,193,Многостаен,https://bezkomisiona.bg/46,some_image,SOME_DATE
24,bezkomisiona,237987,Люлин 6,72,Многостаен,https://bezkomisiona.bg/29,some_image,SOME_DATE
"""
        assert response.text.replace("\r", "").strip() == expected.strip()

    def test_type_filter(self):
        """
        Test data filtering based on the home_type query parameter
        """
        response = client.get(f"/{self.endpoint}?home_type=Двустаен")
        expected = """
id,Свалено от,Цена,Квартал,Големина в кв.м.,Тип на имота,URL,Снимка,Намерено на дата
1,luximmo,246483,Люлин 3,84,Двустаен,https://luximmo.bg/23,some_image,SOME_DATE
3,superimoti,210395,Горубляне,195,Двустаен,https://superimoti.bg/64,some_image,SOME_DATE
5,avista,216479,Младост 2,125,Двустаен,https://avista.bg/96,some_image,SOME_DATE
11,arcoreal,234161,Връбница 2,81,Двустаен,https://arcoreal.bg/25,some_image,SOME_DATE
27,home2u,268885,Градина,199,Двустаен,https://home2u.bg/83,some_image,SOME_DATE
"""
        assert response.text.replace("\r", "").strip() == expected.strip()

    def test_combo_filters(self):
        """
        Test data filtering based on the multiple query parameters
        """
        response = client.get(
            f"/{self.endpoint}?home_type=Двустаен&source_name=home2u")
        expected = """
id,Свалено от,Цена,Квартал,Големина в кв.м.,Тип на имота,URL,Снимка,Намерено на дата
27,home2u,268885,Градина,199,Двустаен,https://home2u.bg/83,some_image,SOME_DATE"""
        assert response.text.replace("\r", "").strip() == expected.strip()

    def test_all_filters_applied(self):
        """
        Test data filtering when all query parameters are added
        """
        other_params = "home_type=Многостаен&price=300000&home_size=70&location=Младост 1A"
        response = client.get(
            f"/{self.endpoint}?source_name=bezkomisiona&{other_params}")
        expected = """
id,Свалено от,Цена,Квартал,Големина в кв.м.,Тип на имота,URL,Снимка,Намерено на дата
15,bezkomisiona,280778,Младост 1A,193,Многостаен,https://bezkomisiona.bg/46,some_image,SOME_DATE"""
        assert response.text.replace("\r", "").strip() == expected.strip()

    # Bad weather testcases
    def test_invalid_query_parameter(self):
        """
        Test data filtering with invalid parameter passed.
        Should return all listings
        """
        response = client.get(f"/{self.endpoint}?locc=Младост 1D")
        # invalid query parameter returns all listings
        expected = """
id,Свалено от,Цена,Квартал,Големина в кв.м.,Тип на имота,URL,Снимка,Намерено на дата
4,addressbg,57644,Младост 4,142,Едностаен,https://addressbg.bg/66,some_image,SOME_DATE
6,superimoti,61497,Илинден,193,Студио,https://superimoti.bg/66,some_image,SOME_DATE
7,bezkomisiona,98228,Овча купел 2,99,Тристаен,https://bezkomisiona.bg/30,some_image,SOME_DATE
29,imotbg,98807,Белите Брези,106,Едностаен,https://imotbg.bg/87,some_image,SOME_DATE
18,superimoti,98964,Димитър Миленков,123,Многостаен,https://superimoti.bg/77,some_image,SOME_DATE
14,addressbg,126041,Център,94,Мезонет,https://addressbg.bg/61,some_image,SOME_DATE
9,era,131733,Света троица,163,Мезонет,https://era.bg/69,some_image,SOME_DATE
2,bezkomisiona,170294,Слатина,185,Мезонет,https://bezkomisiona.bg/61,some_image,SOME_DATE
19,home2u,173626,Хиподрума,61,Тристаен,https://home2u.bg/64,some_image,SOME_DATE
10,ues,177669,Обеля 2,192,Мезонет,https://ues.bg/80,some_image,SOME_DATE
26,luximmo,192682,Банишора,166,Едностаен,https://luximmo.bg/45,some_image,SOME_DATE
23,bulgarianproperties,193864,Света троица,123,Мезонет,https://bulgarianproperties.bg/10,some_image,SOME_DATE
3,superimoti,210395,Горубляне,195,Двустаен,https://superimoti.bg/64,some_image,SOME_DATE
21,galardo,215036,Дружба 2,172,Едностаен,https://galardo.bg/49,some_image,SOME_DATE
5,avista,216479,Младост 2,125,Двустаен,https://avista.bg/96,some_image,SOME_DATE
12,mirelabg,232870,Левски,155,Мезонет,https://mirelabg.bg/76,some_image,SOME_DATE
11,arcoreal,234161,Връбница 2,81,Двустаен,https://arcoreal.bg/25,some_image,SOME_DATE
24,bezkomisiona,237987,Люлин 6,72,Многостаен,https://bezkomisiona.bg/29,some_image,SOME_DATE
28,home2u,240912,Експериментален,156,Мезонет,https://home2u.bg/20,some_image,SOME_DATE
20,era,242059,Стрелбище,127,Едностаен,https://era.bg/30,some_image,SOME_DATE
1,luximmo,246483,Люлин 3,84,Двустаен,https://luximmo.bg/23,some_image,SOME_DATE
30,novdom1,255456,Зона Б-5-3,111,Мезонет,https://novdom1.bg/74,some_image,SOME_DATE
27,home2u,268885,Градина,199,Двустаен,https://home2u.bg/83,some_image,SOME_DATE
15,bezkomisiona,280778,Младост 1A,193,Многостаен,https://bezkomisiona.bg/46,some_image,SOME_DATE
16,yavlena,282492,Славия,56,Студио,https://yavlena.bg/97,some_image,SOME_DATE
8,bezkomisiona,289343,Люлин,68,Студио,https://bezkomisiona.bg/57,some_image,SOME_DATE
17,avista,293794,Република 2,75,Едностаен,https://avista.bg/14,some_image,SOME_DATE
22,yourhome,295392,Овча купел 1,97,Многостаен,https://yourhome.bg/83,some_image,SOME_DATE
13,ues,296825,Люлин 9,88,Многостаен,https://ues.bg/35,some_image,SOME_DATE
25,yavlena,299179,Дървеница,120,Мезонет,https://yavlena.bg/11,some_image,SOME_DATE
"""
        assert response.is_success
        assert response.text.replace("\r", "").strip() == expected.strip()

    def test_invalid_location_filter(self):
        """
        Invalid location filter passed should return an error and invalid response
        """
        response = client.get(f"/{self.endpoint}?location=Младост 1D")
        assert not response.is_success

    def test_invalid_source_filter(self):
        """
        Invalid source filter passed should return an error and invalid response
        """
        response = client.get(f"/{self.endpoint}?source_name=invalid")
        assert not response.is_success

    def test_invalid_type_filter(self):
        """
        Invalid home_type filter passed should return an error and invalid response
        """
        response = client.get(f"/{self.endpoint}?home_type=Dvustaen")
        assert not response.is_success

    def test_invalid_size_filter(self):
        """
        Invalid home_size filter passed should return an error and invalid response
        """
        response = client.get(f"/{self.endpoint}?home_size=big")
        assert not response.is_success

    def test_invalid_price_filter(self):
        """
        Invalid price filter passed should return an error and invalid response
        """
        response = client.get(f"/{self.endpoint}?price=123d")
        assert not response.is_success

    def test_all_filters_invalid_location(self):
        """
        Invalid location filter passed along with all other all other correct parameters should
        an return error and an invalid response
        """
        other_params = "home_type=Многостаен&price=300000&home_size=70&location=Младост 1D"
        response = client.get(
            f"/{self.endpoint}?source_name=bezkomisiona&{other_params}")
        assert not response.is_success


class TestDownloadAllAds(TestDownloadNewAds):
    """
    Testing the behavior of the download-all-ads endpoint.
    """

    @classmethod
    def setup_class(cls):
        """setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.endpoint = "download-all-ads"
