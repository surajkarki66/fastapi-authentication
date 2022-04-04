from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends, Response


from app.models import User
from app.config import settings
from app.database import get_db
from app.utils import hash, verify
from app.helpers.jwt_handler import signJWT
from app.helpers.jwt_bearer import JWTBearer
from app.schemas import UserLoginSchema, UserSchema, UserCreateSchema,\
    TokenSchema, UserUpdateSchema, PasswordUpdateSchema

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED,
             response_model=UserSchema)
def user_signup(user: UserCreateSchema, db: Session = Depends(get_db)) -> dict:
    check_user = db.query(User).filter(User.email == user.email).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with email already exist")
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=TokenSchema)
def user_login(response: Response, user: UserLoginSchema, db: Session = Depends(get_db)) -> dict:
    check_user = db.query(User).filter(
        User.email == user.email).first()

    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect email")

    if not verify(user.password, check_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")

    access_token = signJWT(check_user.id, settings.jwt_expire_seconds)
    response.set_cookie(key="access_token",
                        value=f"{access_token}", expires=settings.jwt_expire_seconds, httponly=True, secure=True)

    return {"access_token": access_token}


@router.get('/get', response_model=List[UserSchema],
            dependencies=[Depends(JWTBearer())])
def get_users(db: Session = Depends(get_db), limit: int = 10,
              skip: int = 0) -> List[dict]:
    users = db.query(User).limit(limit).offset(skip).all()
    return users


@router.get('/{id}', response_model=UserSchema,
            dependencies=[Depends(JWTBearer())])
def get_one_user(id: int, db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(JWTBearer())) -> dict:

    user_query = db.query(User).filter(User.id == id)

    user = user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")

    if id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested \
                                action")

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{id}", response_model=UserSchema)
def update_user(id: int, updated_post: UserUpdateSchema,
                db: Session = Depends(get_db),
                current_user: dict = Depends(JWTBearer())):

    user_query = db.query(User).filter(User.id == id)

    user = user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")

    if id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested\
                                action")

    user_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return user_query.first()


@router.patch("/change_password/{id}", response_model=UserSchema)
def change_password(id: int, updated_user: PasswordUpdateSchema,
                    db: Session = Depends(get_db),
                    current_user: dict = Depends(JWTBearer())):

    user_query = db.query(User).filter(User.id == id)

    user = user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")

    if id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested\
                                 action")

    if not verify(updated_user.old_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")

    hashed_password = hash(updated_user.password)
    updated_user.password = hashed_password
    updated_user = updated_user.dict()
    updated_user.pop("old_password")
    user_query.update(updated_user, synchronize_session=False)

    db.commit()

    return user_query.first()
