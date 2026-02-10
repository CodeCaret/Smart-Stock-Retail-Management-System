    def process_sale(self, product_id, quantity):
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be numeric")

        product = self.products.get(product_id)
        if not product:
            raise ValueError("Product not found")

        # business logic
        product.reduce_stock(quantity)

        # update DB (atomic operation)
        self.cursor.execute(
            "UPDATE products SET stock_quantity = ? WHERE id = ?",
            (product.stock_quantity, product_id)
        )

        self.cursor.execute(
            "INSERT INTO sales_log (product_id, quantity_sold) VALUES (?, ?)",
            (product_id, quantity)
        )

        self.conn.commit()


    def low_stock_alert(self, threshold=5):
        return [
            product for product in self.products.values()
            if product.stock_quantity < threshold
        ]
