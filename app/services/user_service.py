# app/services/user_service.py
def create_user(db: Session, user_in: UserCreate) -> User:
    hashed = get_password_hash(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db, email, password):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
