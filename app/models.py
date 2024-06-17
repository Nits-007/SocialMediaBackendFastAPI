from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.sql.expression import null
from .database import Base 
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer , primary_key=True , nullable=False)
    title = Column(String , primary_key=False , nullable=False)
    content = Column(String , primary_key=False , nullable=False)
    published = Column(Boolean , server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text('now()'))
    owner_id = Column(Integer , ForeignKey("users.id" , ondelete="CASCADE") , nullable=False)
    owner = relationship("User") #Fetch the user based on the user id and then returns it 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key=True , nullable=False)
    email = Column(String , nullable=False , unique=True)
    password = Column(String , nullable=True)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text('now()'))
    
class Vote(Base):
    __tablename__ = "votes"
    
    user_id = Column(Integer , ForeignKey("users.id" , ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer , ForeignKey("posts.id" , ondelete="CASCADE"), primary_key=True)
