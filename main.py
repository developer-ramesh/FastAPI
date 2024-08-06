from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from models import async_session
import crud
import schemas

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "Welcome to the FastAPI application"}

# Dependency to get the database session
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

@app.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_user = await crud.create_user(db, name=user.name, email=user.email)
        return db_user
    except SQLAlchemyError as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user")

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_user = await crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return db_user
    except SQLAlchemyError as e:
        logger.error(f"Error reading user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error reading user")



if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)