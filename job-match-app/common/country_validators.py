import requests
from fastapi import Query,HTTPException
from opencage.geocoder import OpenCageGeocode
from fastapi.responses import JSONResponse


OPENCAGE_API_KEY = "c5da8ed7653f4b4babc9794a3eb445b0"
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

def validate_location(city: str, country: str):
    location_query = f"{city}, {country}"
    result = geocoder.geocode(location_query)

    if not result or not result[0]['components']:
        raise HTTPException(status_code=400, detail="Invalid city or country")

    components = result[0]['components']
    if 'city' in components and 'country' in components:
        if components['city'] != city or components['country'] != country:
            raise HTTPException(status_code=400, detail="The city is not from this country")
    else:
        raise HTTPException(status_code=400, detail="Invalid city or country")

    return result
