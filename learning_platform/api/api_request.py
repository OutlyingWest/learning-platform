import requests
import base64
from requests.auth import HTTPBasicAuth


data = {
    "email": " test38@example.com ",
    "birthday": "2022-08-20",
    "description": "Разработал 5 персональных сайтов для фотографа, travel-агентства, SMM-агентства. "
                   "Имею большой опыт в реализации сложных проектов",
    "name": "Никита Кукиш",
    "password": "password5729562356238"
}

auth_data = {
    'username': 'alexeybuv7@gmail.com',
    'password': '123450',
}

# userpass = '{0}:{1}'.format(auth_data['username'], auth_data['password'])
# userpass_encoded = base64.b64encode(userpass.encode()).decode()
# print(userpass_encoded)

# response = requests.get(url='http://127.0.0.1:8000/api/users/',
#                         headers={'Authorization': '9c2e27e6cbd2bf9d3019981146488e20a597dcc9'})

response = requests.post(url='http://127.0.0.1:8000/api/generate-token/', data=auth_data)

print(response.text, response.status_code)
