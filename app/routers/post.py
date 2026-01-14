# # from typing import List, Optional
# # from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
# # from httpx import Limits
# # from sqlalchemy.orm import Session
# # from app import models, oauth2, schemas
# # from app.database import get_db
# # from sqlalchemy import func


# # router = APIRouter()  #Creating an instance of APIRouter() class to manage our routes in different files


# # #It is in another file schemas
# # # class Post(BaseModel):   #class Post extending BaseModel
# # #     title : str          #Making class for data of new post
# # #     content : str
# # #     published : bool = True  #By default true
# #     #rating : Optional[int] = None  #Optional field


# # #Variable to store the data from user(not using database currently)
# # #my_posts = [{"title" : "title of post1" , "content" : "content of post2" , "id" : 1} , {"title":"favorite foods" , "content":"I like pizza" , "id" : 2}] 

# # # def find_post(id) :  #function to find the data according to the given id
# # #     for p in my_posts :
# # #         if p["id"] == id :
# # #             return p 
        
# # # def find_index_post(id) :
# # #     for i , p in enumerate(my_posts) :
# # #         if p["id"] == id : 
# # #             return i 


# # #READ => all post
# # #replace app.post with router.post as we dont have access to app and here router will do the same work 
# # @router.get("/posts" , response_model=List[schemas.PostVotes])   # response_model=List[schemas.PostResponse]  => Show the response according to our defined class not in the by default way of FastAPI
# # async def get_posts(db: Session=Depends(get_db) , limit: int = 10 , search: Optional[str]=""):   #Setting up a Query Parameter : limit(by default 10) entered by a user , search(in title , given by user)
    
# #     #Databse: 2 methods => 1=>Normal Query  2=>ORM
    
# #     #1=> Using normal Database Query
# #     # cursor.execute(""" SELECT * FROM posts """)  #Executing Query according to our need
# #     # posts = cursor.fetchall() #Fetching all data as required
    
# #     #2=> Using ORM
# #     print(limit)
# #     #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all() #ORM => Retrieves all the data from database
    
# #     posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id==models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()  #Join Query ORM => using to get which user liked which post and how much likes are there on a post

# #     result = [schemas.PostVotes(post=post , votes=votes) for post , votes in posts]

# #     return result


# # #READ => particular post(according to given id)
# # @router.get("/posts/{id}") #,response_model=List[schemas.PostResponse]
# # async def get_post(id : int , db: Session = Depends(get_db)) :  #id : int => FastAPI validates that if id is an integer or not
    
# #     #Databse: 2 methods => 1=>Normal Query  2=>ORM
    
# #     #1=> Using normal Database Query
# #     # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))
# #     # post = cursor.fetchone()

# #     #2=> ORM
# #     post = db.query(models.Post).filter(models.Post.id == id).first()
# #     posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id==models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.id==id).all()  #Join Query ORM => using to get which user liked which post and how much likes are there on a post

# #     if not post :
# #         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"post with id {id} was not found")

# #     print(post)
# #     return post


# # #CREATE
# # @router.post("/posts" , status_code= status.HTTP_201_CREATED)
# # async def create_posts(post : schemas.PostCreate , db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)): #Added oauth2 dependany because to create post it is required to be logged in and it will check if the user is logged in(it will force the user to logged in)

# #     #Databse: 2 methods => 1=>Normal Query  2=>ORM
    
# #     #1=> Using normal Database Query
# #     # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
# #     # new_post = cursor.fetchone() 
# #     # conn.commit()

# #     #2=> ORM
# #     new_post = models.Post(title=post.title,content=post.content,published=post.published,owner_id=current_user.id) #owner_id=current_user.id so that it automatically fetch the id of the currently logged user
# #     db.add(new_post)
# #     db.commit()
# #     db.refresh(new_post)
# #     return new_post


# # #DELETE
# # @router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT) 
# # async def delete_post(id : int , db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)) :

# #     #Databse: 2 methods => 1=>Normal Query  2=>ORM
    
# #     #1=> Using normal Database Query
# #     # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
# #     # deleted_post = cursor.fetchone()
# #     # conn.commit()

# #     #2=> ORM
# #     post = db.query(models.Post).filter(models.Post.id == id)

# #     if not post.first() :
# #         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"post with id {id} was not found")
# #     print(post.first().owner_id)
# #     print(current_user.id)
    
# #     #Only owner of a post can delete it
# #     #if post.first().owner_id != current_user.id :
# #     #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not authorized to perform requested action")
    
# #     post.delete(synchronize_session=False)
# #     db.commit()

# #     return Response(status_code=status.HTTP_204_NO_CONTENT)

# # #UPDATE
# # @router.put("/posts/{id}" , response_model=List[schemas.PostResponse])
# # async def update_post(id : int , post : schemas.PostCreate , db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)) :  #passing Post class as we will update data(instance) of that class

# #     #Databse: 2 methods => 1=>Normal Query  2=>ORM
    
# #     #1=> Using normal Database Query
# #     # cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """ , (post.title , post.content , post.published , str(id)))
# #     # updated_post = cursor.fetchone()
# #     # conn.commit()

# #     #2=> ORM
# #     post_query = db.query(models.Post).filter(models.Post.id == id)
# #     ppost = post_query.first()

# #     if not ppost :
# #         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"post with id {id} was not found")
    
# #     #Only owner of a post can update it
# #     #if ppost.owner_id != current_user.id :
# #     #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not authorized to perform requested action")

# #     post_query.update(dict(post) , synchronize_session=False)
# #     db.commit()




# from typing import List, Optional
# from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter , Form , File , UploadFile
# from httpx import Limits
# from sqlalchemy.orm import Session
# from app import models, oauth2, schemas
# from app.database import get_db
# from sqlalchemy import func
# import shutil
# import uuid
# import os


# router = APIRouter()  #Creating an instance of APIRouter() class to manage our routes in different files

# IMAGEDIR = "static/images/"
# os.makedirs(IMAGEDIR, exist_ok=True)

# #It is in another file schemas
# # class Post(BaseModel):   #class Post extending BaseModel
# #     title : str          #Making class for data of new post
# #     content : str
# #     published : bool = True  #By default true
#     #rating : Optional[int] = None  #Optional field


# #Variable to store the data from user(not using database currently)
# #my_posts = [{"title" : "title of post1" , "content" : "content of post2" , "id" : 1} , {"title":"favorite foods" , "content":"I like pizza" , "id" : 2}] 

# # def find_post(id) :  #function to find the data according to the given id
# #     for p in my_posts :
# #         if p["id"] == id :
# #             return p 
        
# # def find_index_post(id) :
# #     for i , p in enumerate(my_posts) :
# #         if p["id"] == id : 
# #             return i 


# #READ => all post
# #replace app.post with router.post as we dont have access to app and here router will do the same work 
# @router.get("/posts" , response_model=List[schemas.PostVotes])   # response_model=List[schemas.PostResponse]  => Show the response according to our defined class not in the by default way of FastAPI
# async def get_posts(db: Session=Depends(get_db) , limit: int = 10 , search: Optional[str]=""):   #Setting up a Query Parameter : limit(by default 10) entered by a user , search(in title , given by user)
    
#     #Databse: 2 methods => 1=>Normal Query  2=>ORM
    
#     #1=> Using normal Database Query
#     # cursor.execute(""" SELECT * FROM posts """)  #Executing Query according to our need
#     # posts = cursor.fetchall() #Fetching all data as required
    
#     #2=> Using ORM
#     print(limit)
#     #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all() #ORM => Retrieves all the data from database
    
#     posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id==models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).order_by(models.Post.created_at.desc()).limit(limit).all()  #Join Query ORM => using to get which user liked which post and how much likes are there on a post

#     result = [schemas.PostVotes(post=post , votes=votes) for post , votes in posts]

#     return result


# #READ => particular post(according to given id)
# @router.get("/posts/{id}") #,response_model=List[schemas.PostResponse]
# async def get_post(id : int , db: Session = Depends(get_db)) :  #id : int => FastAPI validates that if id is an integer or not
    
#     #Databse: 2 methods => 1=>Normal Query  2=>ORM
    
#     #1=> Using normal Database Query
#     # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))
#     # post = cursor.fetchone()

#     #2=> ORM
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id==models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.id==id).all()  #Join Query ORM => using to get which user liked which post and how much likes are there on a post

#     if not post :
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"post with id {id} was not found")

#     print(post)
#     return post


# #CREATE
# @router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# async def create_posts(
#     # We cannot use Pydantic models (schemas.PostCreate) alongside File uploads easily.
#     # We must use Form(...) for text fields.
#     title: str = Form(...),
#     content: str = Form(...),
#     published: bool = Form(True),
#     file: Optional[UploadFile] = File(None), # Optional: in case user doesn't upload an image
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user)
# ):
    
#     image_path = None

#     # Logic to save the image if provided
#     if file:
#         # 1. Generate a unique filename to avoid overwrites
#         # extract extension (e.g., .jpg)
#         _, ext = os.path.splitext(file.filename) 
#         # create unique name (e.g., 234234-234234.jpg)
#         unique_filename = f"{uuid.uuid4()}{ext}" 
#         image_path = f"{IMAGEDIR}{unique_filename}"

#         # 2. Save the file locally
#         with open(image_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#     # 3. Save to Database
#     # Note: We manually map the Form variables to the Model
#     new_post = models.Post(
#         title=title, 
#         content=content, 
#         published=published, 
#         owner_id=current_user.id,
#         image_url=image_path # Save the path to the DB
#     )
    
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post

# #DELETE
# @router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT) 
# async def delete_post(id : int , db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)) :

#     #Databse: 2 methods => 1=>Normal Query  2=>ORM
    
#     #1=> Using normal Database Query
#     # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
#     # deleted_post = cursor.fetchone()
#     # conn.commit()

#     #2=> ORM
#     post = db.query(models.Post).filter(models.Post.id == id)

#     if not post.first() :
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"post with id {id} was not found")
#     print(post.first().owner_id)
#     print(current_user.id)
    
#     #Only owner of a post can delete it
#     #if post.first().owner_id != current_user.id :
#     #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not authorized to perform requested action")
    
#     post.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# #UPDATE
# @router.put("/posts/{id}", response_model=schemas.PostResponse)
# async def update_post(
#     id: int, 
#     # REPLACE 'post: schemas.PostCreate' with these Form/File parameters:
#     title: str = Form(...),
#     content: str = Form(...),
#     published: bool = Form(True),
#     image: Optional[UploadFile] = File(None), # This handles the new image file
#     db: Session = Depends(get_db), 
#     current_user: int = Depends(oauth2.get_current_user)
# ):
#     # 1. Find the post
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

#     if post.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

#     # 2. Prepare the update data
#     update_data = {
#         "title": title,
#         "content": content,
#         "published": published
#     }

#     # 3. Handle Image Update (if a new file was sent)
#     if image:
#         # Generate unique filename

#         if post.image_url:
#             path_to_remove = post.image_url
#             # Check if full path or relative needs handling
#             if os.path.exists(path_to_remove):
#                 os.remove(path_to_remove)

#         image.filename = f"{uuid.uuid4()}.png"
        
#         # Read and write the new file
#         file_location = f"{IMAGEDIR}{image.filename}"
#         contents = await image.read()
#         with open(file_location, "wb") as f:
#             f.write(contents)
            
#         # Add new filename to update data
#         update_data["image_url"] = f"static/images/{image.filename}"

#     # 4. Perform the update
#     post_query.update(update_data, synchronize_session=False)
#     db.commit()

#     return post_query.first()
    
# #     return post_query.first()





from typing import List, Optional
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter , Form , File , UploadFile
from httpx import Limits
from sqlalchemy.orm import Session
from app import models, oauth2, schemas
from app.database import get_db
from sqlalchemy import func
import shutil
import uuid
import os

import cloudinary
import cloudinary.uploader



router = APIRouter()  #Creating an instance of APIRouter() class to manage our routes in different files

cloudinary.config( 
  cloud_name = "ddpaffipb", 
  api_key = "586837344257975", 
  api_secret = "6KjYIymFMNxYFzdF6v0VN-DoPAY" 
)

IMAGEDIR = "static/images/"
os.makedirs(IMAGEDIR, exist_ok=True)

#It is in another file schemas
# class Post(BaseModel):   #class Post extending BaseModel
#     title : str          #Making class for data of new post
#     content : str
#     published : bool = True  #By default true
    #rating : Optional[int] = None  #Optional field


#Variable to store the data from user(not using database currently)
#my_posts = [{"title" : "title of post1" , "content" : "content of post2" , "id" : 1} , {"title":"favorite foods" , "content":"I like pizza" , "id" : 2}] 

# def find_post(id) :  #function to find the data according to the given id
#     for p in my_posts :
#         if p["id"] == id :
#             return p 
        
# def find_index_post(id) :
#     for i , p in enumerate(my_posts) :
#         if p["id"] == id : 
#             return i 


#READ => all post
#replace app.post with router.post as we dont have access to app and here router will do the same work 
@router.get("/posts" , response_model=List[schemas.PostVotes])   # response_model=List[schemas.PostResponse]  => Show the response according to our defined class not in the by default way of FastAPI
async def get_posts(db: Session=Depends(get_db) , limit: int = 10 , search: Optional[str]=""):   #Setting up a Query Parameter : limit(by default 10) entered by a user , search(in title , given by user)
    
    #Databse: 2 methods => 1=>Normal Query  2=>ORM
    
    #1=> Using normal Database Query
    # cursor.execute(""" SELECT * FROM posts """)  #Executing Query according to our need
    # posts = cursor.fetchall() #Fetching all data as required
    
    #2=> Using ORM
    print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all() #ORM => Retrieves all the data from database
    
    posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id==models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).order_by(models.Post.created_at.desc()).limit(limit).all()  #Join Query ORM => using to get which user liked which post and how much likes are there on a post

    result = [schemas.PostVotes(post=post , votes=votes) for post , votes in posts]

    return result


#READ => particular post(according to given id)
@router.get("/posts/{id}") #,response_model=List[schemas.PostResponse]
async def get_post(id : int , db: Session = Depends(get_db)) :  #id : int => FastAPI validates that if id is an integer or not
    
    #Databse: 2 methods => 1=>Normal Query  2=>ORM
    
    #1=> Using normal Database Query
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()

    #2=> ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()
    posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id==models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.id==id).all()  #Join Query ORM => using to get which user liked which post and how much likes are there on a post

    if not post :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"post with id {id} was not found")

    print(post)
    return post


#CREATE
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    published: bool = Form(True),
    image: Optional[UploadFile] = File(None), # Image file
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    image_url = None
    
    if image:
        # Upload to Cloudinary directly
        upload_result = cloudinary.uploader.upload(image.file)
        image_url = upload_result.get("secure_url") # This is a permanent HTTP link

    new_post = models.Post(
        title=title, 
        content=content, 
        published=published, 
        image_url=image_url, # Save the Cloudinary URL, not a local path
        owner_id=current_user.id
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#DELETE
@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT) 
async def delete_post(id : int , db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)) :

    #Databse: 2 methods => 1=>Normal Query  2=>ORM
    
    #1=> Using normal Database Query
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    #2=> ORM
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first() :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"post with id {id} was not found")
    print(post.first().owner_id)
    print(current_user.id)
    
    #Only owner of a post can delete it
    #if post.first().owner_id != current_user.id :
    #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#UPDATE
@router.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post(
    id: int, 
    # REPLACE 'post: schemas.PostCreate' with these Form/File parameters:
    title: str = Form(...),
    content: str = Form(...),
    published: bool = Form(True),
    image: Optional[UploadFile] = File(None), # This handles the new image file
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    # 1. Find the post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # 2. Prepare the update data
    update_data = {
        "title": title,
        "content": content,
        "published": published
    }

    # 3. Handle Image Update (if a new file was sent)
    if image:
        # Upload NEW image to Cloudinary
        upload_result = cloudinary.uploader.upload(image.file)
        new_image_url = upload_result.get("secure_url")
        
        # Add new URL to update data
        update_data["image_url"] = new_image_url
        
        # NOTE: Ideally, you should also delete the OLD image from Cloudinary here 
        # to save space, but that requires storing the 'public_id' in your DB. 
        # For now, just overwriting the URL is fine.

    # 4. Perform the update
    post_query.update(update_data, synchronize_session=False)
    db.commit()

    return post_query.first()

