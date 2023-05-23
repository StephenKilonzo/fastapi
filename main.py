from typing import Annotated
from enum import Enum
from fastapi import Body, FastAPI, Query
from pydantic import BaseModel


app = FastAPI()


class ModelName(str, Enum):
    steve = "steve"
    mose = "mose"
    fay = "fay"



class Student(BaseModel):
    name: str
    age: int
    level: str
    description: str | None = None


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


fake_items_db = [{"item_name": "Jack"}, {"item_name": "Doo"}, {"item_name": "Showry"}]


@app.get("/")
async def root():
    return {"message":f"Here comes FastApi."}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id":item_id}


@app.get("/models/{model_name}")
async def get_user(model_name: ModelName):
    if model_name is ModelName.steve:
        return {"model_name": model_name, "message":"Steve in FastAPI!"}
    
    if model_name.value == "Fay":
        return {"model_name": model_name, "message":"Real code got home."}
    
    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

#fake url// query param
@app.get("/items/")
async def read_item(skip:int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]



#query param type conversion
@app.get("/items/{item_id}")
async def read_item(item_id:str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "FastAPI can get sweet!"}
        )
    return item
    

#multiple path and query params
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "user_id": user_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"description":"Steve Let's do this!"}
        )
    return item

# require query parameter
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id":item_id, "needy":needy}
    return item


# Create your data model
@app.post("/users/")
async def create_student(user: Student):
    return Student

@app.post("/students/")
async def create_student(student: Student):
    student_dict= student.dict()
    if student.level:
        student_details = student.name + str(student.age) + student.level
        student_dict.update({"student_details": student_details})
    return student_dict

@app.post("/students/{student_id}")
async def create_student(student_id: int, student: Student):
    return {"student_id": student_id, **student.dict()}



# multiple body params and query
@app.put("/items/{item_id}")
async def update_item(*, item_id: int, item: Item, user: User, importance: Annotated[int, Body(gt=0)], q: str | None = None,):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

# Query Parameters and String Validations
# enforce q such that its length doesn't exceed 50 characters.
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results