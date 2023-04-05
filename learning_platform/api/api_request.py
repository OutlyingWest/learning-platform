import requests


data = {
    "email": " test38@example.com ",
    "birthday": "2022-08-20",
    "description": "Разработал 5 персональных сайтов для фотографа, travel-агентства, SMM-агентства. "
                   "Имею большой опыт в реализации сложных проектов",
    "name": "Никита Кукиш",
    "password": "password5729562356238"
}
response = requests.post(url='http://127.0.0.1:8000/api/users/', data=data,
                         files={'avatar': open('/home/alex/downloads/ava.jpg', 'rb')})
print(response.text, response.status_code)
