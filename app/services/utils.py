from dotenv import load_dotenv
from groq import Groq
load_dotenv()

def get_exact_location_name(location: str) -> str:
    '''
    This function takes the location name, if there are some issues with this name, then it will correct it and return the location name with the proper name
    '''

    client = Groq()
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

        return location_retrever.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM Normalization failed : {e}")
        return location.strip().lower()


