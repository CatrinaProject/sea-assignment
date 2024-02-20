## Table of Contents
* [Description](#description)
* [Functionality](#functionality)
* [Features](#features)
  * [Validation](#validation)
  * [Admin/Regular Roles](#adminregular-roles)
  * [Database](#database)
* [Technologies](#technologies)
* [Installation](#installation)
* [Usage](#usage)


## Description
The Television and Tests Management Web Application is a Flask-based web application that allows users to manage a database of television and test records. Users can view, add, edit, and delete records, and perform user registration and login. The application also includes both client-side and server-side validation to ensure data integrity and security.
The intended use of the application is for developers to keep track of television specifications and test case criteria.

## Functionality
* **User Registration and Login:** Users can register for an account and log in to access the application's features.
* **View Televisions and Tests List:** Users can view a list of television records.
* **Add Televisions and Tests Records:** Users can add new television records to the database.
* **Edit Televisions and Tests Records:** Users can edit new records they have made as long as they're within the same session. Else, they will need to ask an Admin to edit their records.
* **Delete Televisions and Tests Records:** Users can delete television records.
* **Admin Approval Dashboard:** Admin Users can approve other regular users to become an Admin.

## Features
### Validation
* Server-side and Client-side validation is implemented for user registration, ensuring that usernames and passwords meet specified criteria.
  * Username criteria:
    * Minimum length of 5 characters
    * Alphabetical characters only
  * Password criteria:
    * Minimum length of 5 characters
    * At least one uppercase letter
    * At least one lowercase letter
    * At least one digit (number)
    * At least one special character (non-alphanumeric)
* All inputs for television and test records also need to meet specified criteria. Input data is validated to prevent inappropriate characters and ensure data integrity.
  * Input criteria:
    * No special characters (/\-.,']+$)
    * Alpha-numerical characters only
    * Maximum length of 50 characters
    * Tests.Duration field has additional criteria, it can only be a decimal to 5 units and 2 decimal places
* Validation error messages are provided to users for feedback on data input, if their inputs are invalid the submit button is disabled and an error message is displayed.
* Confirmation notification banners are implemented when editing and deleting records which ask the user to confirm their actions before the database is updated.

### Admin/Regular Roles
User authentication is implemented to protect certain functionalities, such as editing and deleting records, for authorized users.

_Marking each feature as a CRUD operation_

**Regular users can:**
* (C) Add new television and test records
* (R) View all television and test records
* (U) Edit the record they just added, but once they log out and the session is closed they're no longer able to edit the record

**Admin users can:**
* (C) Add new television and test records
* (R) View all television and test records
* (U) Edit all television and test records
* (D) Delete all television and test records
* (U) Approve regular users to become admins

### Database
* The application uses SQLite as its database engine.
* The database schema includes a `users` table for storing regular and admin user information, a `televisions` table for storing television records and a `tests` table for storing test records.
* SQLite is serverless and uses a local file (`database.db`) for data storage.

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

#### Admin Login
The examiner can log in as an admin user with these credentials:
* Username: `admin` 
* Password: `Pass123?`

Or the examiner can register a new account, by default this is a regular user, and they would need to be approved by an admin using the Approval Dashboard.

## Usage
* Access the application by opening a web browser and navigating to https://catrinaproject1.pythonanywhere.com/
* Register for a new user account or log in as admin with the credentials in [# Admin Login](#admin-login)
* Use the application to manage television and test records, including adding, editing, and deleting (admin only) records.
