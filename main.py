from fastapi import FastAPI,HTTPException, Path, Query
import json

app = FastAPI()

@app.get("/") #endpoint
def greet():
    return{"hello fast api"}


@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

# helper function
def load_data():
    with open("students.json","r")as file:
        return json.load(file)
    
@app.get("/students")
def student():
    return load_data()


@app.get("/students/{student_id}") #path parameter student_id

def get_id(student_id:str=Path(...,description="The ID of the student to retrieve")):
    data= load_data()
    if student_id not in data:
        raise HTTPException(status_code=404, 
                            detail=f"Student not '{student_id}' found")    
    return data[student_id]


# ? er por query thakbe


@app.get("/filter")
def filter(course:str=Query(None,description="Filter students by course")):
    data=load_data()
    if course is None:
        return data
    filtered = {}
    for student_id, info in data.items():
        if info["course"].lower()==course.lower():
            filtered[student_id]=info
    return filtered