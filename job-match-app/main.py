from fastapi import FastAPI
from routers.company_routers import companies_router
from routers.job_ads_routers import job_ads_router
from routers.job_seeker_routers import job_seekers_router
from routers.admin_routers import admin_router
from routers.token_router import token_router


app = FastAPI(title='Skill Sync', description='to be continued')
app.include_router(companies_router)
app.include_router(job_ads_router)
app.include_router(admin_router)
app.include_router(token_router)
app.include_router(job_seekers_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)