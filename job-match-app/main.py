from fastapi import FastAPI, Request
from routers.company_routers import companies_router
from routers.job_ads_routers import job_ads_router
from routers.job_seeker_routers import job_seekers_router
from routers.admin_routers import admin_router
from routers.skills_router import skills_router
from routers.token_router import token_router
from routers.profile_router import profile_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI(title='Skill Sync', description='to be continued')
templates = Jinja2Templates(directory='job-match-app/static/html')
app.mount('/static', StaticFiles(directory='job-match-app/static'), name='static')
app.include_router(companies_router)
app.include_router(job_ads_router)
app.include_router(admin_router)
app.include_router(token_router)
app.include_router(job_seekers_router)
app.include_router(profile_router)
app.include_router(skills_router)


@app.get('/', response_class= HTMLResponse, include_in_schema=False)
async def read_root(request: Request):
    return templates.TemplateResponse("landing_page.html", {"request": request})

@app.get('/job_seeker_register', response_class=HTMLResponse, include_in_schema=False)
async def read_job_seeker_register(request: Request):
    return templates.TemplateResponse("job_seeker_register.html", {"request": request})

@app.get('/login', response_class=HTMLResponse, include_in_schema=False)
async def read_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get('/company_register', response_class=HTMLResponse, include_in_schema=False)
async def read_login_page(request: Request):
    return templates.TemplateResponse("company_register.html", {"request": request})

@app.get('/seeker_tab', response_class=HTMLResponse, include_in_schema=False)
async def read_seeker_page(request: Request):
    return templates.TemplateResponse("logged_seeker.html", {"request": request})

@app.get('/cv_maker', response_class=HTMLResponse, include_in_schema=False)
async def read_cv_maker(request: Request):
    return templates.TemplateResponse("cv_maker.html", {"request": request})

@app.get('/seeker_section', response_class=HTMLResponse, include_in_schema=False)
async def read_seeker_section(request: Request):
    return templates.TemplateResponse("seeker_section.html", {"request": request})

@app.get('/seeker_section/personal_info', response_class=HTMLResponse, include_in_schema=False)
async def read_seeker_personal_info(request: Request):
    return templates.TemplateResponse("personal_info_seeker.html", {"request": request})

@app.get('/seeker_section/personal_info/edit', response_class=HTMLResponse, include_in_schema=False)
async def read_seeker_edit_info(request: Request):
    return templates.TemplateResponse("edit_seeker_info.html", {"request": request})

@app.get('/seeker_section/searching', response_class=HTMLResponse, include_in_schema=False)
async def read_searching_page(request: Request):
    return templates.TemplateResponse("searching_seeker.html", {"request": request})

@app.get('/seeker_section/searching/percantage', response_class=HTMLResponse, include_in_schema=False)
async def read_searching_percent_page(request: Request):
    return templates.TemplateResponse("percentage_search_seeker.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)