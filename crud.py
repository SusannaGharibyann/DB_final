from models import Sport
from schemas import SportCreate
from models import Result
from schemas import ResultCreate
from sqlalchemy.orm import Session
from models import Athlete
from schemas import AthleteCreate
from sqlalchemy import func, desc


# Create a new sport
def create_sport(db: Session, sport: SportCreate):
    db_sport = Sport(name=sport.name, popularity=sport.popularity, unit=sport.unit)
    db.add(db_sport)
    db.commit()
    db.refresh(db_sport)
    return db_sport

# Get a single sport by ID
def get_sport(db: Session, sport_id: int):
    return db.query(Sport).filter(Sport.id == sport_id).first()

# Update a sport
def update_sport(db: Session, sport_id: int, sport: SportCreate):
    db_sport = db.query(Sport).filter(Sport.id == sport_id).first()
    if db_sport:
        db_sport.name = sport.name
        db_sport.popularity = sport.popularity
        db_sport.unit = sport.unit
        db.commit()
        db.refresh(db_sport)
    return db_sport

# Delete a sport
def delete_sport(db: Session, sport_id: int):
    db_sport = db.query(Sport).filter(Sport.id == sport_id).first()
    if db_sport:
        db.delete(db_sport)
        db.commit()
        return True
    return False

# Filter sports with optional criteria
def filter_sports(db: Session, name: str = None, world_record_gt: float = None, world_record_lt: float = None, skip: int = 0, limit: int = 100):
    query = db.query(Sport)
    if name:
        query = query.filter(Sport.name.ilike(f"%{name}%"))
    if world_record_gt:
        query = query.filter(Sport.world_record > world_record_gt)
    if world_record_lt:
        query = query.filter(Sport.world_record < world_record_lt)
    return query.offset(skip).limit(limit).all()

# JOIN example: Get sports with the number of results
def get_sports_with_result_counts(db: Session):
    return db.query(Sport.name, func.count().label("result_count")).join(Sport.results).group_by(Sport.name).all()

# Update a world record for a sport
def update_world_record(db: Session, sport_name: str, new_record: float):
    sport = db.query(Sport).filter(Sport.name == sport_name).first()
    if sport:
        sport.world_record = new_record
        db.commit()
        return True
    return False

# Group sports by unit
def group_sports_by_unit(db: Session):
    return db.query(Sport.unit, func.count().label("count")).group_by(Sport.unit).all()

# Get sorted sports
def get_sorted_sports(db: Session, order_by: str, descending: bool, skip: int, limit: int):
    order_column = getattr(Sport, order_by, Sport.name)
    if descending:
        order_column = desc(order_column)
    return db.query(Sport).order_by(order_column).offset(skip).limit(limit).all()


# Create a new athlete
def create_athlete(db: Session, athlete: AthleteCreate):
    db_athlete = Athlete(name=athlete.name, age=athlete.age, country=athlete.country, sport_id=athlete.sport_id)
    db.add(db_athlete)
    db.commit()
    db.refresh(db_athlete)
    return db_athlete

# Get a single athlete by ID
def get_athlete(db: Session, athlete_id: int):
    return db.query(Athlete).filter(Athlete.id == athlete_id).first()

# Get a list of athletes with pagination
def get_athletes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Athlete).offset(skip).limit(limit).all()

# Update an athlete
def update_athlete(db: Session, athlete_id: int, athlete: AthleteCreate):
    db_athlete = db.query(Athlete).filter(Athlete.id == athlete_id).first()
    if db_athlete:
        db_athlete.name = athlete.name
        db_athlete.age = athlete.age
        db_athlete.country = athlete.country
        db_athlete.sport_id = athlete.sport_id
        db.commit()
        db.refresh(db_athlete)
    return db_athlete

# Delete an athlete
def delete_athlete(db: Session, athlete_id: int):
    db_athlete = db.query(Athlete).filter(Athlete.id == athlete_id).first()
    if db_athlete:
        db.delete(db_athlete)
        db.commit()
        return True
    return False

# Filter athletes with optional criteria
def filter_athletes(db: Session, name: str = None, sport: str = None, country: str = None, skip: int = 0, limit: int = 100):
    query = db.query(Athlete)
    if name:
        query = query.filter(Athlete.name.ilike(f"%{name}%"))
    if sport:
        query = query.join(Athlete.sport).filter(Sport.name.ilike(f"%{sport}%"))
    if country:
        query = query.filter(Athlete.country.ilike(f"%{country}%"))
    return query.offset(skip).limit(limit).all()

# Get athletes with detailed results (JOIN example)
def get_athletes_with_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Athlete.name, Athlete.country, func.count().label("result_count")).join(Athlete.results).group_by(Athlete.id).offset(skip).limit(limit).all()

# Get athletes sorted by a specific field
def get_sorted_athletes(db: Session, order_by: str, descending: bool, skip: int, limit: int):
    order_column = getattr(Athlete, order_by, Athlete.name)
    if descending:
        order_column = desc(order_column)
    return db.query(Athlete).order_by(order_column).offset(skip).limit(limit).all()
# Create a new result
def create_result(db: Session, result: ResultCreate):
    db_result = Result(athlete_id=result.athlete_id, sport_id=result.sport_id, score=result.score, date=result.date)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

# Get a single result by ID
def get_result(db: Session, result_id: int):
    return db.query(Result).filter(Result.id == result_id).first()

# Get a list of results with pagination
def get_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Result).offset(skip).limit(limit).all()

# Update a result
def update_result(db: Session, result_id: int, result: ResultCreate):
    db_result = db.query(Result).filter(Result.id == result_id).first()
    if db_result:
        db_result.score = result.score
        db_result.date = result.date
        db.commit()
        db.refresh(db_result)
    return db_result

# Delete a result
def delete_result(db: Session, result_id: int):
    db_result = db.query(Result).filter(Result.id == result_id).first()
    if db_result:
        db.delete(db_result)
        db.commit()
        return True
    return False

# Filter results with optional criteria (e.g., score, athlete, sport)
def filter_results(db: Session, athlete_id: int = None, sport_id: int = None, score_gt: float = None, score_lt: float = None, skip: int = 0, limit: int = 100):
    query = db.query(Result)
    if athlete_id:
        query = query.filter(Result.athlete_id == athlete_id)
    if sport_id:
        query = query.filter(Result.sport_id == sport_id)
    if score_gt:
        query = query.filter(Result.score > score_gt)
    if score_lt:
        query = query.filter(Result.score < score_lt)
    return query.offset(skip).limit(limit).all()

# Get results grouped by sport
def group_results_by_sport(db: Session):
    return db.query(Sport.name, func.count().label("result_count")).join(Result).group_by(Sport.name).all()

# Get the best score for each athlete
def get_best_scores_for_athletes(db: Session):
    return db.query(Result.athlete_id, func.max(Result.score).label("best_score")).group_by(Result.athlete_id).all()

