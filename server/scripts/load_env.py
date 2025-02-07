# !FIX ME: still note set env variable in .env file
import os

from dotenv import find_dotenv, load_dotenv

# Load the .env file
load_dotenv(find_dotenv(), override=True)

print(f"Test load value of SERPAPI_API_KEY: {os.getenv('SERPAPI_API_KEY')}")
