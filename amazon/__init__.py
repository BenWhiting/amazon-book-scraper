import requests
from amazon.client import Client

class Connection(object):
    def __init__(self, URL=""):
        self.url = URL

    def search(self,  max_pages=0):
        cli = Client()
        cli.get_products(self.url, max_pages)