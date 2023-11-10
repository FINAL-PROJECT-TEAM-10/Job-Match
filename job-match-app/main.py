from fastapi import FastAPI
from routers.job_seeker_routers import job_seekers_router




app = FastAPI(title='Job_Match', description='to be continued')



app.include_router(job_seekers_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)