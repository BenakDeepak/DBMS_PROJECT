
# Farm Management System

## Overview

The **Farm Management System** is a web-based application designed to manage a farm's operations. This system allows users to manage farmers, workers, farms, crops, equipment, and crop inventory. It includes an admin panel for full CRUD operations, a farmer dashboard for managing farms and responding to workers, and a worker dashboard for sending messages to farmers. The system is built using **Streamlit** for the front end, with **MySQL** as the database for back-end operations.

## Features

- **Admin Panel**: Full control over farmers, workers, farms, equipment, and crops.
- **Farmer Dashboard**:
  - View, add, and edit farmer details.
  - Place equipment orders.
  - Respond to worker messages.
- **Worker Dashboard**: 
  - View farmer details.
  - Send messages to farmers with payment information.
- **User Authentication**: Admin, farmer, and worker roles with specific privileges.
- **Custom Background**: The interface includes a customizable background image for a personalized user experience.

## Technologies Used

- **Frontend**: Streamlit (Python)
- **Backend**: MySQL Database
- **Libraries**: 
  - `Pandas` for data handling.
  - `MySQL Connector` for database interaction.
  - `PIL` for image handling.
  - `Base64` for encoding images.

## Prerequisites

- Python 3.x
- MySQL Server
- Required Python packages (install via `requirements.txt`):
  ```
  streamlit
  mysql-connector-python
  pandas
  pillow
  ```

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-repository/farm-management-system.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up your MySQL database:
   - Create a MySQL database named `farm_management`.
   - Run the provided SQL script to create necessary tables (`Users`, `Farmer`, `Worker`, `Farm`, `Crop`, `Equipment`, `Messages`, etc.).

4. Update the database connection in the `get_connection` function in your script with your MySQL credentials.

   ```python
   def get_connection():
       return mysql.connector.connect(
           host="localhost",
           user="your_mysql_username",
           password="your_mysql_password",
           database="farm_management"
       )
   ```

## How to Run the Application

1. Run the application using Streamlit:

   ```
   streamlit run app.py
   ```

2. Access the application in your browser at:

   ```
   http://localhost:8501
   ```

## How to Use the Application

### Admin Login

- The admin can manage all entities in the system including users, farmers, workers, farms, crops, and equipment. 
- Upon logging in, the admin can navigate the dashboard and choose the table to manage (Users, Farmers, Workers, Farms, Equipment, Crops, Crop Inventory).

### Farmer Login

- A farmer can view their details, manage farm operations, place equipment orders, and respond to worker messages.
- Farmers can also view the crops and crop inventory associated with their farms.

### Worker Login

- Workers can view farmer details and send messages to farmers including payment offers.
- The worker can send job-related queries to farmers and await a response.

## Key Functionalities

### User Authentication
The system allows login for different roles (Admin, Farmer, Worker). Each role has specific privileges:
- **Admin**: Full access to the system for managing all tables.
- **Farmer**: Limited access to manage their own data and respond to workers.
- **Worker**: Ability to view farmers and send messages.

### Admin Dashboard
The admin can:
- View, add, and delete users.
- Manage details of farmers, farms, workers, crops, and crop inventory.
  
### Farmer Dashboard
Farmers can:
- View and edit their own details.
- Place orders for equipment.
- Respond to workers’ messages.

### Worker Dashboard
Workers can:
- View farmers.
- Send messages to farmers along with details of payment offers.

### Message System
Farmers and workers can communicate via the message system. Workers can send messages to farmers with offers, and farmers can reply to these messages.

## Custom Background

You can set a custom background for the application by placing the image file path in the `image_path` variable inside the `get_base64_of_image` function.

```python
image_path = "C:\\path_to_your_image\\background_image.jpg"
```

This image will be displayed as the background of the web application.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributors

- [BENAK DEEPAK] - Project Lead and Developer

---

This README gives users a complete overview of the Farm Management System, how to set it up, and how to use its features. Be sure to update any sections like contributors or GitHub links with actual details from your project.
