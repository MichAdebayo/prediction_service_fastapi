import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URL of your FastAPI server
base_url = "http://127.0.0.1:8000"

# Authentication token (ensure you have a valid token from the `/auth/login` endpoint)
auth_token_test = os.getenv("AUTH_TOKEN_TEST")


# Loan request data
loan_request_data = {
    "state": "CA",
    "bank": "JP MORGAN",
    "naics": 92,
    "term": 36,
    "no_emp": 19,
    "new_exist": 1,
    "create_job": 30,
    "retained_job": 25,
    "urban_rural": 1,
    "rev_line_cr": 0,
    "low_doc": 0,
    "gr_appv": 170000,
    "recession": 0,
    "has_franchise": 0
}

# Headers for the request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {auth_token_test}"
}

# Send POST request to the `/loans/request` endpoint
response = requests.post(
    f"{base_url}/loans/request",
    json=loan_request_data,
    headers=headers
)

# Print the response
print("Loan Request Response:")
print(response.json())