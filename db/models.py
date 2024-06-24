# models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts_post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    owner_id = Column(Integer, ForeignKey("accounts_user.id"))

    owner = relationship("User", back_populates="posts")


class User(Base):
    __tablename__ = "accounts_user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    nickname = Column(String, unique=True, index=True)
    avatar = Column(String, nullable=True)

    posts = relationship("Post", back_populates="owner")
