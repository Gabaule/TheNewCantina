Of course! Here is a `readme.md` file for your "The New Cantina" project.

---

# The New Cantina

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Powered-blue?logo=docker)](https://www.docker.com/)
[![HTMX](https://img.shields.io/badge/HTMX-1.9-blue?logo=htmx&logoColor=white)](https://htmx.org/)

**The New Cantina** is a modern, full-stack web application for a university canteen meal ordering system. It provides a seamless experience for students and staff to view daily menus, manage their account balance, and place orders. The application also features a comprehensive admin dashboard for managing users, cafeterias, dishes, and daily menus.

The entire project is built with a Python/Flask backend, a dynamic HTMX/Alpine.js frontend, and is fully containerized with Docker for easy setup and deployment.


_Admin Menu Management Dashboard_

---

## ✨ Key Features

### User Features
-   👤 **Authentication:** Secure login for students, staff, and administrators.
-   💰 **Balance Management:** Users have a personal balance and can top it up.
-   🗓️ **Dynamic Menu Browsing:** View daily menus for different cafeterias by selecting a date. The interface updates instantly without page reloads.
-   🛒 **Ordering System:** Add dishes to a shopping cart and place an order, which is deducted from the user's balance.
-   📜 **Order History:** View past orders, filterable by month.
-   📱 **Responsive UI:** A clean, responsive interface built with Tailwind CSS that works on desktop and mobile.

### Admin Features
-   ⚙️ **Admin Dashboard:** A separate, comprehensive interface for system management.
-   👥 **User Management:** Full CRUD (Create, Read, Update, Delete) operations for all user accounts.
-   🏢 **Cafeteria Management:** Add or remove cafeterias from the system.
-   🍲 **Dish Management:** A central repository for all available dishes, including name, description, price, and type.
-   📝 **Interactive Menu Management:** An intuitive dashboard to create and update daily menus. Admins can add existing or new dishes to the menu for a specific day and assign them to one or more cafeterias in a single interface.

---

## 🛠️ Tech Stack

-   **Backend:** Python 3.11+, Flask, SQLAlchemy (ORM)
-   **Frontend:** HTML5, Tailwind CSS, **HTMX**, **Alpine.js**
-   **Database:** PostgreSQL 16
-   **Containerization:** Docker, Docker Compose
-   **Development & Testing:**
    -   **PgAdmin:** For direct database management.
    -   **Pytest:** For automated backend testing.

---

## 🚀 Getting Started

### Prerequisites
-   [Docker](https://www.docker.com/products/docker-desktop/)
-   [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

### Installation & Running

1.  **Clone the repository:**
    ```sh
    git clone <your-repository-url>
    cd <project-directory>
    ```

2.  **Build and run the services:**
    ```sh
    docker-compose up --build
    ```
    The application will start, and the PostgreSQL database will be automatically initialized and seeded with demo data on the first run.

### Accessing the Services

-   **Main Application:** [**http://localhost:8081**](http://localhost:8081)
-   **PgAdmin (Database GUI):** [**http://localhost:5050**](http://localhost:5050)
    -   **Email:** `admin@example.com`
    -   **Password:** `password`
    -   *(To connect to the database in PgAdmin, use `postgres-db` as the hostname, `TheNewCantina` as the database name, `admin` as the user, and `password` as the password.)*

### Demo Accounts

You can use the following accounts to log in and test the application:

| Role    | Email                  | Password   |
|---------|------------------------|------------|
| 👨‍🎓 **Student** | `student1@example.com` | `pass123`  |
| 👨‍🏫 **Staff**   | `faculty1@example.com` | `pass123`  |
| 👑 **Admin**  | `admin@example.com`    | `password` |

---

## 📂 Project Structure

The project is organized to separate concerns, making it easy to navigate and maintain.

```
.
├── app/                  # Main Flask application source code
│   ├── controller/       # Flask blueprints, routes, and business logic
│   ├── models/           # SQLAlchemy ORM models
│   ├── templates/        # Jinja2 HTML templates (including admin section)
│   ├── db_seeder.py      # Populates the DB with initial data
│   └── main.py           # Application entry point
├── db-init/              # Database initialization scripts
│   └── init.sql          # SQL schema definition
├── docker/               # Docker-related files
│   ├── docker-compose.yml# Defines the services (app, db, pgadmin)
│   └── Dockerfile        # Instructions to build the Python app image
├── tests/                # Automated tests
│   └── test-python/      # Pytest tests for models and controllers
└── readme.md             # This file
```

---

## ✅ Running Tests

The project includes a suite of backend tests using Pytest. The tests use an in-memory SQLite database and do not affect the main PostgreSQL database.

To run the tests, execute the following command while the services are running:

```sh
docker-compose exec python-app pytest
```

This will run all unit tests for the SQLAlchemy models and API controllers inside the `python-app` container.