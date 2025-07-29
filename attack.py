import requests
import time
import threading

# --- Configuration ---
BASE_URL = "http://127.0.0.1:3000"
LOGIN_URL = f"{BASE_URL}/auth/login"
TARGET_URL = f"{BASE_URL}/tasks/"

# --- Credentials for a test user ---
# Make sure this user exists in your database
USERNAME = "milon@gmail"
PASSWORD = "pass"

# --- Attack Parameters ---
REQUEST_COUNT = 20  # Total requests to send
CONCURRENCY = 5     # Number of threads to use

def get_auth_token():
    """Logs in to get a JWT token."""
    print(f"Attempting to log in as {USERNAME}...")
    try:
        response = requests.post(LOGIN_URL, data={"username": USERNAME, "password": PASSWORD})
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("Login successful. Token obtained.")
            return token
        else:
            print(f"Login failed! Status: {response.status_code}, Response: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("Login failed. Connection error. Is the server running?")
        return None

def make_request(session, headers, i):
    """Sends a single request to the target URL."""
    task_data = {
        "title": f"Attack Task {i}",
        "description": "This is a test task from the attack script.",
        "is_done": False
    }
    try:
        response = session.post(TARGET_URL, headers=headers, json=task_data)
        print(
            f"Request #{i + 1}: "
            f"Status: {response.status_code} -> "
            f"{response.text[:100]}..."
        )
    except requests.exceptions.RequestException as e:
        print(f"Request #{i + 1}: Connection Error - {e}")

def flood_server():
    token = get_auth_token()
    if not token:
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\nStarting attack: Sending {REQUEST_COUNT} requests to {TARGET_URL} with {CONCURRENCY} threads.\n")

    with requests.Session() as session:
        threads = []
        for i in range(REQUEST_COUNT):
            thread = threading.Thread(target=make_request, args=(session, headers, i))
            threads.append(thread)
            thread.start()
            # Small delay to avoid overwhelming the client machine, not the server
            time.sleep(0.05)

        for thread in threads:
            thread.join()

    print("\nAttack finished.")

if __name__ == "__main__":
    flood_server()
