import requests


def send_post_requests():
    url = "http://localhost:4999/"  # Replace with your endpoint URL

    for i in range(10):
        data = {"msg": f"Message {i + 1}"}  # Constructing data with "msg" parameter
        response = requests.post(url, data=data)

        # Check response status code
        if response.status_code == 200:
            print(f"Request {i + 1} sent successfully.")
        else:
            print(f"Failed to send request {i + 1}. Status code: {response.status_code}")


if __name__ == "__main__":
    send_post_requests()
