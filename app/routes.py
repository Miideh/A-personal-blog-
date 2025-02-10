from fastapi import APIRouter, Request, HTTPException, Depends, Form
from fastapi.templating import Jinja2Templates
from app.database import blog_collection

app_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@app_router.get("/")
async def home(request: Request):
    blogs = await blog_collection.find().to_list(100)
    for blog in blogs:
        blog["_id"] = str(blog["_id"])
    return templates.TemplateResponse("home.html", {"request": request, "blogs": blogs})

@app_router.get("/blog/{blog_id}")
async def blog_detail(blog_id: str, request: Request):
    blog = await blog_collection.find_one({"_id": ObjectId(blog_id)})
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog["_id"] = str(blog["_id"])
    return templates.TemplateResponse("blog.html", {"request": request, "blog": blog})

@app_router.post("/blog/create")
async def create_blog(title: str = Form(...), content: str = Form(...)):
    new_blog = {"title": title, "content": content}
    result = await blog_collection.insert_one(new_blog)
    return {"message": "Blog created successfully", "id": str(result.inserted_id)}

@app_router.post("/blog/update/{blog_id}")
async def update_blog(blog_id: str, title: str = Form(...), content: str = Form(...)):
    update_result = await blog_collection.update_one(
        {"_id": ObjectId(blog_id)},
        {"$set": {"title": title, "content": content}}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found or no update made")
    return {"message": "Blog updated successfully"}

@app_router.delete("/blog/delete/{blog_id}")
async def delete_blog(blog_id: str):
    delete_result = await blog_collection.delete_one({"_id": ObjectId(blog_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}

@app_router.get("/dashboard")
async def dashboard(request: Request):
    blogs = await blog_collection.find().to_list(100)
    for blog in blogs:
        blog["_id"] = str(blog["_id"])
    return templates.TemplateResponse("dashboard.html", {"request": request, "blogs": blogs})
