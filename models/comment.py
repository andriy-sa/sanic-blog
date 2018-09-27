from app import db
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func


class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, primary_key=True)
    text = Column(Text(), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
