from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from database import users_collection
from passlib.context import CryptContext
import secrets


security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# authenticate the user login
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    collection = users_collection
    user = collection.find_one({"email": credentials.username})
    if user and pwd_context.verify(credentials.password, user["password"]):
        return user
    raise HTTPException(status_code=401, detail="Invalid login credentials")
