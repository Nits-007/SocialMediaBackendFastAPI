from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db

router = APIRouter()  #Creating an instance of APIRouter() class to manage our routes in different files

#User Login Signup

#replace app.post with router.post as we dont have access to app and here router will do the same work 
@router.post("/users" , status_code=status.HTTP_201_CREATED , response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)) :
    hashed_password = utils.hash(user.password) #Converting password into hash code
    user.password = hashed_password
    new_user = models.User(email=user.email,password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}" , response_model=schemas.UserResponse)
async def get_user(id : int , db : Session=Depends(get_db)) :
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exist")
    return user 
    

