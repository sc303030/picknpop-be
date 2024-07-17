# models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base


class TimestampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "accounts_user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    nickname = Column(String, unique=True, index=True)
    avatar = Column(String, nullable=True)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")


class Team(Base, TimestampMixin):
    __tablename__ = "posts_team"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    league = Column(String, index=True)
    emblem = Column(String, nullable=True)
    posts = relationship("Post", back_populates="teams")


class Post(Base, TimestampMixin):
    __tablename__ = "posts_post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("accounts_user.id"))
    team_id = Column(Integer, ForeignKey("posts_team.id"))

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    teams = relationship("Team", back_populates="posts")


class Comment(Base, TimestampMixin):
    __tablename__ = "posts_comment"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("accounts_user.id"))
    post_id = Column(Integer, ForeignKey("posts_post.id"))
    message = Column(Text)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
