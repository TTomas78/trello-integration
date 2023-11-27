from fastapi import HTTPException
import requests

class HTTPHandlerService():

    @classmethod
    def request(self, *args, **kwargs):    
        response = requests.request(*args, **kwargs)
        if response.status_code == 400:
            raise HTTPException(status_code=500, detail="There was an error with the request to a third party API")
        if response.status_code in  [401,403]:
            raise HTTPException(status_code=500, detail="Cannot authenticate with a third party API")
        if response.status_code == 404:
            raise HTTPException(status_code=500, detail="Third party API resource not found")
        if response.status_code == 500:
            raise HTTPException(status_code=500, detail="Third party API error")
        if response.status_code == 200 or response.status_code == 201:
            return response
        else:
            raise HTTPException(status_code=500, detail="There was an error related with a third party API")

