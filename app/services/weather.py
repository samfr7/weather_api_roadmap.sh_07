import requests
import json
from flask import jsonify
from dotenv import load_dotenv
from ..extensions import redis_client
from .utils import get_exact_location_name
import redis
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

# First we need to initialize the redis client
# decode_resposes = True ensure Redis returns normal string instead of byte strings

def get_weather_location_from_redis(redis_key):
    try:
        cached_result = redis_client.get(redis_key)
        if cached_result:
            logger.info(f"Cache hit! for {redis_key}")
            return json.loads(cached_result)
        else:
            return None
    except redis.ConnectionError:
        logger.warning("Redis is down")
        return None


def get_weather_location(location:str):
    location = location.strip().lower()
    redis_key = f"weather:{location}"

    # 1. A check for redis should be made here with an assumption 
    logger.debug(f"Attempting to fetch data for location: {location}")
    cached_result = get_weather_location_from_redis(redis_key=redis_key)
    if cached_result:
        return cached_result , 200
    
    logger.debug(f"Failed to fetch data for location: {location} in Redis")
    logger.debug(f"Getting the right location name from LLM")
    # 2. Check if its something short form of a location which is already present or a spelling mistake with LLM
    location = get_exact_location_name(location=location)

    logger.debug(f"Fetched data: name for location: {location}")

    redis_key = f"weather:{location}"


    # 3. Check in redis again
    logger.debug(f"Attempting to fetch data for location: {location} Again!")
    cached_result = get_weather_location_from_redis(redis_key=redis_key)
    if cached_result:
        return cached_result , 200
    
    logger.debug(f"Failed to fetch data for location: {location} in Redis")

    BASE_URL=f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/today'

    params = {
        'key' : os.getenv('API_KEY'),
        'unitGroup': 'metric',
        'contentType':'json'
    }

    # This check is important if the api where we are fetching the data from is down or not available
    # 4. Check with the API
    logger.debug(f"Attempting to fetch data for location: {location} via API!")
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        logger.warning(f"Exception while fetching the data from the API")
        return {"message": f"External API request failed: {str(e)}"}, 500
    
    result = {}
    if response.status_code == 200:
        response = response.json()
        result['tempmax'] = response.get('days')[0].get('tempmax')
        result['tempmin'] = response.get('days')[0].get('tempmin')
        result['temp'] = response.get('days')[0].get('temp')
        result['feelslike'] = response.get('days')[0].get('feelslike')
        result['feelslikemax'] = response.get('days')[0].get('feelslikemax')
        result['feelslikemin'] = response.get('days')[0].get('feelslikemin')        
    else:
        return {"message": response.text}, response.status_code

    # 5. To set the location in redis
    logger.debug(f"Setting the data for location: {location} in Redis!")
    try:
        redis_client.set(redis_key, json.dumps(result), ex=43200)
    except redis.ConnectionError:
        print("Warning: Failed to save to Redis")
        pass
    logger.debug(f"Returning data for location: {location}!")
    return result, 200

if __name__ == "__main__":
    get_weather_location('Banglaore')