import pytest
import json
import requests
from unittest.mock import patch, MagicMock
from app.services.weather import get_weather_location_from_redis, get_weather_location
from app.services.utils import get_exact_location_name

@patch('app.services.weather.redis_client.get')
def test_none_location_from_redis(mock_redis_get):
    mock_redis_get.return_value = None

    redis_key = "weather:bangalore"
    cached_result = get_weather_location_from_redis(redis_key=redis_key)

    assert cached_result == None

@patch('app.services.weather.redis_client.get')
def test_value_location_from_redis(mock_redis_get):
    mock_redis_get.return_value = json.dumps({"temp":28.1})

    redis_key = "weather:bangalore"
    cached_result = get_weather_location_from_redis(redis_key=redis_key)

    assert cached_result is not None
    assert "temp" in cached_result.keys()

@patch('app.services.utils.client.chat.completions.create')
def test_normalize_location_with_llm(mock_groq_create):
    fake_message = MagicMock()
    fake_message.content = "bangalore"

    fake_choice = MagicMock()
    fake_choice.message = fake_message

    mock_groq_create.return_value.choices = [fake_choice]

    result = get_exact_location_name("bglore")

    assert result == "bangalore"

@patch('app.services.weather.redis_client')
@patch('app.services.utils.client.chat.completions.create')
@patch('app.services.weather.requests.get')
def test_fetch_weather(mock_req_get, mock_exact_name, mock_redis):
    mock_redis.get.return_value = None

    fake_message = MagicMock()
    fake_message.content = "bangalore"

    fake_choice = MagicMock()
    fake_choice.message = fake_message

    mock_exact_name.return_value.choices = [fake_choice]

    fake_api_data = {"days": [{"temp": 28.5}]}
    mock_req_get.return_value.status_code = 200
    mock_req_get.return_value.json.return_value = fake_api_data


    cached_result, status_code = get_weather_location("bangalore")
    print(cached_result)
    assert 'temp' in cached_result.keys()
    assert status_code == 200
    mock_redis.set.assert_called_once_with("weather:bangalore", json.dumps(cached_result),ex=43200)
    assert mock_redis.get.call_count == 2


@patch('app.services.weather.redis_client')
@patch('app.services.utils.client.chat.completions.create')
@patch('app.services.weather.requests.get')
def test_fetch_weather_cache_hit(mock_req_get, mock_exact_name, mock_redis):
    mock_redis.get.return_value = json.dumps({"temp":28.1})

    fake_message = MagicMock()
    fake_message.content = "bangalore"

    fake_choice = MagicMock()
    fake_choice.message = fake_message

    mock_exact_name.return_value.choices = [fake_choice]

    fake_api_data = {"days": [{"temp": 28.5}]}
    mock_req_get.return_value.status_code = 200
    mock_req_get.return_value.json.return_value = fake_api_data


    cached_result, status_code = get_weather_location("bangalore")
    print(cached_result)
    assert 'temp' in cached_result.keys()
    assert status_code == 200
    mock_redis.get.assert_called_once()
    mock_req_get.assert_not_called()

@patch('app.services.weather.redis_client')
@patch('app.services.utils.client.chat.completions.create')
@patch('app.services.weather.requests.get')
def test_fetch_weather_api_error(mock_req_get, mock_exact_name, mock_redis):
    mock_redis.get.return_value = None

    fake_message = MagicMock()
    fake_message.content = "bangalore"

    fake_choice = MagicMock()
    fake_choice.message = fake_message

    mock_exact_name.return_value.choices = [fake_choice]

    fake_api_data = {"days": [{"temp": 28.5}]}
    # mock_req_get.return_value.status_code = 200
    # mock_req_get.return_value.json.return_value = fake_api_data
    mock_req_get.side_effect = requests.exceptions.RequestException("Similitude network failure")


    cached_result, status_code = get_weather_location("bangalore")

    assert status_code == 500
    assert "message" in cached_result.keys()