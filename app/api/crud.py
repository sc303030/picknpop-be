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
    total_posts = db.query(Post).count()

    comment_count_subquery = (
        db.query(Comment.post_id, func.count(Comment.id).label("comment_count"))
        .group_by(Comment.post_id)
        .subquery()
    )

    emotion_count_subquery = (
        db.query(Emotion.post_id, func.count(Emotion.id).label("emotion_count"))
        .group_by(Emotion.post_id)
        .subquery()
    )

    # 실제 게시물 쿼리
    posts = (
        db.query(
            Post,
            func.coalesce(comment_count_subquery.c.comment_count, 0).label(
                "comment_count"
            ),
            func.coalesce(emotion_count_subquery.c.emotion_count, 0).label(
                "emotion_count"
            ),
        )
        .outerjoin(comment_count_subquery, Post.id == comment_count_subquery.c.post_id)
        .outerjoin(emotion_count_subquery, Post.id == emotion_count_subquery.c.post_id)
        .options(joinedload(Post.author))
        .order_by(Post.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total_count": total_posts,
        "posts": [
            post_schema.PostMain(
                id=post.id,
                title=post.title,
                content=post.content,
                author=post.author,
                created_at=post.created_at,
                updated_at=post.updated_at,
                views=post.views,
                comment_count=comment_count,
                emotion_count=emotion_count,
            )
            for post, comment_count, emotion_count in posts
        ],
    }


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
    one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
    popular_posts = (
        db.query(Post, func.count(PostViewLog.id).label("recent_views"))
        .outerjoin(
            PostViewLog,
            (Post.id == PostViewLog.post_id)
            & (PostViewLog.viewed_at >= one_minute_ago),
        )
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
def update_post(
    db: Session, post_id: int, post_update: post_schema.PostUpdate, user_id: int
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != user_id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to delete this comment"
        )

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
def delete_post(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != user_id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to delete this comment"
        )
    db.delete(post)
    db.commit()
    return {"message": "Post marked as deleted successfully"}


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


def delete_comment(db: Session, comment_id: int, current_user_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.author_id != current_user_id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to delete this comment"
        )

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted successfully"}


def get_teams(db: Session, skip: int = 0):
    return db.query(Team).offset(skip).all()


def get_posts_by_team(db: Session, team_id: int, skip: int = 0, limit: int = 10):
    total_posts = db.query(Post).join(Post.teams).filter(Team.id == team_id).count()
    comment_count_subquery = (
        db.query(Comment.post_id, func.count(Comment.id).label("comment_count"))
        .group_by(Comment.post_id)
        .subquery()
    )

    emotion_count_subquery = (
        db.query(Emotion.post_id, func.count(Emotion.id).label("emotion_count"))
        .group_by(Emotion.post_id)
        .subquery()
    )

    posts = (
        db.query(
            Post,
            func.coalesce(comment_count_subquery.c.comment_count, 0).label(
                "comment_count"
            ),
            func.coalesce(emotion_count_subquery.c.emotion_count, 0).label(
                "emotion_count"
            ),
        )
        .outerjoin(comment_count_subquery, Post.id == comment_count_subquery.c.post_id)
        .outerjoin(emotion_count_subquery, Post.id == emotion_count_subquery.c.post_id)
        .options(joinedload(Post.author), joinedload(Post.teams))
        .join(Post.teams)
        .filter(Team.id == team_id)
        .order_by(Post.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total_count": total_posts,
        "posts": [
            post_schema.PostMain(
                id=post.id,
                title=post.title,
                content=post.content,
                author=post.author,
                created_at=post.created_at,
                updated_at=post.updated_at,
                views=post.views,
                comment_count=comment_count,
                emotion_count=emotion_count,
            )
            for post, comment_count, emotion_count in posts
        ],
    }


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
