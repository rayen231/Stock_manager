from mysql.connector import Error

import mysql.connector
from pydantic import BaseModel


class Supplier(BaseModel):
    ID: int
    Name: str
    Adress: str  # We will convert this from datetime to string
    Contact: int


class SupplierManager:
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

    def create_supplier(self, name, adress, contact):
        """Create a new supplier."""
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Supplier (Name, Adress, Contact) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, adress, contact))
            self.connection.commit()
            return "Supplier created successfully"
        except Error as e:
            return f"Error: {e}"

    def read_supplier(self, supplier_id=None):
        """Read supplier details by ID."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if supplier_id is None:
                query = "SELECT * FROM Supplier"
                cursor.execute(query)
                suppliers = cursor.fetchall()
                suppliers_list = [Supplier(**supplier) for supplier in suppliers]
                return suppliers_list
            
            else:

                query = "SELECT * FROM Supplier WHERE ID = %s"
                cursor.execute(query, (supplier_id,))
                supplier = cursor.fetchone()
                return Supplier(**supplier)
            
        except Error as e:
            print(f"Error: {e}")
            return None

    def update_supplier(self, supplier_id, name=None, adress=None, contact=None):
        """Update supplier details."""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Supplier SET "
            updates = []
            params = []
            if name:
                updates.append("Name = %s")
                params.append(name)
            if adress:
                updates.append("Adress = %s")
                params.append(adress)
            if contact:
                updates.append("Contact = %s")
                params.append(contact)
            query += ", ".join(updates) + " WHERE ID = %s"
            params.append(supplier_id)
            cursor.execute(query, tuple(params))
            self.connection.commit()
            return "Supplier updated successfully"
        except Error as e:
            return f"Error: {e}"

    def delete_supplier(self, supplier_id):
        """Delete a supplier by ID."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Supplier WHERE ID = %s"
            cursor.execute(query, (supplier_id,))
            self.connection.commit()
            return "Supplier deleted successfully"
        except Error as e:
            return f"Error: {e}"

    def close_connection(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

# Example usage
if __name__ == "__main__":

    manager = SupplierManager()

    # Create a supplier
    manager.create_supplier("Example Supplier", "123 Example St", "123-456-7890")

    # Read a supplier
    supplier = manager.read_supplier(1)
    if supplier:
        print(f"Supplier details: {supplier}")
    else:
        print("Supplier not found")

    # Update a supplier
    manager.update_supplier(1, adress="456 New Adress", contact="987-654-3210")

    # Delete a supplier
    manager.delete_supplier(1)

    manager.close_connection()