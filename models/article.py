from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base as Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Article(Base()):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, primary_key=True)
    description = Column(Text(), nullable=True)
    is_published = Column(Boolean(), default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    comments = relationship("Comment")
