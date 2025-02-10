from fastapi import APIRouter, Request, HTTPException, Depends ,Request
from fastapi.templating import Jinja2Templates 
from app.database import blog_collection 

app_router = APIRouter() 
templates = Jinja2Templates(directory="app/templates") 


@app_router.get("/") 
async def home(request: Request): 
    blogs = await blog_collection.find().to_list(100) 
    for blog in blogs: 
        blog["_id"] = str(blog["_id"]) 
    return templates.TemplateResponse("home.html", {"request": request, 
"blogs": blogs}) 



@app_router.get("/blog/{blog_id}") 
async def blog_detail(blog_id: str, request: Request): 
    blog = await blog_collection.find_one({"_id": ObjectId(blog_id)}) 
    if not blog: 
        raise HTTPException(status_code=404, detail="Blog not found") 
    blog["_id"] = str(blog["_id"]) 
    return templates.TemplateResponse("blog.html", {"request": request,"blog": blog}) 

@app_router.get("/dashboard")
async def dashboard(request: Request): 
    blogs = await blog_collection.find().to_list(100) 
    for blog in blogs: 
        blog["_id"] = str(blog["_id"]) 
    return templates.TemplateResponse("dashboard.html", {"request": request, "blogs": blogs})

@app_router.put("/blog/{blog_id}")
async def  blog_detail(blog_id:str , reqquest: Request)
    