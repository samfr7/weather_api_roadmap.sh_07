from dotenv import load_dotenv
from groq import Groq
load_dotenv()
import logging

logger = logging.getLogger(__name__)

# its recommended that we define these variables outside as its defines once the program runs and it available, if its inside it needs to define again and again
client = Groq()

def get_exact_location_name(location: str) -> str:
    '''
    This function takes the location name, if there are some issues with this name, then it will correct it and return the location name with the proper name
    '''
    logger.debug(f"Attempting to fetch the right name for location: {location}!")
    
    try:
        location_retrever = client.chat.completions.create(
            messages=[
                {
                    'role':'system',
                    'content': '''
    You are a strict geolocation normalization data-processor. Your sole objective is to resolve user input into a valid, canonical city name.

    RULES:
    1. Return EXACTLY and ONLY the resolved city name. Do not include any conversational text, greetings, explanations, or punctuation.
    2. The entire output MUST be strictly in lowercase.
    3. Resolve common abbreviations and acronyms to their full city names.
    4. Correct spelling mistakes accurately.
    5. Map historical, local, or alternative names to their most widely recognized standard English name.
    6. If the input is complete gibberish or clearly not a geographic location, return the exact string: "invalid".

    EXAMPLES:
    Input: hyd
    Output: hyderabad

    Input: bglore
    Output: bangalore

    Input: bengaluru
    Output: bangalore

    Input: nyc
    Output: new york city

    Input: new york city
    Output: new york city

    Input: san fran
    Output: san francisco

    Input: bombay
    Output: mumbai

    Input: sdfksdfj
    Output: invalid
                    
    '''
                },
                {
                    'role':'user',
                    'content':f'{location}'
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )
        location = location_retrever.choices[0].message.content.strip()
        logger.debug(f"The right name for the location is {location}")
        return location
    except Exception as e:
        logger.warning(f"Attempt failed to fetch data for location: {location}! Returning the same location")
        return location.strip().lower()


