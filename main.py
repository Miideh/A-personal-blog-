from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates 
from app.routes import app_router 

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static", name="static"))
templates = Jinja2Templates(directory="app/templates") 
app.include_router(app_router) 
