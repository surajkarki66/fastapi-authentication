from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List, Optional

from app.models import Post
from app.database import get_db
from app.schemas import PostSchema, PostCreateSchema
from app.helpers.jwt_bearer import JWTBearer


router = APIRouter()


@router.get("/get", response_model=List[PostSchema],
            dependencies=[Depends(JWTBearer())])
def get_posts(db: Session = Depends(get_db), limit: int = 10,
              skip: int = 0, search: Optional[str] = "") -> List[dict]:
    posts = db.query(Post).filter(Post.title.contains(
        search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}", response_model=PostSchema,
            dependencies=[Depends(JWTBearer())])
def get_one_post(id: int, db: Session = Depends(get_db)) -> dict:
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post


@router.post("/create", status_code=status.HTTP_201_CREATED,
             response_model=PostCreateSchema)
def add_post(post: PostCreateSchema, db: Session = Depends(get_db),
             current_user: dict = Depends(JWTBearer())) -> dict:
    new_post = Post(user_id=current_user["user_id"], **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(JWTBearer())) -> dict:

    post_query = db.query(Post).filter(Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.user_id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform \
                                requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostSchema)
def update_post(id: int, updated_post: PostCreateSchema,
                db: Session = Depends(get_db),
                current_user: dict = Depends(JWTBearer())):

    post_query = db.query(Post).filter(Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.user_id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested\
                                 action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
