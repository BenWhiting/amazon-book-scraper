from .product import Product

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