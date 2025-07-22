from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import List, Optional
from fastapi import FastAPI
from app.db.database import Base , engine

from app.db.models.posts.post import Post
from app.api.v1.schemas.post import PostCreate, PostUpdate
from app.api.v1.post_routes import post_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(post_router)


def create_post(db: Session, user, data: PostCreate) -> Post:
    try:
        new_post = Post(title=data.title, content=data.content, owner_id=user.id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        print(f"Error creating post: {e}")
        raise

#get
def get_posts(db: Session, skip: int = 0, limit: int = 10) -> List[Post]:
    return db.query(Post).offset(skip).limit(limit).all()


# Update 
def update_post(db: Session, post_id: UUID, data: PostUpdate) -> Optional[Post]:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None

    # Only update if data is provided
    if data.title:
        post.title = data.title
    if data.content:
        post.content = data.content

    db.commit()
    db.refresh(post)
    return post


# Delete
def delete_post(db: Session, post_id: UUID) -> None:
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
