import requests

def streaming_test():
    url = "http://localhost:5000/streaming"
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=1024):
            print(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def server_signup():
    url = "http://localhost:5000/signup"
    data = {
        "id": 1,
        "name": "user",
        "password": "password1",
        "identity": 1
    }
    try:
        response = requests.get(url, params=data)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    server_signup()