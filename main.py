import requests
from datetime import datetime as dt
import os

APP_ID = os.environ.get('APP_ID')
API_KEY = os.environ.get('API_KEY')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

exercise_endpoint = os.environ.get('exercise_endpoint')
sheets_endpoint = os.environ.get('sheets_endpoint')


GENDER = 'male'
WEIGHT_KG = '86.2'
HEIGHT_CM = '182'
AGE = '38'

# Exercise NLP POST request

post_headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
    'Content-Type': 'application/json'
}

post_body = {
    "query": input("Enter activity: "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, headers=post_headers, json=post_body)
response.raise_for_status()
data = response.json()

duration = data['exercises'][0]['duration_min']
calories = data['exercises'][0]['nf_calories']
name = data['exercises'][0]['name']
# Google Sheet API POST request
# Date	Time	Exercise	Duration	Calories

sheety_headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {BEARER_TOKEN}'
}

sheets_body = {
    'workout': {
        'date': dt.now().date().strftime('%m/%d/%Y'),
        'time': dt.now().time().strftime('%H:%M:%S'),
        'exercise': name.title(),
        'duration': duration,
        'calories': calories,
    }
}

response = requests.post(
    sheets_endpoint,
    headers=sheety_headers,
    json=sheets_body
)
print(response.json())
