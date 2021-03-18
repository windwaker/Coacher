from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from coacher import models
from coacher.database import engine, SessionLocal
from coacher.models import Player

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class PlayerRequest(BaseModel):
    """
    Can we make this obsolete and use the DB model instead?
    """
    first_name: str
    last_name: str
    date_of_birth: str


@app.get("/")
def dashboard(request: Request, first_name=None, active=None, db: Session = Depends(get_db)):
    """
    Displays the player list and CRUD screen
    :return: A jinja template
    """
    players = db.query(Player)

    if first_name:
        players = players.filter(Player.first_name == first_name)

    if active == 'on':
        players = players.filter(Player.active.is_(True))
        print('on')
    else:
        players = players.filter(Player.active.is_(False))
        print('off')

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "players": players,
        "first_name": first_name,
        "active": active
    })


def do_some_heavy_lifting(first_name: str):
    db = SessionLocal()

    player = db.query(Player).filter(Player.first_name == first_name).first()
    player.date_of_birth = "01-01-2021"

    db.add(player)
    db.commit()


@app.post("/player")
async def create_player(player_request: PlayerRequest,
                        background_tasks: BackgroundTasks,
                        db: Session = Depends(get_db)):
    """
    Creates a player
    :return: 201
    """
    player = models.Player()
    player.first_name = player_request.first_name
    player.last_name = player_request.last_name
    player.date_of_birth = player_request.date_of_birth
    player.active = True

    db.add(player)
    db.commit()

    background_tasks.add_task(do_some_heavy_lifting, player.first_name)

    return {
        "code": "success"
    }
