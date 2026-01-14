from pydantic_settings import BaseSettings


class Settings(BaseSettings) :  #Making class for environment variables
   database_hostname: Optional[str] = None
   database_port: Optional[str] = None
   database_password: Optional[str] = None
   database_name: Optional[str] = None
   database_username: Optional[str] = None
   secret_key : str 
   algorithm : str
   access_token_expire_minutes : int

   class Config :
      env_file = ".env"

settings = Settings() #Instance of the class defined above
 
