from datetime import date
from typing import Optional

from smart_stock_management.utils.stock_exceptions import InsufficientStockError


class Product:
    """
    Represents a product in the inventory.
    """

    def __init__(
        self,
        product_id: Optional[int],
        name: str,
        price: float,
        stock_quantity: int,
    ):
        self.id = product_id
        self.name = name
        self.price = price
        self._stock_quantity = stock_quantity

    # price validation
    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be numeric")
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        self._price = float(value)

    # stock encapsulation
    @property
    def stock_quantity(self) -> int:
        return self._stock_quantity
    
    def set_stock(self, quantity: int) -> None:
        if not isinstance(quantity, int):
            raise ValueError("Stock quantity must be an integer")
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        self._stock_quantity = quantity


    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce stock by the given quantity.
        """
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if quantity > self._stock_quantity:
            raise InsufficientStockError(
                f"Insufficient stock for product '{self.name}'"
            )

        self._stock_quantity -= quantity


    def increase_stock(self, quantity: int) -> None:
        """
        Increase stock by the given quantity.
        """
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        self._stock_quantity += quantity


    def __repr__(self) -> str:
        return (
            f"Product(id={self.id}, name='{self.name}', "
            f"price={self.price}, stock_quantity={self.stock_quantity})"
        )


class PerishableProduct(Product):
    """
    Represents a perishable product with an expiry date.
    """

    def __init__(
        self,
        product_id: Optional[int],
        name: str,
        price: float,
        stock_quantity: int,
        expiry_date: date,
    ):
        super().__init__(product_id, name, price, stock_quantity)

        if not isinstance(expiry_date, date):
            raise ValueError("expiry_date must be a date object")

        self.expiry_date = expiry_date

    def is_expired(self) -> bool:
        """
        Check if the product is expired.
        """
        return self.expiry_date < date.today()

    def __repr__(self) -> str:
        return (
            f"PerishableProduct(id={self.id}, name='{self.name}', "
            f"price={self.price}, stock_quantity={self.stock_quantity}, "
            f"expiry_date={self.expiry_date})"
        )
