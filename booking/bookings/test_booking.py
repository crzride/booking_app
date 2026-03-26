import requests
import threading

URL = "http://127.0.0.1:8000/api/bookings/"

HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc0NDIwNzk1LCJpYXQiOjE3NzQ0MjA0OTUsImp0aSI6IjY5YjU3NjI5MDMzNTQ4YTI5ODIyY2E1N2NjZWIxMjdmIiwidXNlcl9pZCI6IjEifQ.Red5O4o0iNL-kcANtHBU1fqTzg563C7FiFpGNb1rdx4"
}

DATA = {
    "room": 1,
    "rooms_count": 1,
    "guest_number": 2,
    "check_in": "2026-04-01",
    "check_out": "2026-04-05"
}


def send_request():
    response = requests.post(URL, json=DATA, headers=HEADERS)
    print(response.status_code, response.text)


threads = []

for i in range(5):
    t = threading.Thread(target=send_request)
    threads.append(t)
    t.start()

for t in threads:
    t.join()