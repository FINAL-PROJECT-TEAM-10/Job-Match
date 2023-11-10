from fastapi import FastAPI
from routers.company_routers import companies_router
from routers.job_ads_routers import job_ads_router



app = FastAPI(title='Job_Match', description='to be continued')
app.include_router(companies_router)
app.include_router(job_ads_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)