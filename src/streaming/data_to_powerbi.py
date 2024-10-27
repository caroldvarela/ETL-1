import requests
from decouple import config

def send_to_powerbi(row):
    url = config('POWERBI_API')
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json={"rows": [row]})
    if response.status_code != 200:
        print(f"Error sending data to Power BI: {response.text}")

    print('Message sent to powerbi\n')
