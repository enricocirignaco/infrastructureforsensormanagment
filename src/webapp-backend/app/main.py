from fastapi import Depends, FastAPI

from .routers import users, projects

app = FastAPI()


app.include_router(users.router)
app.include_router(projects.router)

#@app.get("/")
#async def root():
#    return {"message": "Hello Bigger Applications!"}