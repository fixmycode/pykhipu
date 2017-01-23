import requests
from .client import Client
from .responses import BanksResponse


class Banks():
    ENDPOINT = '/banks'

    def __init__(self, client):
        self.client = client

    def get(self):
        response = self.client.make_request('GET', ENDPOINT)
        return BanksResponse.from_response(response.json())
