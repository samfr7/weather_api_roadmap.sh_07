import logging
import os

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')

    # File handler
    file_handler = logging.FileHandler('logs/weather_api.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger('app')
    root_logger.setLevel(logging.DEBUG)
    root_logger.propagate = False

    # # Silence Flask's default HTTP request logging
    # logging.getLogger('werkzeug').setLevel(logging.WARNING)
    
    # # Silence the requests library connection logging
    # logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    # # (Optional) Silence the Groq LLM API connection logging if it is noisy
    # logging.getLogger('httpx').setLevel(logging.WARNING)

    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)