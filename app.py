import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="benak@2010",
        database="FarmManagement"
    )

# Function to execute query and return results
def run_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    conn.close()
    return pd.DataFrame(data, columns=columns)

# Function to execute an update/insert query
def run_action(query, values):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    conn.close()

# Streamlit App
st.title("Farm Management Admin Panel")

# Sidebar Navigation
pages = ["Farmers", "Farms", "Employee", "Equipment", "Crops", "Crop Inventory"]
page = st.sidebar.selectbox("Choose a page", pages)

if page == "Farmers":
    st.header("Farmers")
    action = st.selectbox("Choose action", ["View", "Add", "Edit", "Delete"])

    if action == "View":
        df = run_query("SELECT * FROM Farmer")
        st.write(df)

    elif action == "Add":
        with st.form("Add Farmer"):
            name = st.text_input("Name")
            address = st.text_input("Address")
            contact_info = st.text_input("Contact Info")
            submitted = st.form_submit_button("Add Farmer")
            if submitted:
                run_action("INSERT INTO Farmer (name, address, contact_info) VALUES (%s, %s, %s)", (name, address, contact_info))
                st.success("Farmer added successfully")

    elif action == "Edit":
        farmers = run_query("SELECT farmer_id, name FROM Farmer")
        farmer_dict = {row['name']: row['farmer_id'] for index, row in farmers.iterrows()}
        farmer_name = st.selectbox("Choose a farmer to edit", list(farmer_dict.keys()))
        farmer_id = farmer_dict[farmer_name]
        farmer = run_query(f"SELECT * FROM Farmer WHERE farmer_id = {farmer_id}").iloc[0]

        with st.form("Edit Farmer"):
            name = st.text_input("Name", value=farmer['name'])
            address = st.text_input("Address", value=farmer['address'])
            contact_info = st.text_input("Contact Info", value=farmer['contact_info'])
            submitted = st.form_submit_button("Update Farmer")
            if submitted:
                run_action("UPDATE Farmer SET name = %s, address = %s, contact_info = %s WHERE farmer_id = %s", (name, address, contact_info, farmer_id))
                st.success("Farmer updated successfully")

    elif action == "Delete":
        farmers = run_query("SELECT farmer_id, name FROM Farmer")
        farmer_dict = {row['name']: row['farmer_id'] for index, row in farmers.iterrows()}
        farmer_name = st.selectbox("Choose a farmer to delete", list(farmer_dict.keys()))
        farmer_id = farmer_dict[farmer_name]

        if st.button("Delete Farmer"):
            run_action("DELETE FROM Farmer WHERE farmer_id = %s", (farmer_id,))
            st.success("Farmer deleted successfully")

elif page == "Farms":
    st.header("Farms")
    action = st.selectbox("Choose action", ["View", "Add", "Edit", "Delete"])

    if action == "View":
        df = run_query("SELECT * FROM Farm")
        st.write(df)

    elif action == "Add":
        farmers = run_query("SELECT farmer_id, name FROM Farmer")
        farmer_dict = {row['name']: row['farmer_id'] for index, row in farmers.iterrows()}
        with st.form("Add Farm"):
            location = st.text_input("Location")
            size = st.number_input("Size", min_value=0.0, step=0.01)
            farmer_name = st.selectbox("Farmer", list(farmer_dict.keys()))
            submitted = st.form_submit_button("Add Farm")
            if submitted:
                farmer_id = farmer_dict[farmer_name]
                run_action("INSERT INTO Farm (location, size, farmer_id) VALUES (%s, %s, %s)", (location, size, farmer_id))
                st.success("Farm added successfully")

    elif action == "Edit":
        farms = run_query("SELECT farm_id, location FROM Farm")
        farm_dict = {row['location']: row['farm_id'] for index, row in farms.iterrows()}
        farm_location = st.selectbox("Choose a farm to edit", list(farm_dict.keys()))
        farm_id = farm_dict[farm_location]
        farm = run_query(f"SELECT * FROM Farm WHERE farm_id = {farm_id}").iloc[0]
        farmers = run_query("SELECT farmer_id, name FROM Farmer")
        farmer_dict = {row['name']: row['farmer_id'] for index, row in farmers.iterrows()}

        with st.form("Edit Farm"):
            location = st.text_input("Location", value=farm['location'])
            size = st.number_input("Size", value=farm['size'], min_value=0.0, step=0.01)
            farmer_name = st.selectbox("Farmer", list(farmer_dict.keys()))
            submitted = st.form_submit_button("Update Farm")
            if submitted:
                farmer_id = farmer_dict[farmer_name]
                run_action("UPDATE Farm SET location = %s, size = %s, farmer_id = %s WHERE farm_id = %s", (location, size, farmer_id, farm_id))
                st.success("Farm updated successfully")

    elif action == "Delete":
        farms = run_query("SELECT farm_id, location FROM Farm")
        farm_dict = {row['location']: row['farm_id'] for index, row in farms.iterrows()}
        farm_location = st.selectbox("Choose a farm to delete", list(farm_dict.keys()))
        farm_id = farm_dict[farm_location]

        if st.button("Delete Farm"):
            run_action("DELETE FROM Farm WHERE farm_id = %s", (farm_id,))
            st.success("Farm deleted successfully")
elif page == "Crop Inventory":
    st.header("Crop Inventory")
    action = st.selectbox("Choose action", ["View", "Add", "Edit", "Delete"])

    if action == "View":
        df = run_query("SELECT * FROM crop_inventory")
        st.write(df)

    elif action == "Add":
        crops = run_query("SELECT crop_id, crop_name FROM Crop")
        crop_dict = {row['crop_name']: row['crop_id'] for index, row in crops.iterrows()}
        with st.form("Add Crop Inventory"):
            crop_name = st.selectbox("Crop", list(crop_dict.keys()))
            quantity = st.number_input("Quantity", min_value=0.0, step=0.01)
            storage_location = st.text_input("Storage Location")
            submitted = st.form_submit_button("Add Inventory")
            if submitted:
                crop_id = crop_dict[crop_name]
                run_action("INSERT INTO crop_inventory (crop_id, quantity, storage_location) VALUES (%s, %s, %s)", 
                           (crop_id, quantity, storage_location))
                st.success("Crop inventory added successfully")

    elif action == "Edit":
        inventories = run_query("SELECT inventory_id, crop_id FROM crop_inventory")
        inventory_dict = {row['inventory_id']: row['crop_id'] for index, row in inventories.iterrows()}
        inventory_id = st.selectbox("Choose an inventory item to edit", list(inventory_dict.keys()))
        inventory = run_query(f"SELECT * FROM crop_inventory WHERE inventory_id = {inventory_id}").iloc[0]
        crops = run_query("SELECT crop_id, crop_name FROM Crop")
        crop_dict = {row['crop_name']: row['crop_id'] for index, row in crops.iterrows()}

        with st.form("Edit Crop Inventory"):
            crop_name = st.selectbox("Crop", list(crop_dict.keys()))
            quantity = st.number_input("Quantity", value=inventory['quantity'], min_value=0.0, step=0.01)
            storage_location = st.text_input("Storage Location", value=inventory['storage_location'])
            submitted = st.form_submit_button("Update Inventory")
            if submitted:
                crop_id = crop_dict[crop_name]
                run_action("UPDATE crop_inventory SET crop_id = %s, quantity = %s, storage_location = %s WHERE inventory_id = %s", 
                           (crop_id, quantity, storage_location, inventory_id))
                st.success("Crop inventory updated successfully")

    elif action == "Delete":
        inventories = run_query("SELECT inventory_id, crop_id FROM crop_inventory")
        inventory_dict = {row['inventory_id']: row['crop_id'] for index, row in inventories.iterrows()}
        inventory_id = st.selectbox("Choose an inventory item to delete", list(inventory_dict.keys()))

        if st.button("Delete Inventory"):
            run_action("DELETE FROM crop_inventory WHERE inventory_id = %s", (inventory_id,))
            st.success("Crop inventory deleted successfully")
elif page == "Crops":
    st.header("Crops")
    action = st.selectbox("Choose action", ["View", "Add", "Edit", "Delete"])

    if action == "View":
        df = run_query("SELECT * FROM Crop")
        st.write(df)

    elif action == "Add":
        with st.form("Add Crop"):
            crop_name = st.text_input("Crop Name")
            variety = st.text_input("Variety")
            planting_date = st.date_input("Planting Date")
            expected_harvest_date = st.date_input("Expected Harvest Date")
            submitted = st.form_submit_button("Add Crop")
            if submitted:
                run_action("INSERT INTO Crop (crop_name, variety, planting_date, expected_harvest_date) VALUES (%s, %s, %s, %s)", 
                           (crop_name, variety, planting_date, expected_harvest_date))
                st.success("Crop added successfully")

    elif action == "Edit":
        crops = run_query("SELECT crop_id, crop_name FROM Crop")
        crop_dict = {row['crop_name']: row['crop_id'] for index, row in crops.iterrows()}
        crop_name = st.selectbox("Choose a crop to edit", list(crop_dict.keys()))
        crop_id = crop_dict[crop_name]
        crop = run_query(f"SELECT * FROM Crop WHERE crop_id = {crop_id}").iloc[0]

        with st.form("Edit Crop"):
            crop_name = st.text_input("Crop Name", value=crop['crop_name'])
            variety = st.text_input("Variety", value=crop['variety'])
            planting_date = st.date_input("Planting Date", value=crop['planting_date'])
            expected_harvest_date = st.date_input("Expected Harvest Date", value=crop['expected_harvest_date'])
            submitted = st.form_submit_button("Update Crop")
            if submitted:
                run_action("UPDATE Crop SET crop_name = %s, variety = %s, planting_date = %s, expected_harvest_date = %s WHERE crop_id = %s", 
                           (crop_name, variety, planting_date, expected_harvest_date, crop_id))
                st.success("Crop updated successfully")

    elif action == "Delete":
        crops = run_query("SELECT crop_id, crop_name FROM Crop")
        crop_dict = {row['crop_name']: row['crop_id'] for index, row in crops.iterrows()}
        crop_name = st.selectbox("Choose a crop to delete", list(crop_dict.keys()))
        crop_id = crop_dict[crop_name]

        if st.button("Delete Crop"):
            run_action("DELETE FROM Crop WHERE crop_id = %s", (crop_id,))
            st.success("Crop deleted successfully")
elif page == "Employee":
    st.header("Employee")
    action = st.selectbox("Choose action", ["View", "Add", "Edit", "Delete"])

    if action == "View":
        df = run_query("SELECT * FROM Employee")
        st.write(df)

    elif action == "Add":
        with st.form("Add Employee"):
            name = st.text_input("Name")
            contact_info = st.text_input("Contact Info")
            farm_id = st.selectbox("Farm ID", options=run_query("SELECT farm_id FROM Farm")["farm_id"].tolist())
            submitted = st.form_submit_button("Add Employee")
            if submitted:
                run_action("INSERT INTO Employee (name, contact_info, farm_id) VALUES (%s, %s, %s)", (name, contact_info, farm_id))
                st.success("Employee added successfully")

    elif action == "Edit":
        employees = run_query("SELECT employee_id, name FROM Employee")
        employee_dict = {row['name']: row['employee_id'] for index, row in employees.iterrows()}
        employee_name = st.selectbox("Choose an employee to edit", list(employee_dict.keys()))
        employee_id = employee_dict[employee_name]
        employee = run_query(f"SELECT * FROM Employee WHERE employee_id = {employee_id}").iloc[0]

        with st.form("Edit Employee"):
            name = st.text_input("Name", value=employee['name'])
            contact_info = st.text_input("Contact Info", value=employee['contact_info'])
            farm_id = st.selectbox("Farm ID", options=run_query("SELECT farm_id FROM Farm")["farm_id"].tolist(), index=run_query(f"SELECT farm_id FROM Employee WHERE employee_id = {employee_id}").iloc[0])
            submitted = st.form_submit_button("Update Employee")
            if submitted:
                run_action("UPDATE Employee SET name = %s, contact_info = %s, farm_id = %s WHERE employee_id = %s", (name, contact_info, farm_id, employee_id))
                st.success("Employee updated successfully")

    elif action == "Delete":
        employees = run_query("SELECT employee_id, name FROM Employee")
        employee_dict = {row['name']: row['employee_id'] for index, row in employees.iterrows()}
        employee_name = st.selectbox("Choose an employee to delete", list(employee_dict.keys()))
        employee_id = employee_dict[employee_name]

        if st.button("Delete Employee"):
            run_action("DELETE FROM Employee WHERE employee_id = %s", (employee_id,))
            st.success("Employee deleted successfully")
elif page == "Equipment":
    st.header("Equipment")
    action = st.selectbox("Choose action", ["View", "Add", "Edit", "Delete"])

    if action == "View":
        df = run_query("SELECT * FROM Equipment")
        st.write(df)

    elif action == "Add":
        with st.form("Add Equipment"):
            equipment_name = st.text_input("Equipment Name")
            description = st.text_input("Description")
            farm_id = st.selectbox("Farm ID", options=run_query("SELECT farm_id FROM Farm")["farm_id"].tolist())
            submitted = st.form_submit_button("Add Equipment")
            if submitted:
                run_action("INSERT INTO Equipment (equipment_name, description, farm_id) VALUES (%s, %s, %s)", (equipment_name, description, farm_id))
                st.success("Equipment added successfully")

    elif action == "Edit":
        equipment = run_query("SELECT equipment_id, equipment_name FROM Equipment")
        equipment_dict = {row['equipment_name']: row['equipment_id'] for index, row in equipment.iterrows()}
        equipment_name = st.selectbox("Choose equipment to edit", list(equipment_dict.keys()))
        equipment_id = equipment_dict[equipment_name]
        equipment = run_query(f"SELECT * FROM Equipment WHERE equipment_id = {equipment_id}").iloc[0]

        with st.form("Edit Equipment"):
            equipment_name = st.text_input("Equipment Name", value=equipment['equipment_name'])
            description = st.text_input("Description", value=equipment['description'])
            farm_id = st.selectbox("Farm ID", options=run_query("SELECT farm_id FROM Farm")["farm_id"].tolist(), index=run_query(f"SELECT farm_id FROM Equipment WHERE equipment_id = {equipment_id}").iloc[0])
            submitted = st.form_submit_button("Update Equipment")
            if submitted:
                run_action("UPDATE Equipment SET equipment_name = %s, description = %s, farm_id = %s WHERE equipment_id = %s", (equipment_name, description, farm_id, equipment_id))
                st.success("Equipment updated successfully")

    elif action == "Delete":
        equipment = run_query("SELECT equipment_id, equipment_name FROM Equipment")
        equipment_dict = {row['equipment_name']: row['equipment_id'] for index, row in equipment.iterrows()}
        equipment_name = st.selectbox("Choose equipment to delete", list(equipment_dict.keys()))
        equipment_id = equipment_dict[equipment_name]

        if st.button("Delete Equipment"):
            run_action("DELETE FROM Equipment WHERE equipment_id = %s", (equipment_id,))
            st.success("Equipment deleted successfully")
elif page == "Crop Inventory":
    st.header("Crop Inventory")
    action = st.selectbox("Choose action", ["View", "Add", "Edit", "Delete"])

    if action == "View":
        df = run_query("SELECT * FROM Crop_Inventory")
        st.write(df)

    elif action == "Add":
        crops = run_query("SELECT crop_id, crop_name FROM Crop")
        crop_dict = {row['crop_name']: row['crop_id'] for index, row in crops.iterrows()}
        with st.form("Add Crop Inventory"):
            crop_name = st.selectbox("Crop", list(crop_dict.keys()))
            quantity = st.number_input("Quantity", min_value=0.0, step=0.01)
            storage_location = st.text_input("Storage Location")
            submitted = st.form_submit_button("Add Inventory")
            if submitted:
                crop_id = crop_dict[crop_name]
                run_action("INSERT INTO Crop_Inventory (crop_id, quantity, storage_location) VALUES (%s, %s, %s)", 
                           (crop_id, quantity, storage_location))
                st.success("Crop inventory added successfully")

    elif action == "Edit":
        inventories = run_query("SELECT inventory_id, crop_id FROM CropInventory")
        inventory_dict = {row['inventory_id']: row['crop_id'] for index, row in inventories.iterrows()}
        inventory_id = st.selectbox("Choose an inventory item to edit", list(inventory_dict.keys()))
        inventory = run_query(f"SELECT * FROM CropInventory WHERE inventory_id = {inventory_id}").iloc[0]
        crops = run_query("SELECT crop_id, crop_name FROM Crop")
        crop_dict = {row['crop_name']: row['crop_id'] for index, row in crops.iterrows()}

        with st.form("Edit Crop Inventory"):
            crop_name = st.selectbox("Crop", list(crop_dict.keys()))
            quantity = st.number_input("Quantity", value=inventory['quantity'], min_value=0.0, step=0.01)
            storage_location = st.text_input("Storage Location", value=inventory['storage_location'])
            submitted = st.form_submit_button("Update Inventory")
            if submitted:
                crop_id = crop_dict[crop_name]
                run_action("UPDATE CropInventory SET crop_id = %s, quantity = %s, storage_location = %s WHERE inventory_id = %s", 
                           (crop_id, quantity, storage_location, inventory_id))
                st.success("Crop inventory updated successfully")

    elif action == "Delete":
        inventories = run_query("SELECT inventory_id, crop_id FROM CropInventory")
        inventory_dict = {row['inventory_id']: row['crop_id'] for index, row in inventories.iterrows()}
        inventory_id = st.selectbox("Choose an inventory item to delete", list(inventory_dict.keys()))

        if st.button("Delete Inventory"):
            run_action("DELETE FROM CropInventory WHERE inventory_id = %s", (inventory_id,))
            st.success("Crop inventory deleted successfully")
