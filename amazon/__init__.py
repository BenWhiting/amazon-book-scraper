import requests
from amazon.client import Client

_HOST_URL = "www.amazon.com"
_DEFAULT_USER_AGENT = ""
_CHROME_DEKSTOP_USER_AGENT = ""
_ACCEPT = "text/html,application/xhtml+xml,\
    application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"


_USER_AGENT_LIST = [
    _DEFAULT_USER_AGENT,
    _CHROME_DEKSTOP_USER_AGENT,
]

class Connection(object):
    def __init__(self, URL=""):
        self.url = URL

    def search(self,  max_product=100):
        cli = Client()
        cli.get_products(self.url, max_product)