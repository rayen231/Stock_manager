from mysql.connector import Error
import mysql.connector
from pydantic import BaseModel
from datetime import date
from pydantic import BaseModel, Field

class Order(BaseModel):
    ID: int
    Date: str  # We will convert this from datetime to string
    Total: int
    SupplierID: float
    Status: str

class OrderManager:
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

    def create_order(self, date, total, supplier_id, status):
        """Create a new order."""
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO `order` (Date, Total, SupplierID, Status) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (date, total, supplier_id, status))
            self.connection.commit()
            return " Order created successfully"
        except Error as e:
            return f"Error: {e}"

    def read_order(self, order_id="empty"):
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if order_id == "empty":
                print("order_id is None")
                query = "SELECT * FROM `order`"
                cursor.execute(query)
                orders = cursor.fetchall()
                orders_list = []
                for order in orders:
                    order['Date'] = order['Date'].isoformat()  # Convert date to string
                    orders_list.append(Order(**order))
                return orders_list
            
            else:
                query = "SELECT * FROM `order` WHERE ID = %s"
                cursor.execute(query, (order_id,))
                order = cursor.fetchone()
                if order:
                    order['Date'] = order['Date'].isoformat()
                    return Order(**order)
                return None
            
        except Error as e:
            print(f"Error: {e}")
            return None


    def update_order(self, order_id, date=None, total=None, supplier_id=None, status=None):
        """Update order details."""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE `order` SET "
            updates = []
            params = []
            if date:
                updates.append("Date = %s")
                params.append(date)
            if total:
                updates.append("Total = %s")
                params.append(total)
            if supplier_id:
                updates.append("SupplierID = %s")
                params.append(supplier_id)
            if status:
                updates.append("Status = %s")
                params.append(status)
            query += ", ".join(updates) + " WHERE ID = %s"
            params.append(order_id)
            cursor.execute(query, tuple(params))
            self.connection.commit()
            return "Order updated successfully"
        except Error as e:
            return f"Error: {e}"

    def delete_order(self, order_id):
        """Delete an order by ID."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM `order` WHERE ID = %s"
            cursor.execute(query, (order_id,))
            self.connection.commit()
            return "Order deleted successfully"
        except Error as e:
            return f"Error: {e}"

    def close_connection(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

# Example usage
if __name__ == "__main__":
    manager = OrderManager()

    # Create an order
    #manager.create_order("2023-10-01", 100.0, 1, "Pending")

    # Read an order
    # order = manager.read_order(2)
    # if order:
    #     print(f"Order details: {order}")
    # else:
    #     print("Order not found")

    # # Update an order
    manager.update_order(8, total=150.0, status="Completed")

    # # Delete an order
    # #manager.delete_order(1)

    #print(manager.read_order())

    # manager.close_connection()