from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Biocraft", version="2.0.4", lifespan=lifespan)


@app.get("/")
async def root():
    return RedirectResponse(url="/static/")


app.mount("/static", StaticFiles(directory="static", html=True), name="static")

from app.routers import auth, users, admin, chat, inquiries

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(chat.router)
app.include_router(inquiries.router)
