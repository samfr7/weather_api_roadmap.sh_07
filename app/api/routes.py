from flask import Blueprint, jsonify
from ..services import get_weather_location

bp = Blueprint('weather', import_name=__name__)

@bp.route('/weather/<string:location>', methods=['GET'])
def get_weather(location: str):
    data, status_code = get_weather_location(location=location)
    
    return jsonify(data), status_code