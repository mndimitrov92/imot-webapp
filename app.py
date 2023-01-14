import uvicorn
from collections import defaultdict, Counter
from fastapi import FastAPI, Request, Query, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from db_utils import models, crud, schemas
from db_utils.database import SessionLocal, engine
from utils import constants


# build the database
models.Base.metadata.create_all(bind=engine)

# Dependency


def get_db():
    """
    It creates a database connection, and then yields it to the caller. 
    The caller can then use the connection, and when it's done, the connection is closed. 
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    # Initial population of the dictionary
    for source in list(constants.AdSource):
        all_sources[source.value]
    # collect the sources that have listings
    sources = [data.source_name for data in dataset]
    source_counter = Counter(sources)
    all_sources.update(source_counter)
    return all_sources


def _read_ads(source_name, price, location, home_size, home_type, limit, db, only_new_ads=False):
    if any([param for param in [source_name, price, home_size, home_type, location] if param is not None]):
        my_ads = crud.get_filtered_ads(db=db,
                                       source_name=source_name,
                                       price=price,
                                       location=location,
                                       home_size=home_size,
                                       home_type=home_type,
                                       limit=limit,
                                       only_new_ads=only_new_ads)
    else:
        my_ads = crud.get_ordered_ads(
            db=db, limit=limit, only_new_ads=only_new_ads)
    return my_ads


def _display_ads(request, source_name, price, location, home_size, home_type, limit, db, only_new_ads=False):
    # my_ads is a list of Ads objects. The attributes are the db columns
    my_ads = _read_ads(source_name, price, location,
                       home_size, home_type, limit, db, only_new_ads)
    dict_param = {"request": request, "ad_list": my_ads, "show_summary": False}
    if only_new_ads:
        summary = _build_summary_dict(my_ads)
        dict_param["summary_data"] = summary
        dict_param["show_summary"] = True
    return templates.TemplateResponse("ads.html", dict_param)


@app.get("/new-ads", response_class=HTMLResponse, response_model=List[schemas.NewAds])
async def read_new_ads(request: Request,
                       source_name: Optional[constants.AdSource] = None,
                       price: Optional[int] = Query(None, ge=1),
                       location: Optional[constants.AdLocation] = None,
                       home_size: Optional[int] = Query(None, ge=1),
                       home_type: Optional[constants.HomeType] = None,
                       limit: Optional[int] = Query(None, ge=1),
                       db: Session = Depends(get_db),
                       ):
    """
    Dispay function for all collected new ads with support for filters based on a set of price, location, source, 
    home_size, home_type.
    """
    return _display_ads(request=request,
                        source_name=source_name,
                        price=price, location=location,
                        home_size=home_size,
                        home_type=home_type,
                        limit=limit,
                        db=db,
                        only_new_ads=True)


@app.get("/all-ads", response_class=HTMLResponse, response_model=List[schemas.Ads])
async def read_all_ads(request: Request,
                       source_name: Optional[constants.AdSource] = None,
                       price: Optional[int] = Query(None, ge=1),
                       location: Optional[constants.AdLocation] = None,
                       home_size: Optional[int] = Query(None, ge=1),
                       home_type: Optional[constants.HomeType] = None,
                       limit: Optional[int] = Query(None, ge=1, le=100),
                       db: Session = Depends(get_db),
                       ):
    """
    Dispay function for all collected ads with support for filters based on a set of price, location, source,
    home_size, home_type.
    """
    return _display_ads(request=request,
                        source_name=source_name,
                        price=price,
                        location=location,
                        home_size=home_size,
                        home_type=home_type,
                        limit=limit,
                        db=db)


@app.get("/download-all-ads", response_model=List[schemas.Ads])
async def download_all_ads(source_name: Optional[constants.AdSource] = None,
                           price: Optional[int] = Query(None, ge=1),
                           location: Optional[constants.AdLocation] = None,
                           home_size: Optional[int] = Query(None, ge=1),
                           home_type: Optional[constants.HomeType] = None,
                           limit: Optional[int] = Query(None, ge=1),
                           db: Session = Depends(get_db),
                           ):
    """

    """
    my_ads = _read_ads(source_name, price, location, home_size,
                       home_type, limit, db, only_new_ads=False)
    return my_ads


@app.get("/download-new-ads", response_model=List[schemas.NewAds])
async def download_all_ads(source_name: Optional[constants.AdSource] = None,
                           price: Optional[int] = Query(None, ge=1),
                           location: Optional[constants.AdLocation] = None,
                           home_size: Optional[int] = Query(None, ge=1),
                           home_type: Optional[constants.HomeType] = None,
                           limit: Optional[int] = Query(None, ge=1),
                           db: Session = Depends(get_db),
                           ):
    """

    """
    my_ads = _read_ads(source_name, price, location, home_size,
                       home_type, limit, db, only_new_ads=True)
    return my_ads


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
    It starts a server on port 8000, and when you go to the URL http://localhost:8000/docs, it will show
    you the documentation for the API
    """
    config = uvicorn.Config("app:app", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    run()
