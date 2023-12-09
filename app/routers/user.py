from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """This function is for creating the new user

    Arguments:
        user (UserCreate) -- Get user from request.
        db (Session, optional): _database session_. Defaults to Depends(get_db).

    Returns:
        _type_: UserOut
    """
    # Hash the password - user.password
    hashed_password = utils.hase(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    """This function is for get user details

    Args:
        id (int): _user_id_
        db (Session, optional): _database session_. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 Not Found

    Returns:
        _type_: UserOut
    """
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exits")

    return user
