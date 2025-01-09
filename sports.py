from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter()

# Create a new sport
@router.post("/", response_model=schemas.Sport)
def create_sport(sport: schemas.SportCreate, db: Session = Depends(get_db)):
    return crud.create_sport(db=db, sport=sport)

# Get a single sport by ID
@router.get("/{sport_id}", response_model=schemas.Sport)
def read_sport(sport_id: int, db: Session = Depends(get_db)):
    db_sport = crud.get_sport(db=db, sport_id=sport_id)
    if not db_sport:
        raise HTTPException(status_code=404, detail="Sport not found")
    return db_sport

# Update an existing sport
@router.put("/{sport_id}", response_model=schemas.Sport)
def update_sport(sport_id: int, sport: schemas.SportCreate, db: Session = Depends(get_db)):
    db_sport = crud.update_sport(db=db, sport_id=sport_id, sport=sport)
    if not db_sport:
        raise HTTPException(status_code=404, detail="Sport not found")
    return db_sport

# Delete a sport
@router.delete("/{sport_id}", status_code=204)
def delete_sport(sport_id: int, db: Session = Depends(get_db)):
    if not crud.delete_sport(db=db, sport_id=sport_id):
        raise HTTPException(status_code=404, detail="Sport not found")
    return {"detail": "Sport deleted successfully"}

# Filter sports with optional conditions
@router.get("/filter", response_model=list[schemas.Sport])
def filter_sports(
    name: str = None,
    world_record_gt: float = Query(None, alias="world_record[gt]"),
    world_record_lt: float = Query(None, alias="world_record[lt]"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.filter_sports(
        db=db,
        name=name,
        world_record_gt=world_record_gt,
        world_record_lt=world_record_lt,
        skip=skip,
        limit=limit,
    )

# JOIN example: Get sports with the number of results
@router.get("/detailed", response_model=list[dict])
def get_sports_with_result_counts(db: Session = Depends(get_db)):
    return crud.get_sports_with_result_counts(db=db)

# Update a world record for a sport
@router.put("/update_world_record")
def update_world_record(sport_name: str, new_record: float, db: Session = Depends(get_db)):
    if not crud.update_world_record(db=db, sport_name=sport_name, new_record=new_record):
        raise HTTPException(status_code=404, detail="Sport not found")
    return {"detail": "World record updated successfully"}

# GROUP BY example: Count sports by unit
@router.get("/grouped_by_unit", response_model=list[dict])
def group_sports_by_unit(db: Session = Depends(get_db)):
    return crud.group_sports_by_unit(db=db)

# Get sorted sports
@router.get("/sorted", response_model=list[schemas.Sport])
def get_sorted_sports(
    order_by: str = "name",
    descending: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_sorted_sports(
        db=db,
        order_by=order_by,
        descending=descending,
        skip=skip,
        limit=limit,
    )
