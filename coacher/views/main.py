from fastapi import Request, Depends, BackgroundTasks, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from coacher import app, templates
from coacher.database import SessionLocal
from coacher.models import Guardian, Player


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class PlayerRequest(BaseModel):
    """
    """
    first_name: str
    last_name: str
    date_of_birth: str

    # class Config:
    #     orm_mode = True


class GuardianRequest(BaseModel):
    """
    """
    first_name: str
    last_name: str


@app.get("/player", tags=["player"])
async def get_players(db: Session = Depends(get_db)):
    players = db.query(Player).all()
    return players


@app.get("/player/{player_id}", tags=["player"])
async def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    return player


@app.post("/player", tags=["player"])
async def create_player(player_request: PlayerRequest,
                        background_tasks: BackgroundTasks,
                        db: Session = Depends(get_db)):
    """
    Creates a player
    :return: 201
    """
    player = Player()
    player.first_name = player_request.first_name
    player.last_name = player_request.last_name
    player.date_of_birth = player_request.date_of_birth

    db.add(player)
    db.commit()

    background_tasks.add_task(_do_some_heavy_lifting, player.first_name)

    return {
        "code": "success"
    }


@app.put("/player/{player_id}", tags=["player"], status_code=status.HTTP_202_ACCEPTED)
async def update_player(player_id: int, request: PlayerRequest, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id)
    if not player.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Player with id: {player_id} not found")

    player.update(request.dict())  # Why do I need to specify a dict here?
    db.commit()
    return "updated"


@app.delete("/player/{player_id}", tags=["player"])
async def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).delete()
    db.commit()
    return {"message": "Player deleted successfully"}


@app.get("/guardian", tags=["guardian"])
async def get_guardians(db: Session = Depends(get_db)):
    guardians = db.query(Guardian).all()
    return guardians


@app.get("/guardian/{guardian_id}", tags=["guardian"])
async def get_guardian(guardian_id: int, db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(Guardian.id == guardian_id).first()
    return guardian


@app.post("/guardian", tags=["guardian"])
async def create_guardian(guardian_request: GuardianRequest, db: Session = Depends(get_db)):
    """
    Creates a guardian
    :return: 201
    """
    guardian = Guardian()
    guardian.first_name = guardian_request.first_name
    guardian.last_name = guardian_request.last_name

    db.add(guardian)
    db.commit()

    return {
        "code": "success"
    }


@app.put("/guardian/{guardian_id}", tags=["guardian"])
async def update_guardian():
    pass


@app.delete("/guardian/{guardian_id}", tags=["guardian"])
async def delete_guardian():
    pass


@app.get("/", tags=["frontend"])
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
    else:
        players = players.filter(Player.active.is_(False))

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "players": players,
        "first_name": first_name,
        "active": active
    })


@app.get("/guardians", tags=["frontend"])
def guardians(request: Request, db: Session = Depends(get_db)):
    """
        TODO: Add filtering support as per player page
    """
    guardians = db.query(Guardian).all()

    return templates.TemplateResponse("guardians.html", {
        "request": request,
        "guardians": guardians
    })


def _do_some_heavy_lifting(first_name: str):
    db = SessionLocal()

    player = db.query(Player).filter(Player.first_name == first_name).first()
    player.date_of_birth = "01-01-2021"

    db.add(player)
    db.commit()
