from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import os
from dotenv import load_dotenv
load_dotenv()

cors = CORS()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute", "50 per hour", "500 per day"]
    # Need to add redis URI
)

redis_client = redis.Redis(
    host=os.getenv('REDIS_URL'), 
    port=os.getenv('REDIS_PORT'), 
    db=0, 
    decode_responses=True)
