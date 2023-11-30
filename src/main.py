from typing import Annotated 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, FastAPI, Form
import mysql.connector 
from mysql.connector import Error
from dotenv import load_dotenv, dotenv_values

app =FastAPI(title="ToDo-List", version="0.0.1", openapi_url="/openapi.json")
templates = Jinja2Templates(directory="./templates")

# load_dotenv()
config = dotenv_values(".env")

# Serverconnection herstellen
def create_server_connection():
    connection = None
    host_name = config.get("DB_HOST")
    user_name = config.get("DB_USER")
    user_password = config.get("DB_PASSWORD")
    db_name = config.get("DB_NAME")
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password, database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def getOptionalSortedTaskFromDB(connection, sorted):
    cursor = connection.cursor()
    if sorted:
        query = "SELECT id, taskname, taskstatus, taskcategory FROM tasks" 
        print("hello")
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        return result
    except Error as err:
        print(f"Error: '{err}'")
        return None
    
def insertTaskintoDB(connection, taskname, taskstatus, taskcategory):
    cursor = connection.cursor()
    query = "INSERT INTO tasks(taskname, taskstatus, taskcategory) VALUES(%s, %s, %s)" 
    data = (taskname, taskstatus, taskcategory)
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Inserted Data succesfully")
    except Error as err:
        print(f"Error: '{err}'")
    
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
    print(task)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": task})

@app.post("/", response_class=HTMLResponse)
def post_tasks(taskname: Annotated[str, Form()], taskstatus: Annotated[str, Form()], taskcategory: Annotated[str, Form()]):
    connection = create_server_connection()
    insertTaskintoDB(connection, taskname, taskstatus, taskcategory)
    return RedirectResponse(url="http://localhost:8000/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
