from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter()

# Create a new athlete
@router.post("/athletes/", response_model=schemas.AthleteResponse)
def create_athlete(athlete: schemas.AthleteCreate, db: Session = Depends(get_db)):
    return crud.create_athlete(db=db, athlete=athlete)


# Get a single athlete by ID
@router.get("/{athlete_id}", response_model=schemas.Athlete)
def read_athlete(athlete_id: int, db: Session = Depends(get_db)):
    db_athlete = crud.get_athlete(db=db, athlete_id=athlete_id)
    if not db_athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return db_athlete

@router.get("/athletes/", response_model=list[schemas.AthleteResponse])
def read_athletes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")
    return crud.get_athletes(db=db, skip=skip, limit=limit)

# Delete an athlete
@router.delete("/{athlete_id}", status_code=204)
def delete_athlete(athlete_id: int, db: Session = Depends(get_db)):
    if not crud.delete_athlete(db=db, athlete_id=athlete_id):
        raise HTTPException(status_code=404, detail="Athlete not found")
    return {"detail": "Athlete deleted successfully"}

# Filter athletes with optional criteria
@router.get("/filter", response_model=list[schemas.Athlete])
def filter_athletes(
    name: str = None,
    country: str = None,
    age_gt: int = Query(None, alias="age[gt]"),
    age_lt: int = Query(None, alias="age[lt]"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.filter_athletes(
        db=db,
        name=name,
        country=country,
        age_gt=age_gt,
        age_lt=age_lt,
        skip=skip,
        limit=limit,
    )

# JOIN example: Get athletes with their results
@router.get("/detailed", response_model=list[dict])
def get_athletes_with_results(db: Session = Depends(get_db)):
    return crud.get_athletes_with_results(db=db)

# GROUP BY example: Count athletes by country
@router.get("/grouped_by_country", response_model=list[dict])
def group_athletes_by_country(db: Session = Depends(get_db)):
    return crud.group_athletes_by_country(db=db)

# Sorting athletes
@router.get("/sorted", response_model=list[schemas.Athlete])
def get_sorted_athletes(
    order_by: str = "name",
    descending: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_sorted_athletes(
        db=db,
        order_by=order_by,
        descending=descending,
        skip=skip,
        limit=limit,
    )
