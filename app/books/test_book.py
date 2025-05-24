import requests

API_URL = "http://127.0.0.1:8080/book/add_book"

payload = {
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "year": 1937
}

try:
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()  # Викликає виняток для коду статусу 4xx/5xx
    result = response.json()
    print("Book added successfully:", result)
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err} - {response.text}")
except requests.exceptions.RequestException as err:
    print(f"Error connecting to server: {err}")
