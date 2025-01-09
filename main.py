from fastapi import FastAPI
from sqlalchemy.orm import Session
from routers import athletes, results, sports  # Import the respective routers
from database import engine, get_db  # Import engine and get_db
import models
import uvicorn

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI(
    title="Sports API",
    description="A simple REST API for managing sports, athletes, and results.",
    version="1.0.0",
)

# Include the routers for sports, athletes, and results
app.include_router(sports.router, prefix="/sports", tags=["Sports"])
app.include_router(athletes.router, prefix="/athletes", tags=["Athletes"])
app.include_router(results.router, prefix="/results", tags=["Results"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Sports API!"}

if __name__ == "__main__":
    # Run the FastAPI app using uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
