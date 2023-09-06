## Table of Contents
* [Description](#description)
* [Features](#features)
* [Technologies](#technologies)
* [Installation](#installation)
* [Users](#users)
* [Usage](#usage)
* [Database](#database)
* [Validation](#validation)

## Description
The Television and Tests Management Web Application is a Flask-based web application that allows users to manage a database of television and test records. Users can view, add, edit, and delete records, and perform user registration and login. The application also includes both client-side and server-side validation to ensure data integrity and security.
The intended use of the application is for developers to keep track of television specifications and test case criteria.
## Features
* **User Registration and Login:** Users can register for an account and log in to access the application's features.
* **View Televisions and Tests List:** Users can view a list of television records.
* **Add Televisions and Tests Records:** Users can add new television records to the database.
* **Edit Televisions and Tests Records:** Users can edit new records they have made as long as they're within the same session. Else, they will need to ask an Admin to edit their records.
* **Delete Televisions and Tests Records:** Users can delete television records.
* **Admin Approval Dashboard:** Admin Users can approve other users to become an Admin.
* **Client-side Validation:** The application includes client-side validation for all inputs throughout the application, and it validates input data to prevent inappropriate characters and ensure data integrity by disabling submit buttons.
* **Server-side Validation:** The application includes server-side validation for all inputs throughout the application, and it validates input data to prevent inappropriate characters and ensure data integrity.
* **User Authentication:** User authentication is implemented to protect certain functionalities, such as editing and deleting records, for authorized users.

## Technologies
* Flask: A micro web framework for Python.
* SQLite: A lightweight, serverless database engine.
* HTML/CSS: For the frontend of the application.
* Python: The programming language used to build the backend logic.
* Jinja2: A template engine for rendering HTML templates.

## Installation
1. Clone this repository to your local machine.
2. Create a virtual environment for the project (optional but recommended).
3. Run the Flask application by executing `python app.py` from the project's root directory.

## Users
The examiner can log in as an admin user with these credentials:
* Username: `admin` 
* Password: `Admin123?`

Or the examiner can register a new account, by default this is a regular user and they would need to be approved by an admin using the Approval Dashboard.
## Usage
* Access the application by opening a web browser and navigating to `http://localhost:5000/`.
* Register for a new user account or log in if you already have one.
* Use the application to manage television and test records, including adding, editing, and deleting (admin only) records.

## Database
* The application uses SQLite as its database engine.
* The database schema includes a `users` table for storing regular and admin user information, a `televisions` table for storing television records and a `tests` table for storing test records.
* SQLite is serverless and uses a local file (`database.db`) for data storage.

## Validation
* Server-side and Client-side validation is implemented for user registration, ensuring that usernames and passwords meet specified criteria.
* All inputs for television and test records also need to meet specified criteria.
* Input data is validated to prevent inappropriate characters and ensure data integrity.
* Validation messages are provided to users for feedback on data input.
