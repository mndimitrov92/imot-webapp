"""
Main app module.
Initializes the application and starts the uvicorn server.
"""
from collections import defaultdict, Counter
import io
from typing import Optional, List
from fastapi import FastAPI, Request, Query, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from sqlalchemy.orm import Session
import uvicorn

from db_utils import models, crud, schemas
from db_utils.database import SessionLocal, engine
from utils import constants, create_db_folder


# prepare directory and build the database
create_db_folder()
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    """
    It creates a database connection, and then yields it to the caller.
    The caller can then use the connection, and when it's done, the connection is closed.
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


app = FastAPI()
app.mount("/static", StaticFiles(directory=constants.STATIC_DIR), name="static")
templates = Jinja2Templates("templates")


@app.get("/", response_class=HTMLResponse)
async def read_homepage(request: Request):
    """
    It returns a response object that renders the index.html template with the request object as a
    context variable

    :param request: Request
    :type request: Request
    :return: a TemplateResponse object.
    """
    return templates.TemplateResponse("index.html", {"request": request})


def _build_summary_dict(dataset) -> Counter:
    """
    It takes a dataset and returns a dictionary of the number of listings per source

    :param dataset: a list of tuples, where each tuple is a listing and its source
    :return: A dictionary with the source as the key and the number of listings as the value.
    """
    all_sources = defaultdict(int)
    for source in list(constants.AdSource):
        # Initialize the value for all sources
        all_sources[source.value] = 0
    # collect the sources that have listings
    sources = [data.source_name for data in dataset]
    source_counter = Counter(sources)
    all_sources.update(source_counter)
    return all_sources


def _save_to_csv(data, filename="export.csv"):
    """
    It takes a list of objects and converts them to a list of dictionaries,
    then it converts the list of dictionaries to a pandas dataframe and
    then it converts the dataframe to a csv file and returns it as a response

    :param data: the list of ads objects
    :param filename: The name of the file that will be downloaded, defaults to export.csv (optional)
    :return: A StreamingResponse object.
    """
    # Convert the ads objects to a list of regular dictionaries and remove unneccesary keys
    ad_list = []
    for each_ad in data:
        ad_list.append({"id": each_ad.id,
                        "Свалено от": each_ad.source_name,
                        "Цена": each_ad.price,
                        "Квартал": each_ad.location,
                        "Големина в кв.м.": each_ad.home_size,
                        "Тип на имота": each_ad.home_type,
                        "URL": each_ad.url,
                        "Снимка": each_ad.image,
                        "Намерено на дата": each_ad.scraping_date})
    data_frame = pd.DataFrame(ad_list)
    stream = io.StringIO()
    data_frame.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def _read_ads(source_name, price, location, home_size,  # pylint: disable=R0913
              home_type, limit, db_session, only_new_ads=False):
    filters_list = [source_name, price, home_size, home_type, location]
    filtered = (param for param in filters_list if param is not None)
    if any(filtered):
        my_ads = crud.get_filtered_ads(db_session=db_session,
                                       source_name=source_name,
                                       price=price,
                                       location=location,
                                       home_size=home_size,
                                       home_type=home_type,
                                       limit=limit,
                                       only_new_ads=only_new_ads)
    else:
        my_ads = crud.get_ordered_ads(
            db_session=db_session, limit=limit, only_new_ads=only_new_ads)
    return my_ads


def _display_ads(request, source_name, price, location,  # pylint: disable=R0913
                 home_size, home_type, limit, db_session, only_new_ads=False):
    # my_ads is a list of Ads objects. The attributes are the db columns
    my_ads = _read_ads(source_name, price, location,
                       home_size, home_type, limit, db_session, only_new_ads)
    dict_param = {"request": request, "ad_list": my_ads, "show_summary": False}
    if only_new_ads:
        summary = _build_summary_dict(my_ads)
        dict_param["summary_data"] = summary
        dict_param["show_summary"] = True
    return templates.TemplateResponse("ads.html", dict_param)


@app.get("/new-ads", response_class=HTMLResponse, response_model=List[schemas.NewAds])
async def read_new_ads(request: Request,  # pylint: disable=R0913
                       source_name: Optional[constants.AdSource] = None,
                       price: Optional[int] = Query(None, ge=1),
                       location: Optional[constants.AdLocation] = None,
                       home_size: Optional[int] = Query(None, ge=1),
                       home_type: Optional[constants.HomeType] = None,
                       limit: Optional[int] = Query(None, ge=1),
                       db_session: Session = Depends(get_db),
                       ):
    """
    Dispay function for all collected new ads with support for filters based on a set of
    price, location, source, home_size, home_type.
    """
    return _display_ads(request=request,
                        source_name=source_name,
                        price=price, location=location,
                        home_size=home_size,
                        home_type=home_type,
                        limit=limit,
                        db_session=db_session,
                        only_new_ads=True)


@app.get("/all-ads", response_class=HTMLResponse, response_model=List[schemas.Ads])
async def read_all_ads(request: Request,  # pylint: disable=R0913
                       source_name: Optional[constants.AdSource] = None,
                       price: Optional[int] = Query(None, ge=1),
                       location: Optional[constants.AdLocation] = None,
                       home_size: Optional[int] = Query(None, ge=1),
                       home_type: Optional[constants.HomeType] = None,
                       limit: Optional[int] = Query(None, ge=1, le=100),
                       db_session: Session = Depends(get_db),
                       ):
    """
    Dispay function for all collected ads with support for filters based on a set of
    price, location, source, home_size, home_type.
    """
    return _display_ads(request=request,
                        source_name=source_name,
                        price=price,
                        location=location,
                        home_size=home_size,
                        home_type=home_type,
                        limit=limit,
                        db_session=db_session)


@app.get("/download-all-ads", response_model=List[schemas.Ads])
async def download_all_ads(source_name: Optional[constants.AdSource] = None,  # pylint: disable=R0913
                           price: Optional[int] = Query(None, ge=1),
                           location: Optional[constants.AdLocation] = None,
                           home_size: Optional[int] = Query(None, ge=1),
                           home_type: Optional[constants.HomeType] = None,
                           limit: Optional[int] = Query(None, ge=1),
                           db_session: Session = Depends(get_db),
                           ):
    """
    Download API endpoint function for all collected ads with support for filters based on a set of
    price, location, source, home_size, home_type.
    """
    my_ads = _read_ads(source_name, price, location, home_size,
                       home_type, limit, db_session, only_new_ads=False)
    return _save_to_csv(my_ads)


@app.get("/download-new-ads", response_model=List[schemas.NewAds])
async def download_new_ads(source_name: Optional[constants.AdSource] = None,  # pylint: disable=R0913
                           price: Optional[int] = Query(None, ge=1),
                           location: Optional[constants.AdLocation] = None,
                           home_size: Optional[int] = Query(None, ge=1),
                           home_type: Optional[constants.HomeType] = None,
                           limit: Optional[int] = Query(None, ge=1),
                           db_session: Session = Depends(get_db),
                           ):
    """
    Download API endpoint function for new ads with support for filters based on a set of
    price, location, source, home_size, home_type.
    """
    my_ads = _read_ads(source_name, price, location, home_size,
                       home_type, limit, db_session, only_new_ads=True)
    return _save_to_csv(my_ads)


@app.get("/data", response_class=HTMLResponse)
async def read_additional_data(request: Request):
    """
    It returns a template response with the template data.html and the request object

    :param request: The request object
    :type request: Request
    :return: a TemplateResponse object.
    """
    return templates.TemplateResponse("data.html", {"request": request})


def run():
    """
    It starts a server on port 8000, and when you go to the URL http://localhost:8000/docs,
    it will show you the documentation for the API
    """
    config = uvicorn.Config("app:app", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    run()
