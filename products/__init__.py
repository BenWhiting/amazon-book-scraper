from .product import Product
import csv
from .search import *

class Products(object):
    def __init__(self, product_dict_list=[]):
        self.products = []
        self.last_html_page = ""
        self.html_pages =[]
        for product_dict in product_dict_list:
            self._add_product(product_dict)

    def _add_product(self, prodict_dict):
        p = Product(prodict_dict)
        self.products.append(p)

    def __len__(self):
        return len(self.products)

    def __getitem(self, key):
        return self.products[key]
    
    def csv(self, file_name, separator=","):
        if not self.products:
            return
        
        with open(file_name, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=separator)

            header = list(self.products[0].product.keys())
            writer.writerow(header)

            for product in self.products:
                writer.writerow(list(product.product.values()))