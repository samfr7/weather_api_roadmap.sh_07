# Weather API

A Flask-based REST API that provides real-time weather information with intelligent location processing and caching capabilities.

## Features

- **Weather Data Endpoint**: Get current weather conditions for any location
- **Intelligent Location Processing**: Uses Groq LLM to correct location names and handle spelling mistakes
- **Redis Caching**: 12-hour cache for frequently requested locations to reduce API calls
- **CORS Support**: Cross-origin resource sharing enabled for frontend integration
- **Rate Limiting**: Built-in rate limiting to protect the API
- **Comprehensive Temperature Data**: Returns temp, feels-like, max, and min temperatures

## Technology Stack

- **Framework**: Flask
- **Caching**: Redis
- **Weather Data**: Visual Crossing Weather API
- **LLM Processing**: Groq API (for location name correction)
- **Language**: Python

## API Endpoints

### Get Weather for a Location

```
GET /weather/<location>
```

**Parameters:**
- `location` (string, required): The location name (city, region, or address)

**Response:**
```json
{
  "tempmax": 28.5,
  "tempmin": 18.2,
  "temp": 23.4,
  "feelslike": 24.1,
  "feelslikemax": 29.2,
  "feelslikemin": 17.5
}
```

**Example:**
```bash
curl http://localhost:5000/weather/London
```

## Setup & Installation

### Prerequisites

- Python 3.7+
- Redis (for caching functionality)
- API Keys:
  - [Visual Crossing Weather API](https://www.visualcrossing.com/weather-api) - Free tier available
  - [Groq API](https://groq.com) - For LLM-based location processing

### Installation Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd weather_api_roadmap.sh_07
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install flask flask-cors flask-limiter python-dotenv requests groq redis
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   API_KEY=your_visual_crossing_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

5. Start Redis server (required for caching):
   ```bash
   redis-server
   ```

6. Run the application:
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## Project Structure

```
weather_api_roadmap.sh_07/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration settings
│   ├── extensions.py            # CORS and rate limiting setup
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py            # API endpoint definitions
│   └── services/
│       ├── __init__.py
│       ├── weather.py           # Weather data fetching and caching logic
│       └── utils.py             # Utility functions (location name correction)
├── run.py                       # Application entry point
├── .env                         # Environment variables (API keys)
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## How It Works

1. **Client Request**: User requests weather for a location
2. **Redis Check**: API checks if the location is cached (12-hour TTL)
3. **Location Processing**: If not cached, location name is processed using Groq LLM to correct spelling/short forms
4. **Redis Check (2nd)**: Checks cache again with corrected location name
5. **External API Call**: If still not cached, fetches data from Visual Crossing Weather API
6. **Cache Storage**: Caches the result in Redis for 12 hours
7. **Response**: Returns temperature data to the client

## Error Handling

- 500: External API request failed (network issues or Visual Crossing API down)
- 400/404: Invalid location or location not found

## License

MIT License - See [LICENSE](LICENSE) file for details

## Author

Samuel Frank (2026)