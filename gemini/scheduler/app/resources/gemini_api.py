import dagster as dg
import requests 

from gemini.config.settings import GEMINISettings
from typing import Any, Dict

class GEMINIRESTAPI(dg.ConfigurableResource):
    api_host: str = GEMINISettings().GEMINI_REST_API_HOSTNAME
    api_port: int = GEMINISettings().GEMINI_REST_API_PORT

    def get(self, endpoint: str, params: dict = {}) -> Dict[str, Any]:
        url = f"http://{self.api_host}:{self.api_port}/{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Return the JSON response as a dictionary
        except requests.exceptions.RequestException as e:
            # Handle request exceptions
            raise RuntimeError(f"Failed to get data from {url}: {str(e)}") from e
        
        


