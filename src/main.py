from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, FastAPI
import mysql.connector 

app =FastAPI(title="ToDo-List", version="0.0.1", openapi_url="/openapi.json")

router = APIRouter()
templates = Jinja2Templates(directory="./templates")

@app.get('/', response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.post("/add-notes")
def post_notes(request: Request):
    note = input("Enter the note: ")
    with open("note.txt", "a") as file:
        file.write(note + "\n")
    print("Note added successfully!")
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)