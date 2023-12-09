from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = "",
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_post(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {user_id} was not found")
    return post


@router.put("/{id}", response_model=schemas.PostCreate)
def update_post(
        user_id: int,
        updated_post: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == user_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{user_id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
        post: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == user_id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{user_id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
