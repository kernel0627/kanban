from datetime import datetime , timedelta
from jose import JWTError , jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHMS = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_DAYS =  24

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode , SECRET_KEY, algorithm=ALGORITHMS)
    return encoded_jwt


