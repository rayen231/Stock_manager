import streamlit as st
import requests

# Base URLs for the APIs
BASE_URLS = {
    "Product Service": "http://127.0.0.1:8083",
    "Supplier Service": "http://127.0.0.1:8084",
    "Command Line Service": "http://127.0.0.1:8081",
    "Order Service": "http://127.0.0.1:8082",
}

# Sidebar Navigation
service = st.sidebar.selectbox("Select a Service", list(BASE_URLS.keys()))
st.title(f"{service} Dashboard")

# Handle Product Service
if service == "Product Service":
    endpoint = st.selectbox("Select Endpoint", ["/products", "/products/{id}", "/products/create", "/products/update/{id}", "/products/delete/{id}"])
    
    if endpoint == "/products":
        if st.button("Get All Products"):
            response = requests.get(f"{BASE_URLS[service]}{endpoint}")
            st.json(response.json())

    elif endpoint == "/products/{id}":
        product_id = st.number_input("Product ID", value=1)
        if st.button("Get Product"):
            response = requests.get(f"{BASE_URLS[service]}/products/{product_id}")
            st.json(response.json())

    elif endpoint == "/products/create":
        name = st.text_input("Name")
        type_ = st.text_input("Type")
        price = st.number_input("Price", value=0.0)
        quantity = st.number_input("Quantity", value=0)
        supplier_id = st.number_input("Supplier ID", value=1)
        if st.button("Create Product"):
            data = {"ID": 0, "Name": name, "Type": type_, "Price": price, "SupplierID": supplier_id, "Quantity": quantity}
            response = requests.post(f"{BASE_URLS[service]}{endpoint}", json=data)
            st.write(response.text)

    # Add sections for update and delete as needed...
    elif endpoint == "/products/update/{id}":
        product_id = st.number_input("Product ID", value=1)
        name = st.text_input("Name")
        type_ = st.text_input("Type")
        price = st.number_input("Price", value=0.0)
        quantity = st.number_input("Quantity", value=0)
        supplier_id = st.number_input("Supplier ID", value=1)
        if st.button("Update Product"):
            data = {"ID": product_id, "Name": name, "Type": type_, "Price": price, "SupplierID": supplier_id, "Quantity": quantity}
            response = requests.put(f"{BASE_URLS[service]}{endpoint}", json=data)
            st.write(response.text)

    elif endpoint == "/products/delete/{id}":
        product_id = st.number_input("Product ID", value=1)
        if st.button("Delete Product"):
            response = requests.delete(f"{BASE_URLS[service]}{endpoint}")
            st.write(response.text)

# Handle Supplier Service
elif service == "Supplier Service":
    endpoint = st.selectbox("Select Endpoint", ["/suppliers", "/suppliers/{id}", "/suppliers"])
    
    if endpoint == "/suppliers":
        if st.button("Get All Suppliers"):
            response = requests.get(f"{BASE_URLS[service]}{endpoint}")
            st.json(response.json())

    elif endpoint == "/suppliers/{id}":
        supplier_id = st.number_input("Supplier ID", value=1)
        if st.button("Get Supplier"):
            response = requests.get(f"{BASE_URLS[service]}/suppliers/{supplier_id}")
            st.json(response.json())

    # Add sections for create, update, and delete...
    elif endpoint == "/suppliers":
        name = st.text_input("Name")
        if st.button("Create Supplier"):
            data = {"ID": 0, "Name": name}
            response = requests.post(f"{BASE_URLS[service]}{endpoint}", json=data)
            st.write(response.text)

    elif endpoint == "/suppliers/{id}":
        supplier_id = st.number_input("Supplier ID", value=1)
        name = st.text_input("Name")
        if st.button("Update Supplier"):
            data = {"ID": supplier_id, "Name": name}
            response = requests.put(f"{BASE_URLS[service]}{endpoint}", json=data)
            st.write(response.text)

# Handle Command Line Service
elif service == "Command Line Service":
    endpoint = st.selectbox("Select Endpoint", ["/commandligne/", "/commandligne/{id}"])
    
    if endpoint == "/commandligne/":
        product_id = st.number_input("Product ID", value=1)
        date = st.text_input("Date (YYYY-MM-DD)")
        order_id = st.number_input("Order ID", value=1)
        box_quantity = st.number_input("Box Quantity", value=1)
        if st.button("Create Command Line"):
            data = {"product_id": product_id, "date": date, "order_id": order_id, "box_quantity": box_quantity}
            response = requests.post(f"{BASE_URLS[service]}{endpoint}", json=data)
            st.write(response.json())

    # Add sections for read, update, and delete...
    elif    endpoint == "/commandligne/{id}":
        command_id = st.number_input("Command ID", value=1)
        product_id = st.number_input("Product ID", value=1)
        date = st.text_input("Date (YYYY-MM-DD)")
        order_id = st.number_input("Order ID", value=1)
        box_quantity = st.number_input("Box Quantity", value=1)
        if st.button("Update Command Line"):
            data = {"ID": command_id, "product_id": product_id, "date": date, "order_id": order_id, "box_quantity": box_quantity}
            response = requests.put(f"{BASE_URLS[service]}{endpoint}", json=data)
            st.write(response.json())

    elif endpoint == "/commandligne/{id}":
        command_id = st.number_input("Command ID", value=1)
        if st.button("Delete Command Line"):
            response = requests.delete(f"{BASE_URLS[service]}{endpoint}")
            st.write(response.json())

# Handle Order Service
elif service == "Order Service":
    endpoint = st.selectbox("Select Endpoint", ["/orders", "/orders/{id}"])
    
    if endpoint == "/orders":
        if st.button("Get All Orders"):
            response = requests.get(f"{BASE_URLS[service]}{endpoint}")
            st.json(response.json())

    elif endpoint == "/orders/{id}":
        order_id = st.number_input("Order ID", value=1)
        if st.button("Get Order"):
            response = requests.get(f"{BASE_URLS[service]}/orders/{order_id}")
            st.json(response.json())

    # Add sections for create, update, and delete...
    elif endpoint == "/orders":
        date = st.text_input("Date (YYYY-MM-DD)")
        if st.button("Create Order"):
            data = {"ID": 0, "Date": date}
            response = requests.post(f"{BASE_URLS[service]}{endpoint}", json=data)
            st.write(response.json())
            
    elif endpoint == "/orders/{id}":
        order_id = st.number_input("Order ID", value=1)
        date = st.text_input("Date (YYYY-MM-DD)")
        if st.button("Update Order"):
            data = {"ID": order_id, "Date": date}
            response = requests.put(f"{BASE_URLS[service]}{endpoint}", json=data)
            st.write(response.json())

