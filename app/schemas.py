# import datetime
# from typing import Optional
# from pydantic import BaseModel, EmailStr
# from pydantic import conint


# class PostBase(BaseModel):   
#     title : str          
#     content : str
#     published : bool = True

# class PostCreate(PostBase):
#     pass

# class UserResponse(BaseModel) :
#     id : int 
#     email : EmailStr

#     class Config :
#         from_attributes = True

# class PostResponse(BaseModel) :
#     title : str          
#     content : str
#     published : bool 
#     id : int
#     # created_at : datetime
#     owner_id : int
#     owner : UserResponse

#     class Config :
#         from_attributes = True


# class UserCreate(BaseModel) :
#     email : EmailStr #EmailStr will automatically validate for a valid email
#     password : str

# class PostVotes(BaseModel) :
#     post : PostResponse
#     votes : int

#     class Config :
#         from_attributes = True

# class UserLogin(BaseModel) :
#     email : EmailStr
#     password : str

# class Token(BaseModel) :
#     access_token : str
#     token_type : str

# class TokenData(BaseModel) :
#     id : Optional[str] = None

# class Vote(BaseModel) :
#     post_id : int




import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic import conint


class PostBase(BaseModel):   
    title : str          
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel) :
    id : int 
    email : EmailStr
    profile_image: Optional[str] = None

    class Config :
        from_attributes = True

class PostResponse(BaseModel) :
    title : str          
    content : str
    published : bool 
    id : int
    image_url : Optional[str] = None
    # created_at : datetime
    owner_id : int
    owner : UserResponse

    class Config :
        from_attributes = True


class UserCreate(BaseModel) :
    email : EmailStr #EmailStr will automatically validate for a valid email
    password : str

class PostVotes(BaseModel) :
    post : PostResponse
    votes : int

    class Config :
        from_attributes = True

class UserLogin(BaseModel) :
    email : EmailStr
    password : str

class Token(BaseModel) :
    access_token : str
    token_type : str

class TokenData(BaseModel) :
    id : Optional[str] = None

class Vote(BaseModel) :
    post_id : int
    dir : int  #1=> like(vote) , 0=>unlike
#     dir : int  #1=> like(vote) , 0=>unlike
