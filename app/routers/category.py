from typing import Annotated
from sqlalchemy import insert
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends

from app.backend.db_depends import get_db
from app.models import Category
from app.schemas import CreateCategory

router = APIRouter(prefix="/categories", tags=["category"])


@router.get("/")
async def get_all_categories():
    pass


def slugify(name):
    pass


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(db: Annotated[Session, Depends(get_db)], create_category: CreateCategory):
    db.execute(insert(Category).values(name=create_category.name,
                                       parent_id=create_category.parent_id,
                                       slug=slugify(create_category.name)))
    db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful"
    }


@router.put("/")
async def update_category():
    pass


@router.delete("/")
async def delete_category():
    pass