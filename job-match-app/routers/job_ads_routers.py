from fastapi import APIRouter, Query, Body,Header, HTTPException

job_ads_router = APIRouter(prefix='/job_ads',tags={'Everything available for Job_Ads'})

@job_ads_router.post('/')
def create_new_job_ad(description: str = Query(), min_salary: int = Query(),max_salary: int = Query(),
                      status: str = Query(),date_posted: str = Query(), name_of_company: str = Query()):
    pass
