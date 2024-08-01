from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from auth import authenticate
from database import files_collection, users_collection
from models import FileModel
from utils import get_file, get_files, add_file
from dotenv import load_dotenv
from passlib.context import CryptContext
import aiofiles
import os


load_dotenv()

app = FastAPI()
STORAGE_PATH = os.getenv("STORAGE_PATH")
# List of all valid extensions
VALID_EXTENSIONS = {".docx", ".pptx", ".pdf"}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# save the file to a folder called storage
async def save_file(file: UploadFile, file_path: str):
    async with aiofiles.open(file_path, 'wb') as out_file:
        # read file chunk by chunk
        while content := await file.read(1024):  
            await out_file.write(content)


# extract summary from the file, we'll return the first 100 characters
def file_summary(file_path: str):
    with open(file_path, 'rb') as file:
        content = file.read()
        return content[:100].decode('utf-8', errors='ignore')


# register the user to the system
@app.post("/v1/register")
async def register_user(email: str, password: str):
    collection = users_collection
    if collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(password)
    user = {"email": email, "password": hashed_password}
    collection.insert_one(user)
    return {"message": "User registered successfully"}


# # login to system by registered user
# @app.post("/v1/login")
# async def login_user(email: str, password: str):
#     collection = users_collection
#     user = collection.find_one({"email": email})
#     if user and pwd_context.verify(password, user["password"]):
#         return {"message": "Login successful"}
#     raise HTTPException(status_code=401, detail="Invalid credentials")


# save a file to system
@app.post("/v1/files")
async def upload_file(file: UploadFile = File(...), 
                      name: str = File(...), 
                      user: str = Depends(authenticate)):
    file_extension = os.path.splitext(file.filename)[1].lower()  # lowercase

    if file_extension not in VALID_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")
    file_path = os.path.join(STORAGE_PATH, file.filename)
    
    # checks if the file already exists in the database
    existing_file = files_collection.find_one({"filename": file.filename})
    if existing_file:
        raise HTTPException(status_code=400, detail="File already exists")

    # save file to the server
    await save_file(file, file_path)

    # create a file summary
    summary = file_summary(file_path)

    # save file data to the database
    file_model = FileModel(name=name,filename=file.filename, summary=summary,path=file_path)
    await add_file(file_model)
    return {"file_name": file_model.name}


# list all saved a file in the system
@app.get("/v1/files")
async def list_files(current_user: dict = Depends(authenticate)):
    files = await get_files()
    return [{"_id": str(file["_id"]), "name": file["name"]} for file in files]


# view single file using file id from the system if exist
@app.get("/v1/files/{file_id}")
async def get_file_summary(file_id: str, user: str = Depends(authenticate)):
    file = await get_file(file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    else:
        # print(f"-----------------------------{type(file)}")
        return {"file_id": str(file["_id"]), "name": file["name"], "summary": file["summary"],"filepath": file["path"], }

