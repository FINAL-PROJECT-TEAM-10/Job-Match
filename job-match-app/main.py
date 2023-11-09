from fastapi import FastAPI

from routers.admin_routers import admin_router
from routers.token_router import token_router

app = FastAPI()

app.include_router(admin_router)
app.include_router(token_router)


app = FastAPI(title='Job_Match', description='to be continued')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)