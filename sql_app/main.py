from typing import List
import uvicorn


from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

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
def read_queries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_inference_results(db, skip=skip, limit=limit)
    return users

@app.post("/users",response_model=schemas.InferenceResult)
def create_user(inference_result:schemas.InferenceResultCreate, db: Session = Depends(get_db)):
    return crud.create_inference_result(db, inference_result=inference_result.dict())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=6006 , reload=True, debug=False)
