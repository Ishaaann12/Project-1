'''
import httpx

url = "http://127.0.0.1:8000/run"
data = {"task": "Fetch API data"}  # Ensure correct JSON format

response = httpx.post(url, json=data)  # Sending JSON body properly
print(response.status_code, response.json())  # See what FastAPI returns
'''

from tasks import format_markdown # Import your function

print(format_markdown())  # Run it manually
