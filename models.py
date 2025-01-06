from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class Sport(Base):
    __tablename__ = "sports"  # Fix table name

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    unit = Column(String, nullable=False)
    world_record = Column(Float, nullable=True)
    olympic_record = Column(Float, nullable=True)

    results = relationship("Result", back_populates="sport")


class Athlete(Base):
    __tablename__ = "athletes"  # Fix table name

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=False)
    victories = Column(Integer, default=0)

    results = relationship("Result", back_populates="athlete")


class Result(Base):
    __tablename__ = "results"  # Fix table name

    id = Column(Integer, primary_key=True, index=True)
    competition_name = Column(String, nullable=False)
    performance = Column(Float, nullable=False)
    event_date = Column(String, nullable=False)
    location = Column(String, nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"))
    athlete_id = Column(Integer, ForeignKey("athletes.id"))
    additional_info = Column(JSON, default={})

    sport = relationship("Sport", back_populates="results")
    athlete = relationship("Athlete", back_populates="results")
