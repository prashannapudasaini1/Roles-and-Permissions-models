from app.db.database import SessionLocal
from app.db.models.posts.post import Permission  # Your Permission model

DEFAULT_PERMISSIONS = [
    "post:create",
    "post:read",
    "post:update",
    "post:delete"
]

def seed_permissions():
    db = SessionLocal()
    try:
        for perm_name in DEFAULT_PERMISSIONS:
            exists = db.query(Permission).filter_by(name=perm_name).first()
            if not exists:
                db.add(Permission(name=perm_name))
        db.commit()
    finally:
        db.close()
