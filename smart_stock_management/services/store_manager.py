from typing import Dict, List, Optional

from smart_stock_management.models.product import Product
from smart_stock_management.database.product_repository import ProductRepository
from smart_stock_management.database.sales_repository import SalesRepository
from smart_stock_management.utils.stock_exceptions import InsufficientStockError
from smart_stock_management.models.sales import Sale


class StoreManager:
    """
    Core business logic layer for inventory and sales handling.
    """

    LOW_STOCK_THRESHOLD = 5

    def __init__(self) -> None:
        self._products: Dict[int, Product] = {}
        self._load_products()


    def _load_products(self) -> None:
        """
        Load all products from DB into memory for fast lookup.
        """
        products = ProductRepository.get_all_products()
        self._products = {product.id: product for product in products}


    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """
        Fetch a product using O(1) dictionary lookup.
        """
        return self._products.get(product_id)


    def get_low_stock_products(self) -> List[Product]:
        """
        Identify products with low stock.
        """
        return [
            product
            for product in self._products.values()
            if product.stock_quantity < self.LOW_STOCK_THRESHOLD
        ]


    def get_sorted_products_by_price(self) -> List[Product]:
        """
        Return products sorted by price (ascending).
        """
        return sorted(self._products.values(), key=lambda p: p.price)


    def get_sorted_products_by_stock(self) -> List[Product]:
        """
        Return products sorted by stock quantity (ascending).
        """
        return sorted(self._products.values(), key=lambda p: p.stock_quantity)


    def add_product(self, name: str, price: float, stock_quantity: int) -> Product:
        """
        Add a new product to inventory.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string")

        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")

        if not isinstance(stock_quantity, int) or stock_quantity < 0:
            raise ValueError("Stock quantity must be a non-negative integer")

        product_id = ProductRepository.add_product(
            name=name,
            price=price,
            stock_quantity=stock_quantity,
        )

        product = Product(
            product_id=product_id,
            name=name,
            price=price,
            stock_quantity=stock_quantity,
        )

        self._products[product_id] = product

        return product


    def update_product(
        self,
        product_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        stock_quantity: Optional[int] = None,
    ) -> Product:
        """
        Update an existing product.
        """
        product = self.get_product_by_id(product_id)

        if product is None:
            raise ValueError(f"Product with ID {product_id} not found")

        if name is None and price is None and stock_quantity is None:
            raise ValueError("At least one field must be provided for update")

        if name is not None:
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Product name must be a non-empty string")
            product.name = name

        if price is not None:
            product.price = price

        if stock_quantity is not None:
            if not isinstance(stock_quantity, int) or stock_quantity < 0:
                raise ValueError("Stock quantity must be a non-negative integer")
            product.set_stock(stock_quantity)

        ProductRepository.update_product(
            product_id=product.id,
            name=product.name,
            price=product.price,
            stock_quantity=product.stock_quantity,
        )

        return product


    def delete_product(self, product_id: int) -> None:
        """
        Delete a product.
        """
        product = self.get_product_by_id(product_id)

        if product is None:
            raise ValueError(f"Product with ID {product_id} not found")

        ProductRepository.delete_product(product_id)

        del self._products[product_id]

    
    def increase_product_stock(self, product_id: int, quantity: int) -> Product:
        """
        Increase stock of an existing product.
        """
        product = self.get_product_by_id(product_id)

        if product is None:
            raise ValueError(f"Product with ID {product_id} not found")

        product.increase_stock(quantity)

        ProductRepository.update_stock(product_id, product.stock_quantity)

        return product



    def preview_sale(self, product_id: int, quantity: int) -> float:
        """
        Validate sale and return total amount.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

        product = self.get_product_by_id(product_id)

        if product is None:
            raise ValueError(f"Product with ID {product_id} not found")

        if product.stock_quantity < quantity:
            raise InsufficientStockError(
                f"Insufficient stock for product '{product.name}'"
            )

        return product.price * quantity


    def process_sale(self, product_id: int, quantity: int) -> None:
        """
        Process a sale transaction.
        """

        product = self.get_product_by_id(product_id)
        product.reduce_stock(quantity)

        ProductRepository.update_stock(product_id, product.stock_quantity)
        SalesRepository.record_sale(product_id, quantity)


    def get_all_sales(self) -> List[Sale]:
        """
        Return all sales records.
        """
        return SalesRepository.get_all_sales()


    def get_sales_by_product(self, product_id: int) -> List[Sale]:
        """
        Return sales records for a specific product.
        """
        product = self.get_product_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with ID {product_id} not found")

        return SalesRepository.get_sales_by_product(product_id)

