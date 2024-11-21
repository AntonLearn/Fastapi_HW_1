import requests
from config import URL_USER, URL_ADVERTISEMENT


#response = requests.post(url=f"{URL_USER}/", json={"name": "User 2", "password": "Password_2"})
#response = requests.post(url=f"{URL_ADVERTISEMENT}/", json={"header": "Advertisement 2", "owner_id": 2, "description": "Description 2"})
#response = requests.post(url=f"{URL_ADVERTISEMENT}/", json={"header": "Advertisement 3", "owner_id": 1, "description": "Description 3"})

#response = requests.get(url=f"{URL_USER}/1")
#response = requests.get(url=f"{URL_USER}/99")
#response = requests.get(url=f"{URL_ADVERTISEMENT}/1")
#response = requests.get(url=f"{URL_ADVERTISEMENT}/99")

#response = requests.delete(url=f"{URL_USER}/1")
#response = requests.delete(url=f"{URL_ADVERTISEMENT}/1")

#response = requests.patch(url=f'{URL_USER}/1', json={"name": "User 1"})
#response = requests.patch(url=f"{URL_USER}/1", json={"header": "Advertisement_1", "description": "Description_1"})

#response = requests.get(url=f"{URL_USER}/?page=2&size=1")
#response = requests.get(url=f"{URL_USER}/?page=1&size=1&user_id=2&name=User 2&registration_time=2024-11-20T03:47:31.997853")
#response = requests.get(url=f"{URL_ADVERTISEMENT}/")

response = requests.get(url=f"{URL_USER}/")
#response = requests.get(url=f"{URL_ADVERTISEMENT}/")

#response = requests.get(url=f"{URL_USER}/?page=7")

#response = requests.get(url=f"{URL_USER}/?user_id=2")
#response = requests.get(url=f"{URL_ADVERTISEMENT}/?advertisement_id=2")

#response = requests.get(url=f"{URL_USER}/?name=User 5")

print(response.json())