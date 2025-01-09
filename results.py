from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter()

# Create a new result
@router.post("/", response_model=schemas.Result)
def create_result(result: schemas.ResultCreate, db: Session = Depends(get_db)):
    return crud.create_result(db=db, result=result)

# Get a single result by ID
@router.get("/{result_id}", response_model=schemas.Result)
def read_result(result_id: int, db: Session = Depends(get_db)):
    db_result = crud.get_result(db=db, result_id=result_id)
    if not db_result:
        raise HTTPException(status_code=404, detail="Result not found")
    return db_result

# Update an existing result
@router.put("/{result_id}", response_model=schemas.Result)
def update_result(result_id: int, result: schemas.ResultCreate, db: Session = Depends(get_db)):
    db_result = crud.update_result(db=db, result_id=result_id, result=result)
    if not db_result:
        raise HTTPException(status_code=404, detail="Result not found")
    return db_result

# Delete a result
@router.delete("/{result_id}", status_code=204)
def delete_result(result_id: int, db: Session = Depends(get_db)):
    if not crud.delete_result(db=db, result_id=result_id):
        raise HTTPException(status_code=404, detail="Result not found")
    return {"detail": "Result deleted successfully"}

# Filter results with optional conditions
@router.get("/filter", response_model=list[schemas.Result])
def filter_results(
    athlete_id: int = None,
    sport_id: int = None,
    score_gt: float = Query(None, alias="score[gt]"),
    score_lt: float = Query(None, alias="score[lt]"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.filter_results(
        db=db,
        athlete_id=athlete_id,
        sport_id=sport_id,
        score_gt=score_gt,
        score_lt=score_lt,
        skip=skip,
        limit=limit,
    )

# GROUP BY example: Count results by sport
@router.get("/grouped_by_sport", response_model=list[dict])
def group_results_by_sport(db: Session = Depends(get_db)):
    return crud.group_results_by_sport(db=db)

# Sorting results
@router.get("/sorted", response_model=list[schemas.Result])
def get_sorted_results(
    order_by: str = "score",
    descending: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_sorted_results(
        db=db,
        order_by=order_by,
        descending=descending,
        skip=skip,
        limit=limit,
    )
