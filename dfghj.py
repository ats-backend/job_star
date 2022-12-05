import requests

endpoint = f"https://assessbk.afexats.com/api/assessment/application-type"

response = requests.get(url=endpoint)
print(response.json())