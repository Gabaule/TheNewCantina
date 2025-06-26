/* ===========================================================
   The New Cantina - SQL Schema
   - This schema is designed to match the SQLAlchemy models in the application.
   - It creates the tables, constraints, and relationships.
   - Data population is handled by the Python application on first launch.
=========================================================== */

-- Drop all tables if they exist, for a clean install
DROP TABLE IF EXISTS order_item, reservation, daily_menu_item, daily_menu, dish, cafeteria, app_user CASCADE;

-- 1. USERS (app_user)
-- Matches app/models/app_user.py
CREATE TABLE app_user (
    user_id     SERIAL PRIMARY KEY,
    last_name   VARCHAR(50)  NOT NULL,
    first_name  VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    balance     NUMERIC(10, 2) DEFAULT 0.00,
    role        VARCHAR(20) NOT NULL DEFAULT 'student'
                  CHECK (role IN ('student', 'staff', 'admin')),
    created_at  TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. CAFETERIAS (cafeteria)
-- Matches app/models/cafeteria.py
CREATE TABLE cafeteria (
    cafeteria_id  SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    address     TEXT,
    phone       VARCHAR(20),
    created_at  TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. DISHES (dish)
-- Matches app/models/dish.py
CREATE TABLE dish (
    dish_id         SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    description     TEXT,
    dine_in_price   NUMERIC(10,2) NOT NULL,
    dish_type       VARCHAR(20) NOT NULL CHECK (
        dish_type IN ('main_course', 'side_dish', 'soup', 'drink')
    ),
    created_at      TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. DAILY MENUS (daily_menu)
-- Matches app/models/daily_menu.py
CREATE TABLE daily_menu (
    menu_id      SERIAL PRIMARY KEY,
    cafeteria_id   INT NOT NULL REFERENCES cafeteria(cafeteria_id) ON DELETE CASCADE,
    menu_date    DATE NOT NULL,
    created_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (cafeteria_id, menu_date)
);

-- 5. DAILY MENU ITEMS (daily_menu_item)
-- Matches app/models/daily_menu_item.py
CREATE TABLE daily_menu_item (
    menu_item_id  SERIAL PRIMARY KEY,
    menu_id       INT NOT NULL REFERENCES daily_menu(menu_id) ON DELETE CASCADE,
    dish_id       INT NOT NULL REFERENCES dish(dish_id),
    dish_role     VARCHAR(20) NOT NULL CHECK (
        dish_role IN ('main_course', 'side_dish', 'soup', 'drink')
    ),
    display_order INT DEFAULT 1
);

-- 6. RESERVATIONS (reservation = user's order)
-- Matches app/models/reservation.py
CREATE TABLE reservation (
    reservation_id        SERIAL PRIMARY KEY,
    user_id               INT NOT NULL REFERENCES app_user(user_id) ON DELETE CASCADE,
    cafeteria_id          INT REFERENCES cafeteria(cafeteria_id) ON DELETE SET NULL,
    reservation_datetime  TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    total                 NUMERIC(10,2) NOT NULL,
    status                VARCHAR(20) DEFAULT 'pending'
);

-- 7. ORDER ITEMS (order_item = details of each reserved dish)
-- Matches app/models/order_item.py
CREATE TABLE order_item (
    item_id         SERIAL PRIMARY KEY,
    reservation_id  INT NOT NULL REFERENCES reservation(reservation_id) ON DELETE CASCADE,
    dish_id         INT NOT NULL REFERENCES dish(dish_id),
    quantity        INT DEFAULT 1 CHECK (quantity > 0),
    is_takeaway     BOOLEAN NOT NULL,
    applied_price   NUMERIC(10,2) NOT NULL
);

-- END OF SCRIPT