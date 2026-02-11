from typing import List, Optional

from smart_stock_management.database.connection import get_connection
from smart_stock_management.models.product import Product


class ProductRepository:
    """
    Repository responsible for Product persistence.
    """

    @staticmethod
    def add_product(name: str, price: float, stock_quantity: int) -> int:
        query = """
        INSERT INTO Products (name, price, stock_quantity)
        VALUES (?, ?, ?)
        """

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, (name, price, stock_quantity))
        connection.commit()

        product_id = cursor.lastrowid
        connection.close()

        return product_id


    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[Product]:
        """
        Fetch a product by ID.
        Returns a Product object.
        """
        query = """
        SELECT id, name, price, stock_quantity
        FROM Products
        WHERE id = ?
        """

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, (product_id,))
        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return Product(
            product_id=row["id"],
            name=row["name"],
            price=row["price"],
            stock_quantity=row["stock_quantity"],
        )


    @staticmethod
    def get_all_products() -> List[Product]:
        """
        Fetch all products from the database.
        Returns a list of Product object.
        """
        query = """
        SELECT id, name, price, stock_quantity
        FROM Products
        """

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()

        return [
            Product(
                product_id=row["id"],
                name=row["name"],
                price=row["price"],
                stock_quantity=row["stock_quantity"],
            )
            for row in rows
        ]

    @staticmethod
    def update_stock(product_id: int, new_stock: int) -> None:
        """
        Update stock quantity.
        """
        query = """
        UPDATE Products
        SET stock_quantity = ?
        WHERE id = ?
        """

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, (new_stock, product_id))
        connection.commit()
        connection.close()


    @staticmethod
    def update_product(
        product_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        stock_quantity: Optional[int] = None,
    ) -> None:
        """
        Update product details.
        Only provided fields will be updated.
        """

        updates = []
        params = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)

        if price is not None:
            updates.append("price = ?")
            params.append(price)

        if stock_quantity is not None:
            updates.append("stock_quantity = ?")
            params.append(stock_quantity)

        if not updates:
            raise ValueError("No fields provided to update.")

        query = f"""
        UPDATE Products
        SET {', '.join(updates)}
        WHERE id = ?
        """

        params.append(product_id)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, tuple(params))
        connection.commit()
        connection.close()


    @staticmethod
    def delete_product(product_id: int) -> None:
        """
        Delete product.
        """
        query = """
        DELETE FROM Products
        WHERE id = ?
        """

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, (product_id,))
        connection.commit()

        if cursor.rowcount == 0:
            connection.close()
            raise ValueError(f"Product with ID {product_id} not found.")

        connection.close()
