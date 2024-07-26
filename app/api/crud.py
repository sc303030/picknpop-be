from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from app.db.models import Post, Comment, Team
from app.schemas import post as post_schema
from app.schemas import comment as comment_schema


def create_post(db: Session, post: post_schema.PostCreate, user_id: int):
    db_post = Post(
        title=post.title, content=post.content, team_id=post.team_id, author_id=user_id
    )
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
    return db.query(Post).filter(Post.id == post_id).first()


def update_post(db: Session, post_id: int, post: post_schema.PostUpdate):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db_post.title = post.title
        db_post.content = post.content
        db.commit()
        db.refresh(db_post)
        return db_post
    return None


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
        .options(joinedload(Post.author))
        .order_by(Post.id.desc())
        .filter(Post.team_id == team_id)
        .all()
    )
