/* ===========================================================
   Faculty Cafeteria Reservation System - SQL Schema
   - Roles (student, staff, admin)
   - Daily menu structure (main/side/soup/drink)
   - Example data
   - Clean install
=========================================================== */

-- Drop all tables if they exist, for a clean install
DROP TABLE IF EXISTS order_item, reservation, daily_menu_item, daily_menu, dish, cafeteria, app_user CASCADE;

-- 1. USERS (app_user)
CREATE TABLE app_user (
    user_id     SERIAL PRIMARY KEY,
    last_name   VARCHAR(50)  NOT NULL,
    first_name  VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    balance     NUMERIC(10,2) DEFAULT 0.00,
    role        VARCHAR(20) NOT NULL DEFAULT 'student'
                  CHECK (role IN ('student', 'staff', 'admin')),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. CAFETERIAS (cafeteria)
CREATE TABLE cafeteria (
    cafeteria_id  SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    address     TEXT,
    phone       VARCHAR(20),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. DISHES (dish)
CREATE TABLE dish (
    dish_id         SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    description     TEXT,
    dine_in_price   NUMERIC(10,2) NOT NULL,
    is_available    BOOLEAN DEFAULT TRUE,
    dish_type       VARCHAR(20) NOT NULL CHECK (
        dish_type IN ('main_course', 'side_dish', 'soup', 'drink')
    ),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. DAILY MENUS (daily_menu)
CREATE TABLE daily_menu (
    menu_id      SERIAL PRIMARY KEY,
    cafeteria_id   INT REFERENCES cafeteria(cafeteria_id) ON DELETE CASCADE,
    menu_date    DATE NOT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (cafeteria_id, menu_date)
);

-- 5. DAILY MENU ITEMS (daily_menu_item)
CREATE TABLE daily_menu_item (
    menu_item_id SERIAL PRIMARY KEY,
    menu_id      INT REFERENCES daily_menu(menu_id) ON DELETE CASCADE,
    dish_id      INT REFERENCES dish(dish_id) ON DELETE CASCADE,
    dish_role    VARCHAR(20) NOT NULL CHECK (
        dish_role IN ('main_course', 'side_dish', 'soup', 'drink')
    ),
    display_order INT DEFAULT 1
);

-- 6. RESERVATIONS (reservation = user's order)
CREATE TABLE reservation (
    reservation_id    SERIAL PRIMARY KEY,
    user_id     INT REFERENCES app_user(user_id) ON DELETE CASCADE,
    cafeteria_id  INT REFERENCES cafeteria(cafeteria_id) ON DELETE SET NULL,
    reservation_datetime  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total       NUMERIC(10,2) NOT NULL,
    status      VARCHAR(20) DEFAULT 'pending'
);

-- 7. ORDER ITEMS (order_item = details of each reserved dish)
CREATE TABLE order_item (
    item_id         SERIAL PRIMARY KEY,
    reservation_id  INT REFERENCES reservation(reservation_id) ON DELETE CASCADE,
    dish_id         INT REFERENCES dish(dish_id) ON DELETE CASCADE,
    quantity        INT DEFAULT 1 CHECK (quantity > 0),
    is_takeaway     BOOLEAN NOT NULL,
    applied_price   NUMERIC(10,2) NOT NULL
);

-- =======================
-- SAMPLE DATA
-- =======================

-- CAFETERIAS
INSERT INTO cafeteria (name, address, phone) VALUES
    ('Main University Cafeteria', 'Campus A, Main Road 1', '+421 41 513 4001'),
    ('Faculty of Science Cafeteria', 'Science Building, 2nd Floor', '+421 41 513 4201');

-- USERS (with roles)
INSERT INTO app_user (last_name, first_name, email, password, balance, role) VALUES
    ('Novák', 'Jakub', 'jakub.novak@uniza.sk', 'hashedpassword', 25.50, 'student'),
    ('Kováčová', 'Anna', 'anna.kovacova@uniza.sk', 'hashedpassword', 18.75, 'student'),
    ('Smith', 'John', 'john.smith@uniza.sk', 'hashedpassword', 31.00, 'staff'),
    ('Admin', 'Alice', 'alice.admin@uniza.sk', 'hashedpassword', 100.00, 'admin');

-- DISHES (all types)
INSERT INTO dish (name, description, dine_in_price, takeaway_price, is_available, dish_type) VALUES
    -- Main Courses
    ('Schnitzel with Potato Salad', 'Breaded pork schnitzel served with potato salad', 5.80, 6.20, true, 'main_course'),
    ('Chicken Breast with Rice', 'Grilled chicken breast, rice and vegetables', 5.20, 5.60, true, 'main_course'),
    ('Goulash with Dumplings', 'Beef goulash with dumplings', 4.90, 5.30, true, 'main_course'),
    -- Side Dishes
    ('French Fries', 'Crispy golden french fries', 2.30, 2.50, true, 'side_dish'),
    ('Mixed Salad', 'Fresh seasonal salad', 2.80, 3.00, true, 'side_dish'),
    ('Bread Roll', 'Fresh baked bread roll', 0.60, 0.70, true, 'side_dish'),
    -- Soup
    ('Chicken Soup', 'Clear chicken broth with vegetables', 1.80, 2.00, true, 'soup'),
    -- Drink
    ('Mineral Water', 'Sparkling or still mineral water', 1.10, 1.20, true, 'drink');

-- DAILY MENU for Main University Cafeteria (2025-06-25)
INSERT INTO daily_menu (cafeteria_id, menu_date) VALUES (1, '2025-06-25');

-- Get menu_id for today's menu (assuming it's 1)
-- Assign 3 mains, 3 sides, 1 soup, 1 drink
INSERT INTO daily_menu_item (menu_id, dish_id, dish_role, display_order) VALUES
    (1, 1, 'main_course', 1),  -- Schnitzel
    (1, 2, 'main_course', 2),  -- Chicken Breast
    (1, 3, 'main_course', 3),  -- Goulash
    (1, 4, 'side_dish', 1),    -- Fries
    (1, 5, 'side_dish', 2),    -- Mixed Salad
    (1, 6, 'side_dish', 3),    -- Bread Roll
    (1, 7, 'soup', 1),         -- Chicken Soup
    (1, 8, 'drink', 1);        -- Mineral Water

-- RESERVATION: Jakub (student) reserves his lunch for today
INSERT INTO reservation (user_id, cafeteria_id, reservation_datetime, total, status)
VALUES (1, 1, '2025-06-25 12:00:00', 8.70, 'completed');

-- ORDER ITEMS (Jakub's selection: 1 schnitzel, 1 chicken soup, 1 fries)
INSERT INTO order_item (reservation_id, dish_id, quantity, is_takeaway, applied_price) VALUES
    (1, 1, 1, false, 5.80),   -- Schnitzel dine-in
    (1, 7, 1, false, 1.80),   -- Chicken soup dine-in
    (1, 4, 1, false, 1.10);   -- Fries dine-in

-- RESERVATION: Anna (student), takeaway
INSERT INTO reservation (user_id, cafeteria_id, reservation_datetime, total, status)
VALUES (2, 1, '2025-06-25 12:30:00', 10.30, 'pending');

INSERT INTO order_item (reservation_id, dish_id, quantity, is_takeaway, applied_price) VALUES
    (2, 2, 1, true, 5.60),    -- Chicken breast takeaway
    (2, 5, 1, true, 3.00),    -- Mixed salad takeaway
    (2, 8, 1, true, 1.20);    -- Mineral water takeaway

-- RESERVATION: John (staff), on-site
INSERT INTO reservation (user_id, cafeteria_id, reservation_datetime, total, status)
VALUES (3, 1, '2025-06-25 13:00:00', 7.80, 'completed');

INSERT INTO order_item (reservation_id, dish_id, quantity, is_takeaway, applied_price) VALUES
    (3, 3, 1, false, 5.30),   -- Goulash dine-in
    (3, 6, 1, false, 0.70),   -- Bread roll dine-in
    (3, 8, 1, false, 1.80);   -- Mineral water dine-in

-- FIN DU SCRIPT
