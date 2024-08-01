
# fastAPI file storage

We need you to write a small fastAPI python project that has the following three
RESTful API endpoints. Data will be stored in a small MongdoDB collection.



## Steps

Clone the App adn create a virtual enviornment
python -m venv env

Activate the virtual enviornment
source .\env\Scripts\activate

Install the requirements from requirements.txt using pip
pip install -r .\requirements.txt 

Run the app 
uvicorn main:app --reload 
or to run in a specified port use
uvicorn main:app --reload --port 8081

