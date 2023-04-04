from fastapi import FastAPI
from routers import users

app = FastAPI()
app.include_router(users.router)


@app.get("/", status_code=201)
async def read_root():
    return {'Url:': 'https://gergg90.github.io/Blog-Portfolio/'}