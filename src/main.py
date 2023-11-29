from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
import mysql.connector 

app =APIRouter(title="ToDo-List", version="0.0.1", openapi_url="/openapi.json")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

router = APIRouter()
templates = Jinja2Templates(directory="./templates")

@app.get('/', response_class=HTMLResponse)
def read_root():
    return templates.TemplateResponse("index.html", {"request": request})

