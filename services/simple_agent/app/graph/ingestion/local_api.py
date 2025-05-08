import requests
import os

LOCAL_API_ENDPOINT = os.environ.get("LOCAL_API_ENDPOINT")

def call_local_api(endpoint="/"):
    try:
        full_endpoint = f"{LOCAL_API_ENDPOINT}{endpoint}"
        response = requests.get(full_endpoint)
        if response.status_code == 200:
            return response.json()["message"]
        else:
            return {"error": "Failed to fetch data from local API"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
    
if __name__ == "__main__":
    # Example usage
    endpoint = "/"  # Replace with your desired endpoint
    result = call_local_api(endpoint)
    print(result)