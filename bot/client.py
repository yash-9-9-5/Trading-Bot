import requests
from typing import Dict, Any
from bot.logging_config import logger

BASE_URL = "https://httpbin.org" #httpbin.org is a simple HTTP request & response service that can be used for testing and debugging. 

class MockClient: #mock client
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]: #method to handle http requests
        if params is None:
            params = {}

        url = f"{BASE_URL}{endpoint}"
        logger.debug(f"Sending {method} request to {url} with data: {params}")
        
        try:
            if method == "POST":
                # Using json=params sends a direct JSON REST call
                response = self.session.post(url, json=params)
            elif method == "GET":
                response = self.session.get(url, params=params)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response: {data}")
            return data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Error: {e}")
            raise
