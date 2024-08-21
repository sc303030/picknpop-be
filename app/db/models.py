# models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from .database import Base


class TimestampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class EmotionType(Base, TimestampMixin):
    __tablename__ = "posts_emotiontype"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(Text, nullable=True)

    def __str__(self):
        return self.name


class User(Base):
    __tablename__ = "accounts_user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    nickname = Column(String, unique=True, index=True)
    avatar = Column(String, nullable=True)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    emotions = relationship("Emotion", back_populates="user")


class Emotion(Base, TimestampMixin):
    __tablename__ = "posts_emotion"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("accounts_user.id"))
    post_id = Column(Integer, ForeignKey("posts_post.id"))
    emotion_type_id = Column(Integer, ForeignKey("posts_emotiontype.id"))

    user = relationship("User", back_populates="emotions")
    post = relationship("Post", back_populates="emotions")
    emotion_type = relationship("EmotionType")
    __table_args__ = (
        UniqueConstraint(
            "user_id", "post_id", "emotion_type_id", name="unique_user_post_emotion"
        ),
    )


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
    emotions = relationship("Emotion", back_populates="post")


class Comment(Base, TimestampMixin):
    __tablename__ = "posts_comment"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("accounts_user.id"))
    post_id = Column(Integer, ForeignKey("posts_post.id"))
    message = Column(Text)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
