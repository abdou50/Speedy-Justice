import requests
import json

url = 'http://127.0.0.1:5000/signup'

data = {
    'username': 'Achref',
    'email': 'achrefhaddaji95@gmail.com',
    'password': '123456789',
    'password_confirmation': '123456789',
    'phone': '123456789',
    'address': '123456789',
    'city': '123456789',
    'country': '123456789',
    'postal_code': '123456789',
    'role': 'Kharray'
}

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)
print(r.text)