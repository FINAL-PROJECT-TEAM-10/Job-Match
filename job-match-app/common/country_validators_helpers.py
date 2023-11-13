from fastapi import HTTPException
from opencage.geocoder import OpenCageGeocode


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


def validate_city(city: str):
    result = geocoder.geocode(city)

    if result and result[0].get('components', {}).get('_type') == 'city':
        return True
    else:
        raise HTTPException(status_code=400, detail="Invalid city")
    

def find_country_by_city(city:str):

    results = geocoder.geocode(city)

    country = results[0]['components']['country']
    return country