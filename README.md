# Inventory Management System

## Overview

The Inventory Management System is a Django-based application designed for managing property data, including locations and accommodations. The system supports geospatial data using PostgreSQL with the PostGIS extension, allowing for precise location-based queries. Property owners can sign up to manage their accommodations, and administrators can manage the system through a comprehensive admin interface.

## Features

- **Geospatial Data**: Uses PostGIS for location-based features.
- **Property Management**: Manage accommodations with detailed information, including location, amenities, pricing, and more.
- **User Management**: Property owners can sign up, while administrators can approve their requests and manage properties.
- **CSV Import/Export**: Locations can be imported from CSV via the Django Admin interface.
- **Admin Interface**: A comprehensive Django Admin interface for managing locations, accommodations, and user roles.
- **Command-Line Utility**: A Django CLI command to generate a `sitemap.json` file for country locations.
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