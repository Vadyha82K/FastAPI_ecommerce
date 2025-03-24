from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.backend.db_depends import get_db
from app.models import Review, Product
from app.routers.auth import get_current_user
from app.schemas import CreateReview

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/")
async def all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.is_active == True))

    if reviews is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no comments"
        )
    return reviews.all()


@router.get("/{product_id}")
async def products_reviews(
        db: Annotated[AsyncSession, Depends(get_db)],
        product_id: int
):
    product = await db.scalar(select(Product).where(
        Product.id == product_id,
        Product.is_active == True
    ))

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    comments = await db.scalars(select(Review).where(Review.product_id == product_id, Review.is_active == True))
    if comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No comments"
        )
    return comments.all()


@router.post("/")
async def add_review(
        db: Annotated[AsyncSession, Depends(get_db)],
        create_review: CreateReview,
        get_user: Annotated[dict, Depends(get_current_user)]
):
    product = await db.scalar(select(Product).where(
        Product.id == create_review.product_id,
        Product.is_active == True
    ))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if get_user:
        await db.execute(insert(Review).values(
            comment = create_review.comment,
            product_id = create_review.product_id,
            user_id = get_user["id"],
            grade = create_review.grade
        ))
        await db.commit()

        product_reviews = await db.scalars(select(Review).where(Review.product_id == create_review.product_id))
        product_rating = list(review.grade for review in product_reviews)
        product.rating = sum(product_rating) / len(product_rating)
        await db.commit()

        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": "Successful"
        }

@router.delete("/")
async def delete_reviews(
        db: Annotated[AsyncSession, Depends(get_db)],
        review_id: int,
        product_id: int,
        get_user: Annotated[dict, Depends(get_current_user)]
):
    review = await db.scalar(select(Review).where(review_id == Review.id, product_id == Review.product_id))
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or review not found"
        )
    if get_user.get("is_admin"):
        review.is_active = False
        await db.commit()

        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Review delete is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You have not enough permission for this action'
        )
