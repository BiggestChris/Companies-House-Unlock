import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment
COMPANIES_HOUSE_API_KEY = os.getenv('COMPANIES_HOUSE_API_KEY')

# Function to search for a director in Companies House
def search_director(director_name):
    base_url = 'https://api.company-information.service.gov.uk'
    search_url = f'{base_url}/search/officers?q={director_name}'
    headers = {
        'Authorization': f'Basic {COMPANIES_HOUSE_API_KEY}'
    }

    response = requests.get(search_url, headers=headers, auth=HTTPBasicAuth(COMPANIES_HOUSE_API_KEY, ''))

    if response.status_code == 200:
        # print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def get_director_details(officer_id):
    base_url = 'https://api.company-information.service.gov.uk'
    details_url = f'{base_url}/officers/{officer_id}/appointments'
    auth = HTTPBasicAuth(COMPANIES_HOUSE_API_KEY, '')

    response = requests.get(details_url, auth=auth)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def get_company_details(company_number):
    base_url = 'https://api.company-information.service.gov.uk'
    company_url = f'{base_url}/company/{company_number}'
    auth = HTTPBasicAuth(COMPANIES_HOUSE_API_KEY, '')

    response = requests.get(company_url, auth=auth)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
