from fastapi import FastAPI
from routers.company_routers import companies_router
from routers.job_ads_routers import job_ads_router
from routers.job_seeker_routers import job_seekers_router
from routers.admin_routers import admin_router
from routers.token_router import token_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI(title='Skill Sync', description='to be continued')
templates = Jinja2Templates(directory='job-match-app/templates')
app.mount('/static', StaticFiles(directory='job-match-app/static'), name='static')
app.include_router(companies_router)
app.include_router(job_ads_router)
app.include_router(admin_router)
app.include_router(token_router)
app.include_router(job_seekers_router)


@app.get("/", response_class= HTMLResponse)
async def landing_page(request: HTMLResponse):
    return templates.TemplateResponse("landing_page.html",{"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)