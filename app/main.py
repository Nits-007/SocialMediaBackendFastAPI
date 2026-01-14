# from typing import Optional
# from fastapi import FastAPI, HTTPException, Response , status , Depends
# from fastapi.params import Body
# from pydantic import BaseModel
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from fastapi.middleware.cors import CORSMiddleware


# # from app.routers.vote import vote
# from . import models
# from .database import engine
# from sqlalchemy.orm import Session
# from .routers import post , user , auth , vote #importing these 2 files for routing
# from pydantic_settings  import BaseSettings
# from app import config


# app = FastAPI() #instance


# app.add_middleware(  #CORS = > Cross Origin Resource Sharing => Used to make a request to our API from a real website
#     CORSMiddleware,
#     allow_origins=["https://www.google.com"],
#     allow_credentials=True,
#     allow_methods=["*"],  # * means everything/everyone
#     allow_headers=["*"],
# )

# models.Base.metadata.create_all(bind=engine) #ORM=>SQLAlchemy

# #Connecting with our Postgres Database=>will only need if we want to use Real SQL Queries and not ORM's
# while True :
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='nits007',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected")
#         break
#     except Exception as error :
#         print("Failed connecting to database")
#         print("Error : " , error)
#         time.sleep(2)

# app.include_router(post.router)  #including the 2 routes from different files
# app.include_router(user.router)
# app.include_router(auth.router)
# app.include_router(vote.router)



# @app.get("/") #path
# async def root(): #function name
#     return {"message": "Hello World"}



from typing import Optional
from fastapi import FastAPI, HTTPException, Response , status , Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os


# from app.routers.vote import vote
from . import models
from .database import engine
from sqlalchemy.orm import Session
from .routers import post , user , auth , vote #importing these 2 files for routing
from pydantic_settings  import BaseSettings
from app import config


app = FastAPI() #instance

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(  #CORS = > Cross Origin Resource Sharing => Used to make a request to our API from a real website
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # * means everything/everyone
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine) #ORM=>SQLAlchemy

#Connecting with our Postgres Database=>will only need if we want to use Real SQL Queries and not ORM's
while True :
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='nits007',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected")
        break
    except Exception as error :
        print("Failed connecting to database")
        print("Error : " , error)
        time.sleep(2)

app.include_router(post.router)  #including the 2 routes from different files
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


if not os.path.exists('static'):
    os.makedirs('static')



@app.get("/") #path
async def root(): #function name
    return {"message": "Hello World"}




