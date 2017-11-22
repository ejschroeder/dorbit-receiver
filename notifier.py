import requests

def notify(url, message):
    response = requests.post(url, data = message)
    return response.status_code
