from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from coacher import models
from coacher.database import engine


app = FastAPI()

#app.mount("/static", StaticFiles(directory="./static"), name="static")

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates/")

from coacher.views import main, tasks  # Needs to be below the creation of the app instance
