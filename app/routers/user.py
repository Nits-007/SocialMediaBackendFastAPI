# # from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
# # from sqlalchemy.orm import Session

# # from app import models, schemas, utils
# # from app.database import get_db

# # router = APIRouter()  #Creating an instance of APIRouter() class to manage our routes in different files

# # #User Login Signup

# # #replace app.post with router.post as we dont have access to app and here router will do the same work 
# # @router.post("/users" , status_code=status.HTTP_201_CREATED , response_model=schemas.UserResponse)
# # async def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)) :
# #     hashed_password = utils.hash(user.password) #Converting password into hash code
# #     user.password = hashed_password
# #     new_user = models.User(email=user.email,password=user.password)
# #     db.add(new_user)
# #     db.commit()
# #     db.refresh(new_user)
# #     return new_user

# # @router.get("/users/{id}" , response_model=schemas.UserResponse)
# # async def get_user(id : int , db : Session=Depends(get_db)) :
# #     user=db.query(models.User).filter(models.User.id==id).first()
# #     if not user :
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exist")
# #     return user 




# from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter , UploadFile , File
# from sqlalchemy.orm import Session
# from typing import List, Optional
# from app import models, schemas, utils, oauth2
# from app.database import get_db
# import shutil
# import os


# router = APIRouter()  #Creating an instance of APIRouter() class to manage our routes in different files

# #User Login Signup

# #replace app.post with router.post as we dont have access to app and here router will do the same work 
# @router.post("/users" , status_code=status.HTTP_201_CREATED , response_model=schemas.UserResponse)
# async def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)) :
#     hashed_password = utils.hash(user.password) #Converting password into hash code
#     user.password = hashed_password
#     new_user = models.User(email=user.email,password=user.password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @router.get("/users/me", response_model=schemas.UserResponse)
# async def get_current_user_info(current_user: models.User = Depends(oauth2.get_current_user)):
#     return current_user

# @router.get("/users/{id}" , response_model=schemas.UserResponse)
# async def get_user(id : int , db : Session=Depends(get_db)) :
#     user=db.query(models.User).filter(models.User.id==id).first()
#     if not user :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exist")
#     return user 


# #Search Users Endpoint
# @router.get("/users/", response_model=List[schemas.UserResponse])
# async def search_users(search: Optional[str] = "", db: Session = Depends(get_db)):
#     users = db.query(models.User).filter(models.User.email.contains(search)).limit(10).all()
#     return users

# @router.post("/users/image")
# async def upload_profile_image(
#     file: UploadFile = File(...), 
#     current_user: models.User = Depends(oauth2.get_current_user), # Requires login
#     db: Session = Depends(get_db)
# ):
#     # 1. Create a unique filename (to avoid overwrites)
#     file_location = f"static/{current_user.id}_{file.filename}"
    
#     # 2. Save the file to the "static" folder
#     with open(file_location, "wb+") as buffer:
#         shutil.copyfileobj(file.file, buffer)
        
#     # 3. Update the User in the Database with the new URL
#     user_query = db.query(models.User).filter(models.User.id == current_user.id)

#     url = f"http://127.0.0.1:8000/{file_location}"

#     user_query.update({"profile_image": url}, synchronize_session=False)
#     db.commit()
    
#     return {"info": "Image uploaded", "url": url}



from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter , UploadFile , File
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, utils, oauth2
from app.database import get_db
import shutil
import os
import cloudinary
import cloudinary.uploader


router = APIRouter()  #Creating an instance of APIRouter() class to manage our routes in different files

cloudinary.config( 
  cloud_name = "ddpaffipb", 
  api_key = "586837344257975", 
  api_secret = "6KjYIymFMNxYFzdF6v0VN-DoPAY" 
)

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

@router.get("/users/me", response_model=schemas.UserResponse)
async def get_current_user_info(current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user

@router.get("/users/{id}" , response_model=schemas.UserResponse)
async def get_user(id : int , db : Session=Depends(get_db)) :
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exist")
    return user 


#Search Users Endpoint
@router.get("/users/", response_model=List[schemas.UserResponse])
async def search_users(search: Optional[str] = "", db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.email.contains(search)).limit(10).all()
    return users

@router.post("/users/image")
async def upload_profile_image(
    file: UploadFile = File(...), 
    current_user: models.User = Depends(oauth2.get_current_user), # Requires login
    db: Session = Depends(get_db)
):
    # 1. Upload to Cloudinary (No local file saving!)
    upload_result = cloudinary.uploader.upload(file.file)
    
    # 2. Get the secure HTTPS url
    image_url = upload_result.get("secure_url")
        
    # 3. Update the User in the Database with the new URL
    user_query = db.query(models.User).filter(models.User.id == current_user.id)

    user_query.update({"profile_image": image_url}, synchronize_session=False)
    db.commit()
    
    return {"info": "Image uploaded", "url": image_url}

