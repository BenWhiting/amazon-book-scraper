import requests
from amazon.client import Client

class Connection(object):
    def __init__(self, URL=""):
        self.url = URL

    def scrape_search_pages(self):
        cli = Client()
        return cli.initial_scan(self.url)