import os
from typing import Annotated 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, FastAPI, Form, HTTPException
import mysql.connector 
from mysql.connector import Error
from dotenv import load_dotenv

app =FastAPI(title="ToDo-List", version="0.0.1", openapi_url="/openapi.json")
templates = Jinja2Templates(directory="./templates")

load_dotenv()


# Serverconnection herstellen
def create_server_connection():
    connection = None
    host_name = os.getenv("DB_HOST")
    print("##########", host_name)
    user_name = os.getenv("DB_USER")
    user_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, password=user_password, database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def getOptionalSortedTaskFromDB(connection, sorted):
    cursor = connection.cursor()
    if sorted:
        query = "SELECT * FROM tasks" 
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")
        return None
    
def insertTaskintoDB(connection, taskname, taskcategory):
    cursor = connection.cursor()
    query = "INSERT INTO tasks(taskname, taskcategory) VALUES(%s, %s)" 
    data = (taskname, taskcategory)
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Inserted Data succesfully")
    except Error as err:
        print(f"Error: '{err}'")

def deleteTaskDB(connection, id):
    cursor = connection.cursor()
    query = "DELETE FROM tasks WHERE id = %s"
    id = [id] 
    try:
        cursor.execute(query, id)
        connection.commit()
        print("Data succesfully deleted")
    except Error as err:
        print(f"Error: '{err}'")

def updateTasksintoDB(connection, id):
    cursor = connection.cursor()
    query = """
    UPDATE tasks SET taskstatus = CASE 
        WHEN taskstatus = 'open' THEN 'in progress'
        WHEN taskstatus = 'in progress' THEN 'finished'
        ELSE taskstatus
    END
    WHERE id = %s;
    """
    id = [id]
    try:
        cursor.execute(query, id)
        connection.commit()
        print("Taskstatus successfully changed")
    except Error as err:
        print(f"Error: '{err}'")

def find_task(id):
    for task in task:
        if id == task.id:
            return task
    return None
    
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def select_data(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")
        return None

#root-route
@app.get('/', response_class=HTMLResponse)
def read_root(request: Request):
    connection = create_server_connection()
    sorted = True
    task = getOptionalSortedTaskFromDB(connection, sorted)  
    return templates.TemplateResponse("index.html", {"request": request, "tasks": task})

@app.post("/", response_class=HTMLResponse)
def post_tasks(taskname: Annotated[str, Form()], taskcategory: Annotated[str, Form()]):
    connection = create_server_connection()
    insertTaskintoDB(connection, taskname, taskcategory)
    return RedirectResponse(url="http://localhost:8000/", status_code=303)

@app.post('/delete', response_class=RedirectResponse)
def delete_task(id: Annotated[int, Form()]):
    connection = create_server_connection()
    deleteTaskDB(connection, id)
    return RedirectResponse(url="http://localhost:8000/", status_code=303)

@app.post('/update' , response_class=RedirectResponse)
def update_status(id: Annotated[int, Form()]):
    connection = create_server_connection()
    updateTasksintoDB(connection, id)
    return RedirectResponse(url="http://localhost:8000/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
