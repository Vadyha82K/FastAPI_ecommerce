from typing import Annotated

from fastapi import APIRouter, status, Depends
from passlib.context import CryptContext
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.models.user import User
from app.schemas import CreateUser

router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[AsyncSession, Depends(get_db)], create_user: CreateUser):
    await db.execute(insert(User).values(
        first_name= create_user.first_name,
        last_name=create_user.last_name,
        username=create_user.username,
        email=create_user.email,
        hashed_password=bcrypt_context.hash(create_user.password),
    ))
    await db.commit()

    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful",
    }