# Introduction
A Lead Management System for Key Account Managers (KAMs) who manage relationships with large restaurant accounts. This system will help track and manage leads, interactions, and account performance.

## System Requirements
1.	Lead Management
-	Add new restaurant leads
-	Store basic restaurant information
-	Track lead status
2.	Contact Management
-	Multiple Points of Contact (POCs) per restaurant
-	Store contact details (name, role, contact information)
-	Support multiple POCs with different roles
3.	Interaction Tracking
-	Record all calls made to leads
-	Track orders placed
-	Store interaction dates and details
4.	Call Planning
-	Set call frequency for each lead
-	Display leads requiring calls today
-	Track last call made
5.	Performance Tracking
-	Track well-performing accounts
-	Monitor ordering patterns and frequency
-	Identify underperforming accounts

## Prerequisites
1. Python3 must be installed
2. virtualenv must be present to create virutal environment for python
3. postgres must be installed in the system, can use PGadmin also

## Installation Instructions
1. Have to create virtual environment in the UDAAN directory after extracting the zip using ```python3 -m virtualenv venv```
2. Activate venv using ```source venv/bin/activate```
3. Install pip packages using ```pip install -r requirements.txt```
4. Run following commands to create models in database:
    ```
    flask db init
    flask db migrate
    flask db upgrade
    ```
5. Data can be imported to database using ```db_input.sql``` file

## Running Instructions
1. Create .env file with list of variables: ```DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME```
2. run the flask application using ```flask run --debug```
3. To access and use the APIs, open ```http://127.0.0.1:5000``` on browser and APIs can be accessed using swagger

## API documentation
Project contains api_documentation.json file in which all apis are defined