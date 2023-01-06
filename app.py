import uvicorn
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


@app.get("/new-ads", response_class=HTMLResponse)
async def read_new_ads(request: Request):
    """
    It returns a response object that renders the ads.html template with the request object as a context
    variable

    :param request: The request object
    :type request: Request
    :return: a TemplateResponse object.
    """
    return templates.TemplateResponse("ads.html", {"request": request})


@app.get("/all-ads", response_class=HTMLResponse, response_model=List[schemas.Ads])
async def read_all_ads(request: Request,
                       source_name: Optional[constants.AdSource] = None,
                       price: Optional[int] = Query(None, ge=1),
                       location: Optional[constants.AdLocation] = None,
                       limit: Optional[int] = Query(None, ge=1, le=100),
                       db: Session = Depends(get_db),
                       ):
    """
    Dispay function for all collected ads with support for filters based on a set of price, location, source.
    """
    # my_ads is a list of Ads objects. The attributes are the db columns
    if any([param for param in [source_name, price, location] if param is not None]):
        my_ads = crud.get_filtered_ads(db,
                                       source_name=source_name,
                                       price=price,
                                       location=location,
                                       limit=limit)
    else:
        my_ads = crud.get_ordered_ads(db, limit=limit)
    return templates.TemplateResponse("ads.html", {"request": request, "ad_list": my_ads})


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
