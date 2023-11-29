from typing import Annotated 
from fastapi.responses import HTMLResponse
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
    # try:
    #     connection = mysql.connector.connect(
    #         host=host_name, user=user_name, passwd=user_password, database=db_name
    #     )
    #     print("MySQL Database connection successful")
    # except Error as err:
    #     print(f"Error: '{err}'")

    return connection

#root-route
@app.get('/', response_class=HTMLResponse)
def read_root(request: Request):
     
    connection = create_server_connection()
    cursor = connection.cursor()
    query = "SELECT id, todoitem, itemstatus, category FROM notes;"
    cursor.execute(query)
    notes = cursor.fetchall()    
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

@app.post("/", response_class=HTMLResponse)
def post_notes(request: Request, eingabe: Annotated[str, Form()], category: Annotated[str, Form()]
): 
    print(eingabe, category)
    # with open("note.txt", "a") as file:
    #     file.write(note + "\n")
    # print("Note added successfully!")
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)