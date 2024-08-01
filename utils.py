from fastapi import HTTPException
from database import files_collection
from models import FileModel
import bson
from bson import ObjectId



# retrive the file using file id
async def get_file(file_id:str):
    try:
        # convert the file_id string to an ObjectId
        object_id = ObjectId(file_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid file ID format")

    file = files_collection.find_one({"_id": object_id})
    return file


# list all the files
async def get_files():
    files = files_collection.find()
    return files


# add the file
async def add_file(file: FileModel):
    existing_file = files_collection.find_one({"name": file.name})
    if existing_file:
        return None
    result = files_collection.insert_one(file.dict())
    return result.inserted_id

