# from fastapi import APIRouter , Depends , status , HTTPException , Response
# from sqlalchemy.orm import Session
# from app import models, schemas, utils , oauth2
# from app.database import get_db

# router = APIRouter()

# @router.post("/login")
# def login(user_creds : schemas.UserLogin , db : Session = Depends(get_db)) :
#     user = db.query(models.User).filter(models.User.email == user_creds.email).first()
#     if not user :
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credential")
#     if not utils.verify(user_creds.password,user.password) :
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credential")

#     #create a JWT token
#     access_token = oauth2.create_access_token(data={"user_id":user.id})
    
#     #then return the token
#     return {"access token" : access_token , "token_type" : "bearer"}


from fastapi import APIRouter , Depends , status , HTTPException , Response
from sqlalchemy.orm import Session
from app import models, schemas, utils , oauth2
from app.database import get_db

router = APIRouter()

@router.post("/login")
def login(user_creds : schemas.UserLogin , db : Session = Depends(get_db)) :
    user = db.query(models.User).filter(models.User.email == user_creds.email).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credential")
    if not utils.verify(user_creds.password,user.password) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credential")

    #create a JWT token
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    
    #then return the token
    return {"access token" : access_token , "token_type" : "bearer"}


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout():
    """
    Because JWTs are stateless, the server cannot explicitly 'invalidate' a token 
    without a blacklist. This endpoint serves as a signal to the frontend 
    to remove the token from client-side storage (localStorage/cookies).
    """
    return {"message": "Logout successful"}

