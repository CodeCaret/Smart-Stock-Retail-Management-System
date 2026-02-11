from datetime import datetime
from typing import Optional


class Sale:
    """
    Represents a single sale transaction.
    """

    def __init__(
        self,
        sale_id: Optional[int],
        product_id: int,
        quantity_sold: int,
        timestamp: datetime,
    ):
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("product_id must be a positive integer")

        if not isinstance(quantity_sold, int) or quantity_sold <= 0:
            raise ValueError("quantity_sold must be a positive integer")

        if not isinstance(timestamp, datetime):
            raise ValueError("timestamp must be a datetime object")

        self.id = sale_id
        self.product_id = product_id
        self.quantity_sold = quantity_sold
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return (
            f"Sale(id={self.id}, product_id={self.product_id}, "
            f"quantity_sold={self.quantity_sold}, timestamp={self.timestamp})"
        )
