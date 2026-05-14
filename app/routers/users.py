from fastapi import APIRouter,HTTPException,status,Depends
from app.models.schemas import UserCreate,UserResponse
from app.utils.hashing import hash_password
from app.database import get_db
from typing import List
import uuid
from sqlalchemy.orm import Session
from app.models.models import User
router = APIRouter(
    prefix = "/users",
    tags=["Users"]

)

#CREATING USER
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user:UserCreate, db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "User with this email already exists"
        )
    new_user = User (
        user_id = str(uuid.uuid4()),
        name = user.name,
        email = user.email,
        password = hash_password(user.password))
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
#get all users
@router.get("/",response_model=List[UserResponse])
def get_users(db:Session = Depends(get_db)):
    return db.query(User).all()
#get user by id
@router.get("/{user_id}",response_model=UserResponse)
def get_user_by_id(user_id:str,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    return user
#Update user
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id:str,name:str=None,email:str=None,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="usernot found")
    if name:
        user.name = name
    if email:
        user.email=email
    db.commit()
    db.refresh(user)
    return user
#delete user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(user_id:str,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not founf"
        )
    db.delete(user)
    db.commit()
    return