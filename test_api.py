import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import base64

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment
COMPANIES_HOUSE_API_KEY = os.getenv('COMPANIES_HOUSE_API_KEY')

# Ensure the API key is correctly loaded
if not COMPANIES_HOUSE_API_KEY:
    raise ValueError("COMPANIES_HOUSE_API_KEY not found in environment variables")

# Function to search for a director in Companies House
def search_director(director_name):
    base_url = 'https://api.company-information.service.gov.uk'
    search_url = f'{base_url}/search/officers?q={director_name}'
    
    # Print the API key to debug
    print(f"Using API Key: {COMPANIES_HOUSE_API_KEY}")

    # Basic Auth header in Base64 format
    auth_string = base64.b64encode(f"{COMPANIES_HOUSE_API_KEY}:".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_string}'
    }

    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage for testing
search_director("Christopher Stylianou")
