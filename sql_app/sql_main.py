from typing import List
import uvicorn


from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=List[schemas.InferenceResult])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_inference_results(db, skip=skip, limit=limit)
    return users

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=6006 , reload=True, debug=False)
