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

sort_filds=["name","age","course"]
sort_order=["asc","desc"]
@app.get("/sort")
def sort_students(
    sort_by:str=Query(None,description=f"sort students by filed.must be one of the {sort_filds}"),
    sort_order:str=Query("asc",description=f"sort order.must be one of the {sort_order}")
):
    if sort_by not in sort_filds:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Must be one of {sort_filds}")
    if sort_order not in sort_order:
        raise HTTPException(status_code=400, detail="Invalid sort order. Must be 'asc' or 'desc'")
    
    data=load_data()
    student =[]
    for student_id, info in data.items():
        info["id"] = student_id
        student.append(info)
    reverse =( sort_order=="desc")
    sorted_students=sorted(student,key= lambda x:x[sort_by],reverse=reverse)
    return sorted_students



"""
Pagination

http://127.0.0.1:8000/pagination?page=1&limit=2
page -> starting page number
limit -> number of records per page
"""
@app.get("/pagination")
def paginaiton_student(
    page:int=Query(1,ge=1,description="Page number"),
    limit:int=Query(2,ge=1,le=100,description="Number of records per page")
):
    data=load_data()




    student =[]
    for student_id, info in data.items():
        info["id"] = student_id
        student.append(info)

    start =(page -1)*limit
    end=start +limit
    page_student=student[start:end]
    total_student=len(student)
    return{
        "page":page,
        "limit":limit,
        "students": page_student,
        "total_student": total_student  
    }