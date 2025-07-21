# app/api/v1/user_routes.py
@router.post("/users/", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_in)

@router.post("/login/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=token, token_type="bearer")
