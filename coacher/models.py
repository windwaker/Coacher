from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer

from .database import Base


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=False, nullable=False)
    last_name = Column(String, unique=False, nullable=False)
    active = Column(Boolean, unique=False)
    date_of_birth = Column(String, unique=False, nullable=False)
    # add relationship to multiple parents
    guardians = relationship('Guardian', back_populates='players')


class Guardian(Base):
    __tablename__ = 'guardians'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=False, nullable=False)
    last_name = Column(String, unique=False)
    mobile_number = Column(String, unique=True, nullable=False)
    # add relationship to multiple players
    player_id = Column(Integer, ForeignKey('players.id'))
    players = relationship('Player', back_populates='guardians')
