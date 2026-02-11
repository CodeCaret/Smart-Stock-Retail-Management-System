from typing import List
from datetime import datetime

from smart_stock_management.database.connection import get_connection
from smart_stock_management.models.sales import Sale


class SalesRepository:
    """
    Repository responsible for SalesLog persistence.
    """

    @staticmethod
    def record_sale(product_id: int, quantity_sold: int) -> int:
        """
        Insert a sales record into the SalesLog table.
        Returns the generated sale_id.
        """
        query = """
        INSERT INTO SalesLog (product_id, quantity_sold)
        VALUES (?, ?)
        """

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, (product_id, quantity_sold))
        connection.commit()

        sale_id = cursor.lastrowid
        connection.close()

        return sale_id


    @staticmethod
    def get_all_sales() -> List[Sale]:
        """
        Fetch all sales records.
        Returns a list of Sale objects.
        """
        query = """
        SELECT sale_id, product_id, quantity_sold, timestamp
        FROM SalesLog
        ORDER BY timestamp DESC
        """

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()

        return [
            Sale(
                sale_id=row["sale_id"],
                product_id=row["product_id"],
                quantity_sold=row["quantity_sold"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
            )
            for row in rows
        ]

    @staticmethod
    def get_sales_by_product(product_id: int) -> List[Sale]:
        """
        Fetch sales records for a specific product.
        Returns a list of Sale objects.
        """
        query = """
        SELECT sale_id, product_id, quantity_sold, timestamp
        FROM SalesLog
        WHERE product_id = ?
        ORDER BY timestamp DESC
        """

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, (product_id,))
        rows = cursor.fetchall()
        connection.close()

        return [
            Sale(
                sale_id=row["sale_id"],
                product_id=row["product_id"],
                quantity_sold=row["quantity_sold"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
            )
            for row in rows
        ]
