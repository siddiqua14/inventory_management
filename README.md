# Inventory Management System

## Overview

The Inventory Management System is a Django-based application designed for managing property data, including locations and accommodations. The system supports geospatial data using PostgreSQL with the PostGIS extension, allowing for precise location-based queries. Property owners can sign up to manage their accommodations, and administrators can manage the system through a comprehensive admin interface.

## Features

- **Geospatial Data**: Uses PostGIS for location-based features.
- **Property Management**: Manage accommodations with detailed information, including location, amenities, pricing, and more.
- **User Management**: Property owners can sign up, while administrators can approve their requests and manage properties.
- **CSV Import/Export**: Locations can be imported from CSV via the Django Admin interface.
- **Admin Interface**: A comprehensive Django Admin interface for managing locations, accommodations, and user roles.
- **Command-Line Utility**: A Django CLI command to simplify various tasks:

  - Generate a `sitemap.json` file for country locations.
  - Populate the database with initial data:
    - `add_location`
    - `add_accommodation`
    - `add_localize_accommodation`

- **Create the necessary user groups** using the `create_groups` command.
## Prerequisites

Before getting started, make sure you have the following tools and technologies installed:

- **Docker** (for containerization)
- **Docker Compose** (for managing multi-container applications)
- **PostgreSQL** (with PostGIS extension for geospatial data)
- **Python 3.8+** (Django runs on Python)
- **Pip** (Python package installer)
- **Django 3.x+** (web framework)
- **PostGIS** (PostgreSQL extension for geospatial data)
- **Git** (version control)
## Setting up the Environment

### 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/siddiqua14/inventory_management.git
cd inventory-management
```
### 2. Create a Virtual Environment (Optional)
You can create a virtual environment to isolate project dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
cd djangoproject
```
### 3. Install Dependencies

Install the necessary dependencies listed in `requirements.txt` by running the following command:
```bash
pip install -r requirements.txt
```
### 4. Set up Docker


The project includes a **Dockerfile** and **docker-compose.yml** for containerizing the application.

#### Dockerfile:
- Defines the environment for the Django application, including dependencies.

#### docker-compose.yml:
- Defines the services (web, db) and manages the connection between the application and the PostgreSQL database.

To set up the Docker containers, run the following command:

```bash
docker-compose up --build
```
### Apply Database Migrations

To set up the database and populate it with initial data, follow these steps:

1. Open a bash shell in the Django container:
```bash
docker exec -it djangoproject-web-1 bash
```
2. Apply database migrations:

```bash
python manage.py migrate
```
3. Populate the database with initial data by running the following management commands:
```bash
python manage.py add_location
python manage.py add_accommodation
python manage.py add_localize_accommodation
``` 
### Create a Superuser

To access the Django Admin interface, you need to create a superuser. Run the following command:

```bash
docker exec -it djangoproject-web-1 python manage.py createsuperuser
```
Once created, you can log in to the Django Admin interface at http://localhost:8000/admin/

### User Groups and Permissions

#### Property Owners Group

A "Property Owners" user group has been established to restrict access to accommodations.

**Property owners can:**
- View, create, and update their own accommodations.
- **They cannot:** Access accommodations owned by other users.

To create the required user groups, run the following command:
```bash
docker exec -it djangoproject-web-1 python manage.py create_groups
```
#### User Registration and Admin Permissions

When a user signs up through the registration page at http://localhost:8000, their account will be **inactive** by default. An admin must grant permissions for the user to access the "Property Owners" group.

#### Steps for Admin:
1. **Activate the User Account**:
   - Go to the Django Admin interface at http://localhost:8000/admin.
   - Navigate to the **Users** section.
   - Select the newly registered user and check the **Active** checkbox to activate the account.

2. **Assign Staff Status**:
   - If the user requires access to the Django Admin interface, check the **Staff status** checkbox.

3. **Add to Property Owners Group**:
   - Assign the user to the "Property Owners" group by selecting it under the **Groups** section in the user’s profile.

After completing these steps, the user will be able to log in and manage their accommodations within the "Property Owners" group.

---

#### Superuser Access
The superuser account created earlier has full access to all features and data in the Django Admin interface.

### Sitemap Generation

#### Generate the `sitemap.json` File
To generate the `sitemap.json` file containing a list of all location URLs, run the following command:  
```bash
docker exec -it djangoproject-web-1 python manage.py generate_sitemap
```
### Unit Testing

Unit tests are provided to ensure that the code functions as expected and to maintain stability. Tests are written using Django's testing framework.

#### To run tests:
```bash
docker exec -it djangoproject-web-1 python manage.py test
```
#### Code Coverage:
The project aims to maintain a code coverage of at least 70%.
```bash
docker exec -it djangoproject-web-1 coverage run manage.py test
docker exec -it djangoproject-web-1 coverage report
```