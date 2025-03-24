from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func, Boolean

from app.backend.db import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    comment = Column(String, nullable=True)
    comment_date = Column(DateTime, default=func.current_timestamp())
    grade = Column(Integer)
    is_active = Column(Boolean, default=True)