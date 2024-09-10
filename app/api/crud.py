from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import desc, func
from sqlalchemy.orm import Session, joinedload
from app.db.models import Post, Comment, Team, Emotion, EmotionType, PostViewLog
from app.schemas import post as post_schema
from app.schemas import comment as comment_schema
from app.schemas import emotion as emotion_schema


def create_post(db: Session, post: post_schema.PostCreate, user_id: int):
    db_post = Post(title=post.title, content=post.content, author_id=user_id)

    if post.team_ids:
        for team_id in post.team_ids:
            team = db.query(Team).filter(Team.id == team_id).first()
            if team:
                db_post.teams.append(team)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Post)
        .options(joinedload(Post.author))
        .order_by(Post.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_post(db: Session, post_id: int):
    post = (
        db.query(Post)
        .options(joinedload(Post.teams))
        .filter(Post.id == post_id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


def increment_post_views(db: Session, post: Post):
    post.views += 1
    db.add(PostViewLog(post_id=post.id))
    db.commit()
    db.refresh(post)
    return post


def get_popular_posts(db: Session):
    one_minute_ago = datetime.utcnow() - timedelta(minutes=60)
    popular_posts = (
        db.query(Post, func.count(PostViewLog.id).label("recent_views"))
        .join(PostViewLog)
        .filter(PostViewLog.viewed_at >= one_minute_ago)
        .group_by(Post.id)
        .order_by(func.count(PostViewLog.id).desc())
        .limit(5)
        .all()
    )
    return [
        post_schema.PostViewLog(
            post_id=post.id,
            title=post.title,
            content=post.content,
            recent_views=recent_views,
        )
        for post, recent_views in popular_posts
    ]


# 게시글 수정
def update_post(db: Session, post_id: int, post_update: post_schema.PostUpdate):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    for key, value in post_update.dict(exclude_unset=True).items():
        setattr(post, key, value)

    if post_update.team_ids is not None:
        post.teams.clear()

        for team_id in post_update.team_ids:
            team = db.query(Team).filter(Team.id == team_id).first()
            if team:
                post.teams.append(team)

    db.commit()
    db.refresh(post)
    return post


# 게시글 삭제
def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}


def create_comment(
    db: Session, comment: comment_schema.CommentCreate, user_id: int, post_id: int
):
    db_comment = Comment(message=comment.message, author_id=user_id, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments(db: Session, post_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .options(joinedload(Comment.author))
        .order_by(desc(Comment.id))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_teams(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Team).offset(skip).limit(limit).all()


def get_posts_by_team(db: Session, team_id: int):
    return (
        db.query(Post)
        .options(joinedload(Post.author), joinedload(Post.teams))
        .join(Post.teams)
        .filter(Team.id == team_id)
        .order_by(Post.id.desc())
        .all()
    )


def get_emotion_types(db: Session, skip: int = 0):
    return db.query(EmotionType).offset(skip).all()


def get_emotion_counts_by_post(db: Session, post_id: int):
    counts = (
        db.query(Emotion.emotion_type_id, func.count(Emotion.id).label("count"))
        .filter(Emotion.post_id == post_id)
        .group_by(Emotion.emotion_type_id)
        .all()
    )
    return [
        emotion_schema.EmotionResponse(
            emotion_type_id=count.emotion_type_id, count=count.count
        )
        for count in counts
    ]


def get_user_emotion_status(db: Session, user_id: Optional[int], post_id: int):
    if user_id is None:
        return []
    emotions = (
        db.query(Emotion)
        .filter(Emotion.user_id == user_id, Emotion.post_id == post_id)
        .all()
    )
    if not emotions:
        return []
    return [
        emotion_schema.UserEmotionStatus(
            emotion_type_id=emotion.emotion_type_id, voted=True
        )
        for emotion in emotions
    ]


def toggle_emotion(db: Session, user_id: int, post_id: int, emotion_type_id: int):
    emotion = (
        db.query(Emotion)
        .filter(
            Emotion.user_id == user_id,
            Emotion.post_id == post_id,
            Emotion.emotion_type_id == emotion_type_id,
        )
        .first()
    )

    if emotion:
        db.delete(emotion)
        db.commit()
        return {"action": "deleted"}
    else:
        new_emotion = Emotion(
            user_id=user_id, post_id=post_id, emotion_type_id=emotion_type_id
        )
        db.add(new_emotion)
        db.commit()
        db.refresh(new_emotion)
        return {"action": "added"}
