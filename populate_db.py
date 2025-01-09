from sqlalchemy.orm import Session
from database import SessionLocal
from models import Sport, Athlete, Result
from faker import Faker
import random
import logging

faker = Faker()

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sports(session: Session, n=10):
    """Create a batch of sports."""
    logger.info("Creating sports...")
    sports_list = ["100m Dash", "Long Jump", "High Jump", "Shot Put", "Pole Vault",
                   "400m Hurdles", "Javelin Throw", "Discus Throw", "Marathon", "Decathlon"]
    for _ in range(n):
        sport = Sport(
            name=faker.unique.word() if n > len(sports_list) else sports_list.pop(),
            unit=random.choice(["seconds", "meters", "kilograms"]),
            world_record=round(random.uniform(5, 100), 2),
            olympic_record=round(random.uniform(5, 100), 2),
        )
        session.add(sport)
    session.commit()
    logger.info("Sports created successfully!")

def get_sport_ids(session: Session):
    """Fetch sport IDs."""
    logger.info("Fetching sport IDs...")
    return [sport.id for sport in session.query(Sport).all()]

def create_athletes(session: Session, n=50):
    """Create a batch of athletes."""
    logger.info("Creating athletes...")
    for _ in range(n):
        athlete = Athlete(
            full_name=faker.name(),
            country=faker.country(),
            birth_year=random.randint(1960, 2005),
            victories=random.randint(0, 20),
        )
        session.add(athlete)
    session.commit()
    logger.info("Athletes created successfully!")

def get_athlete_ids(session: Session):
    """Fetch athlete IDs."""
    logger.info("Fetching athlete IDs...")
    return [athlete.id for athlete in session.query(Athlete).all()]

def create_results(session: Session, sport_ids, athlete_ids, n=100):
    """Create a batch of results."""
    if not sport_ids or not athlete_ids:
        logger.warning("No sports or athletes found. Skipping result creation.")
        return

    logger.info("Creating results...")
    for _ in range(n):
        result = Result(
            competition_name=faker.sentence(nb_words=3).replace(".", ""),
            performance=round(random.uniform(5, 100), 2),
            event_date=faker.date_this_century().isoformat(),
            location=faker.city(),
            sport_id=random.choice(sport_ids),
            athlete_id=random.choice(athlete_ids),
            additional_info={
                "weather": random.choice(["Sunny", "Rainy", "Windy"]),
                "audience_size": random.randint(1000, 50000),
            },
        )
        session.add(result)
    session.commit()
    logger.info("Results created successfully!")

def populate_database():
    """Main function to populate the database."""
    logger.info("Starting database population...")
    session = SessionLocal()

    try:
        # Create sports
        create_sports(session, 10)
        sport_ids = get_sport_ids(session)
        if not sport_ids:
            logger.error("No sports created. Aborting!")
            return

        # Create athletes
        create_athletes(session, 50)
        athlete_ids = get_athlete_ids(session)
        if not athlete_ids:
            logger.error("No athletes created. Aborting!")
            return

        # Create results
        create_results(session, sport_ids, athlete_ids, 100)

        logger.info("Database population complete!")
    finally:
        session.close()

if __name__ == "__main__":
    populate_database()
