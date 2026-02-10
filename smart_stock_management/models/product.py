class Product:
    def __init__(self, product_id, name, price, stock_quantity):
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be numeric")
        if not isinstance(stock_quantity, int):
            raise ValueError("Stock quantity must be an integer")

        self.id = product_id
        self.name = name
        self.price = price
        self._stock_quantity = stock_quantity  # protected

    @property
    def stock_quantity(self):
        return self._stock_quantity

    def reduce_stock(self, quantity):
        if quantity > self._stock_quantity:
            raise InsufficientStockError("Not enough stock available")
        self._stock_quantity -= quantity



from datetime import date

class PerishableProduct(Product):
    def __init__(self, product_id, name, price, stock_quantity, expiry_date):
        super().__init__(product_id, name, price, stock_quantity)
        self.expiry_date = expiry_date  # date object
