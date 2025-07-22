from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.api.v1.schemas.post import PostCreate, PostRead, PostUpdate
from app.services import post_service
from app.db.database import get_db
from app.db.models.user import User
from app.dependencies import get_current_user, require_permission

post_router = APIRouter(prefix="/posts", tags=["Posts"])

@post_router.get("/", response_model=List[PostRead])
def get_all_posts(db: Session = Depends(get_db), 
                  _: bool = Depends(require_permission("post:read"))):
    return post_service.get_posts(db)

@post_router.post("/", response_model=PostRead)
def create_post(data: PostCreate,
                db: Session = Depends(get_db),
                user: User = Depends(get_current_user),
                _: bool = Depends(require_permission("post:create"))):
    return post_service.create_post(db, user, data)

@post_router.put("/{id}/", response_model=PostRead)
def update_post(id: UUID, 
                data: PostUpdate,
                db: Session = Depends(get_db),
                _: bool = Depends(require_permission("post:update"))):
    return post_service.update_post(db, id, data)

@post_router.delete("/{id}/")
def delete_post(id: UUID,
                db: Session = Depends(get_db),
                _: bool = Depends(require_permission("post:delete"))):
    post_service.delete_post(db, id)
    return {"message": "Post deleted"}
