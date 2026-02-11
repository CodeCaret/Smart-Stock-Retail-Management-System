from datetime import datetime

from smart_stock_management.services.store_manager import StoreManager
from smart_stock_management.utils.stock_exceptions import InsufficientStockError
from smart_stock_management.database.initializer import initialize_database
from smart_stock_management.models.product import PerishableProduct

# input helpers
def read_int(prompt: str, min_value: int | None = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value must be >= {min_value}")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")


def read_float(prompt: str, min_value: float | None = None) -> float:
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value <= min_value:
                print(f"Value must be > {min_value}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def read_non_empty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


# menu actions
def display_product(product):
    print(
        f"""
----------------------------------------
Product ID      : {product.id}
Name            : {product.name}
Price           : ₹{product.price:.2f}
Stock Quantity  : {product.stock_quantity}
----------------------------------------
"""
    )


from datetime import timezone
from zoneinfo import ZoneInfo

def convert_utc_to_ist(utc_dt):

    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)

    return utc_dt.astimezone(ZoneInfo("Asia/Kolkata"))


def display_sale(sale):

    local_time = convert_utc_to_ist(sale.timestamp)

    print(f"""
----------------------------------------
Sale ID     : {sale.id}
Product ID  : {sale.product_id}
Quantity    : {sale.quantity_sold}
Time        : {local_time.strftime("%Y-%m-%d %I:%M:%S %p")}
----------------------------------------
""")



def add_product_flow(manager: StoreManager) -> None:
    name = read_non_empty_string("Enter product name: ")
    price = read_float("Enter price: ", min_value=0)
    quantity = read_int("Enter stock quantity: ", min_value=0)

    product = manager.add_product(name, price, quantity)
    print(f"Product added successfully!")
    display_product(product=product)


def update_product_flow(manager: StoreManager) -> None:
    product_id = read_int("Enter product ID to update: ", min_value=1)

    product = manager.get_product_by_id(product_id)
    if product is None:
        print(f"Product with ID {product_id} not found.")
        return

    print("Leave input blank if you don't want to update a field.")

    name = input("New name: ").strip()
    price_input = input("New price: ").strip()
    stock_input = input("New stock quantity: ").strip()

    kwargs = {}

    if name:
        kwargs["name"] = name

    if price_input:
        try:
            kwargs["price"] = float(price_input)
        except ValueError:
            print("Invalid price. Update aborted.")
            return

    if stock_input:
        try:
            kwargs["stock_quantity"] = int(stock_input)
        except ValueError:
            print("Invalid stock quantity. Update aborted.")
            return

    if not kwargs:
        print("No fields provided for update.")
        return

    updated_product = manager.update_product(product_id, **kwargs)
    print(f"Product updated successfully!")
    display_product(product=updated_product)



def delete_product_flow(manager: StoreManager) -> None:
    product_id = read_int("Enter product ID to delete: ", min_value=1)

    if manager.get_product_by_id(product_id) is None:
        print(f"Product with ID {product_id} not found.")
        return

    manager.delete_product(product_id)
    print("Product deleted successfully.")


def increase_stock_flow(manager: StoreManager) -> None:
    product_id = read_int("Enter product ID: ", min_value=1)

    product = manager.get_product_by_id(product_id)
    if product is None:
        print(f"Product with ID {product_id} not found.")
        return
    
    quantity = read_int("Enter quantity: ", min_value=1)

    try:
        product = manager.increase_product_stock(product_id, quantity)
        print("\nStock updated successfully!")
        display_product(product)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def process_sale_flow(manager: StoreManager) -> None:
    product_id = read_int("Enter product ID: ", min_value=1)

    product = manager.get_product_by_id(product_id)
    if product is None:
        print(f"Product with ID {product_id} not found.")
        return

    quantity = read_int("Enter quantity sold: ", min_value=1)

    try:
        total_amount = manager.preview_sale(product_id, quantity)

        print(f"\nTotal amount to pay: ₹{total_amount:.2f}")
        confirm = input("Do you want to proceed? (y/n): ").strip().lower()

        if confirm != "y":
            print("Transaction cancelled.")
            return

        manager.process_sale(product_id, quantity)
        print("Sale processed successfully.")

        if product.stock_quantity < manager.LOW_STOCK_THRESHOLD:
            print(
                f"ALERT: '{product.name}' is low on stock "
                f"(Remaining: {product.stock_quantity})"
            )

    except InsufficientStockError as e:
        print(e)
    except ValueError as e:
        print(e)


def list_low_stock_products(manager: StoreManager) -> None:
    products = manager.get_low_stock_products()

    if not products:
        print("No low-stock products.")
        return

    print("\nLow-stock products are:")
    for product in products:
        display_product(product=product)


def list_products_sorted(manager: StoreManager) -> None:
    print("\n1. Sort by price")
    print("2. Sort by stock quantity")

    choice = read_int("Choose sorting option: ", min_value=1)

    if choice == 1:
        products = manager.get_sorted_products_by_price()
    elif choice == 2:
        products = manager.get_sorted_products_by_stock()
    else:
        print("Invalid choice.")
        return

    print("\n--- Sorted Products ---")
    for product in products:
        display_product(product=product)


def check_expiry_flow(manager: StoreManager) -> None:
    product_id = read_int("Enter product ID: ", min_value=1)

    product = manager.get_product_by_id(product_id)
    if product is None:
        print(f"Product with ID {product_id} not found.")
        return

    expiry_input = input("Enter expiry date (YYYY-MM-DD): ").strip()

    try:
        expiry_date = datetime.strptime(expiry_input, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    perishable_product = PerishableProduct(
        product.id,
        product.name,
        product.price,
        product.stock_quantity,
        expiry_date,
    )

    if perishable_product.is_expired():
        print(f"Product '{product.name}' is EXPIRED.")
    else:
        print(f"Product '{product.name}' is NOT expired.")


def view_all_sales_flow(manager: StoreManager) -> None:
    sales = manager.get_all_sales()

    if not sales:
        print("No sales records found.")
        return

    print("\n\n--- Sales Records ---")
    for sale in sales:
        display_sale(sale=sale)


def view_sales_by_product_flow(manager: StoreManager) -> None:
    product_id = read_int("Enter product ID: ", min_value=1)

    product = manager.get_product_by_id(product_id)
    if product is None:
        print(f"Product with ID {product_id} not found.")
        return
    
    sales = manager.get_sales_by_product(product_id)

    if not sales:
        print(f"No sales records found for product ID {product_id}.")
        return

    print(f"\n\n--- Sales for Product ID {product_id} ---")
    for sale in sales:
        display_sale(sale=sale)


# main menu
def main() -> None:
    initialize_database()
    manager = StoreManager()

    try:
        while True:
            print("\n\n=== QuickCart Smart-Stock Retail Management System ===\n")
            print("1. Add product")
            print("2. Update product")
            print("3. Delete product")
            print("4. Increase Stock")
            print("5. Process sale")
            print("6. View low-stock products")
            print("7. View all products")
            print("8. Check product expiry")
            print("9. View All Sales")
            print("10. View Sales By Product")
            print("0. Exit")

            choice = read_int("Enter your choice: ")

            try:
                if choice == 1:
                    add_product_flow(manager)
                elif choice == 2:
                    update_product_flow(manager)
                elif choice == 3:
                    delete_product_flow(manager)
                elif choice == 4:
                    increase_stock_flow(manager)
                elif choice == 5:
                    process_sale_flow(manager)
                elif choice == 6:
                    list_low_stock_products(manager)
                elif choice == 7:
                    list_products_sorted(manager)
                elif choice == 8:
                    check_expiry_flow(manager)
                elif choice == 9:
                    view_all_sales_flow(manager)
                elif choice == 10:
                    view_sales_by_product_flow(manager)
                elif choice == 0:
                    print("\nGoodbye!")
                    break
                else:
                    print("Invalid option.")

            except Exception as e:
                print(f"Error: {e}")

    except KeyboardInterrupt:
        print("\nCtrl+c detected, Closing Gracefully!")
        print("\nGoodbye!")

