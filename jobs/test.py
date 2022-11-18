import requests

endpoint = "http://atsbk.afexats.com/api/v1/blogs"
respons = requests.get(endpoint)
print(respons.json())