import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel


class Product(BaseModel):
    ID: int
    Name: str
    Type: str  # We will convert this from datetime to string
    Price: float
    Quantity: int
    SupplierID: int

class ProductsManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',  # Replace with your MySQL username
                password='',  # Replace with your MySQL password
                database='gs'
            )
            if self.connection.is_connected():
                print("Connected to the database")
        except Error as e:
            print(f"Error: {e}")
            self.connection = None

    def create_product(self, name, type, price, quantity, supplier_id):
        """Create a new product."""
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO products (Name, Type, Price, Quantity, SupplierID) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, type, price, quantity, supplier_id))
            self.connection.commit()
            return "Product created successfully"
        except Error as e:
            return f"Error: {e}"

    def read_products(self, product_id=None):
        """Read product details by ID."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if product_id is None:
                query = "SELECT * FROM products"
                cursor.execute(query)
                products = cursor.fetchall()
                products_list = [Product(**product) for product in products]
                return products_list
            else:
                query = "SELECT * FROM products WHERE ID = %s"
                cursor.execute(query, (product_id,))
                product = cursor.fetchone()
                return Product(**product) if product else None
        except Error as e:
                return f"Error: {e}"

    def update_product(self, product_id, name=None, type=None, price=None, quantity=None, supplier_id=None):
        """Update product details."""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE products SET "
            updates = []
            params = []
            if name:
                updates.append("Name = %s")
                params.append(name)
            if type:
                updates.append("Type = %s")
                params.append(type)
            if price:
                updates.append("Price = %s")
                params.append(price)
            if quantity:
                updates.append("Quantity = %s")
                params.append(quantity)
            if supplier_id:
                updates.append("SupplierID = %s")
                params.append(supplier_id)
            query += ", ".join(updates) + " WHERE ID = %s"
            params.append(product_id)
            cursor.execute(query, tuple(params))
            self.connection.commit()
            return "Product updated successfully"
        except Error as e:
            return f"Error: {e}"

    def delete_product(self, product_id):
        """Delete a product by ID."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM products WHERE ID = %s"
            cursor.execute(query, (product_id,))
            self.connection.commit()
            return "Product deleted successfully"
        except Error as e:
            return f"Error: {e}"

    def close_connection(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

    def alert(self):
        """Fetch all products with quantity 0."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM products WHERE Quantity = 0"
            cursor.execute(query)
            products = cursor.fetchall()
            products_list = [Product(**product) for product in products]
            return products_list
        except Error as e:
            return f"Error: {e}"
        
# Example usage
if __name__ == "__main__":

    manager = ProductsManager()

    # Create a product
    manager.create_product("Example Product", "Example Type", 19.99, 100, 1)

    # Read a product
    product = manager.read_products()
    if product:
        print(f"Product details: {product}")
    else:
        print("Product not found")

    # Update a product
    manager.update_product(1, price=24.99, quantity=150, supplier_id=2)

    # Delete a product
    manager.delete_product(1)

    manager.close_connection()