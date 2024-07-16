1) git clone this respository https://github.com/BenakDeepak/college_project1/
2) type this command in MySQL-
CREATE DATABASE FarmManagement;
USE FarmManagement;
CREATE TABLE Farmer ( 
farmer_id INT PRIMARY KEY, 
name VARCHAR(100) NOT NULL,
 address VARCHAR(255),
 contact_info VARCHAR(255) );
CREATE TABLE Farm ( 
farm_id INT PRIMARY KEY,
 location VARCHAR(255), 
size DECIMAL(10, 2), 
farmer_id INT, FOREIGN KEY (farmer_id) REFERENCES Farmer(farmer_id) 
);
4) type this command where the repository(terminal) is stored->  py -m venv env
   env.Scripts.activate.bat()
   pip install mysql-connector-python
   pip install streamlit
   pip install pandas
6) type this command for admin panel -  streamlit run app.py
