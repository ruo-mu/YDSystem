# app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import LoginRouter, PictureRouter

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(LoginRouter.router, prefix="/user", tags=["user"])
app.include_router(PictureRouter.router, prefix="/picture", tags=["picture"])


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "Index"})


@app.get("/main")
async def index(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "name": "main"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app='main:app',
        host="127.0.0.1",
        port=8080,
        reload=True,
        workers=4
    )
