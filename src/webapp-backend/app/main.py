from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager

from .routers import users, projects, auth
from .utils.admin_setup import create_init_admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before application starts
    create_init_admin()

    yield # Application starts here

    # After application stopped



app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
