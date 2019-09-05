class Product(object):
    def __init__(self, product_dict={}):
        self.product = product_dict

    def __getattr__(self, attr):
        return self.product.get(attr, "")