from mysql.connector import Error

import mysql.connector

class CommandLigneManager:
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

    def create_commandligne(self, product_id, date, order_id, box_quantity):
        """Create a new command ligne."""
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO commandligne (ProductID, Date, orderID, BoxQuantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (product_id, date, order_id, box_quantity))
            self.connection.commit()
            print("Command ligne created successfully")
        except Error as e:
            print(f"Error: {e}")

    def read_commandligne(self, commandligne_id):
        """Read command ligne details by ID."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM commandligne WHERE ID = %s"
            cursor.execute(query, (commandligne_id,))
            commandligne = cursor.fetchone()
            return commandligne
        except Error as e:
            print(f"Error: {e}")
            return None

    def update_commandligne(self, commandligne_id, product_id=None, date=None, order_id=None, box_quantity=None):
        """Update command ligne details."""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE commandligne SET "
            updates = []
            params = []
            if product_id:
                updates.append("ProductID = %s")
                params.append(product_id)
            if date:
                updates.append("Date = %s")
                params.append(date)
            if order_id:
                updates.append("orderID = %s")
                params.append(order_id)
            if box_quantity:
                updates.append("BoxQuantity = %s")
                params.append(box_quantity)
            query += ", ".join(updates) + " WHERE ID = %s"
            params.append(commandligne_id)
            cursor.execute(query, tuple(params))
            self.connection.commit()
            print("Command ligne updated successfully")
        except Error as e:
            print(f"Error: {e}")

    def delete_commandligne(self, commandligne_id):
        """Delete a command ligne by ID."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM commandligne WHERE ID = %s"
            cursor.execute(query, (commandligne_id,))
            self.connection.commit()
            print("Command ligne deleted successfully")
        except Error as e:
            print(f"Error: {e}")

    def close_connection(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

# Example usage
if __name__ == "__main__":
    manager = CommandLigneManager()

    # Create a command ligne
    manager.create_commandligne(1, "2023-10-01", 1, 10)

    # Read a command ligne
    commandligne = manager.read_commandligne(8)
    if commandligne:
        print(f"Command ligne details: {commandligne}")
    else:
        print("Command ligne not found")

    # Update a command ligne
    manager.update_commandligne(1, box_quantity=20)

    # Delete a command ligne
    
    manager.delete_commandligne(1)

    manager.close_connection()