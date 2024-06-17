from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:nits007@localhost/fastapi'

#Not working but it should work as it hides the secrets
#SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@"f"{settings.database_hostname }:{settings.database_port}/{settings.database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(): #ORM=>SQLAlchemy
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:nits007@localhost/fastapi'

