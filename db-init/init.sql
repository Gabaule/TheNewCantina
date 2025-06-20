/*======================================================================
  Database schema for canteen management system
======================================================================*/

-----------------------------------------------------------------------
-- 1. Users
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id     SERIAL PRIMARY KEY,
    last_name   VARCHAR(50)  NOT NULL,
    first_name  VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    balance     NUMERIC(10,2) DEFAULT 0.00,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-----------------------------------------------------------------------
-- 2. Canteens
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS canteens (
    canteen_id  SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    address     TEXT,
    phone       VARCHAR(20),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-----------------------------------------------------------------------
-- 3. Dishes
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dishes (
    dish_id         SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    description     TEXT,
    dine_in_price   NUMERIC(10,2) NOT NULL,
    takeaway_price  NUMERIC(10,2) NOT NULL,
    is_available    BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-----------------------------------------------------------------------
-- 4. Orders
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
    order_id    SERIAL PRIMARY KEY,
    user_id     INT REFERENCES users(user_id) ON DELETE CASCADE,
    canteen_id  INT REFERENCES canteens(canteen_id) ON DELETE SET NULL,
    order_date  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total       NUMERIC(10,2) NOT NULL,
    status      VARCHAR(20) DEFAULT 'pending'
);

-----------------------------------------------------------------------
-- 5. Order Details
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_details (
    detail_id       SERIAL PRIMARY KEY,
    order_id        INT REFERENCES orders(order_id) ON DELETE CASCADE,
    dish_id         INT REFERENCES dishes(dish_id) ON DELETE CASCADE,
    quantity        INT DEFAULT 1 CHECK (quantity > 0),
    is_takeaway     BOOLEAN NOT NULL,
    applied_price   NUMERIC(10,2) NOT NULL
);


-- Fake data for University of Zilina canteen management system

-----------------------------------------------------------------------
-- 1. Canteens at University of Zilina
-----------------------------------------------------------------------
INSERT INTO canteens (name, address, phone) VALUES
    ('Main University Canteen - Velky Diel', 'Univerzitná 8215/1, 010 26 Žilina', '+421 41 513 4001'),
    ('Faculty of Civil Engineering Canteen', 'Univerzitná 8215/1, 010 26 Žilina', '+421 41 513 5201'),
    ('Student Dormitory Canteen - Hliny', 'Hliny VI, 010 01 Žilina', '+421 41 513 4501'),
    ('Faculty of Mechanical Engineering Cafeteria', 'Univerzitná 8215/1, 010 26 Žilina', '+421 41 513 2801'),
    ('IT Campus Food Court', 'Univerzitná 8215/1, 010 26 Žilina', '+421 41 513 4201');

-----------------------------------------------------------------------
-- 2. Users (Students and Staff)
-----------------------------------------------------------------------
INSERT INTO users (last_name, first_name, email, password, balance) VALUES
    ('Novák', 'Jakub', 'jakub.novak@stud.uniza.sk', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWBKVaYHYg8Me', 25.50),
    ('Svoboda', 'Petra', 'petra.svoboda@stud.uniza.sk', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWBKVaYHYg8Me', 18.75),
    ('Dvořák', 'Martin', 'martin.dvorak@uniza.sk', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWBKVaYHYg8Me', 42.30),
    ('Kováčová', 'Anna', 'anna.kovacova@stud.uniza.sk', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWBKVaYHYg8Me', 31.20),
    ('Procházka', 'Tomáš', 'tomas.prochazka@stud.uniza.sk', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWBKVaYHYg8Me', 15.80),
    ('Varga', 'Zuzana', 'zuzana.varga@uniza.sk', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWBKVaYHYg8Me', 28.90),
    ('Horváth', 'Michal', 'michal.horvath@stud.uniza.sk', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWBKVaYHYg8Me', 22.15),
    ('Balog', 'Lucia', 'lucia.balog@stud.uniza.sk', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWBKVaYHYg8Me', 33.65),
    ('Krištof', 'David', 'david.kristof@uniza.sk', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWBKVaYHYg8Me', 45.00),
    ('Machová', 'Elena', 'elena.machova@stud.uniza.sk', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWBKVaYHYg8Me', 19.40);

-----------------------------------------------------------------------
-- 3. Dishes (Slovak/Czech cuisine typical for university canteens)
-----------------------------------------------------------------------
INSERT INTO dishes (name, description, dine_in_price, takeaway_price, is_available) VALUES
    -- Main courses
    ('Schnitzel with Potato Salad', 'Breaded pork schnitzel served with traditional potato salad', 5.80, 6.20, true),
    ('Goulash with Dumplings', 'Traditional Slovak beef goulash with bread dumplings', 4.90, 5.30, true),
    ('Chicken Breast with Rice', 'Grilled chicken breast with jasmine rice and vegetables', 5.20, 5.60, true),
    ('Pork Tenderloin with Mashed Potatoes', 'Roasted pork tenderloin with creamy mashed potatoes', 6.10, 6.50, true),
    ('Fish Fillet with Boiled Potatoes', 'Pan-fried fish fillet with herbs and boiled potatoes', 5.50, 5.90, true),
    ('Vegetarian Pasta', 'Pasta with seasonal vegetables and herb sauce', 4.20, 4.60, true),
    ('Beef Stroganoff', 'Tender beef strips in creamy sauce with pasta', 5.70, 6.10, true),
    ('Halusky with Bryndza', 'Traditional Slovak potato dumplings with sheep cheese', 4.50, 4.90, true),
    
    -- Soups
    ('Chicken Soup', 'Clear chicken broth with vegetables and noodles', 1.80, 2.00, true),
    ('Mushroom Cream Soup', 'Creamy soup with forest mushrooms', 2.10, 2.30, true),
    ('Bean Soup', 'Hearty bean soup with smoked meat', 2.20, 2.40, true),
    ('Tomato Soup', 'Classic tomato soup with basil', 1.90, 2.10, true),
    
    -- Sides and snacks
    ('French Fries', 'Crispy golden french fries', 2.30, 2.50, true),
    ('Mixed Salad', 'Fresh seasonal salad with dressing', 2.80, 3.00, true),
    ('Bread Roll', 'Fresh baked bread roll', 0.60, 0.70, true),
    ('Apple Strudel', 'Traditional apple strudel with vanilla sauce', 2.90, 3.10, true),
    
    -- Beverages
    ('Coffee', 'Freshly brewed coffee', 1.20, 1.30, true),
    ('Tea', 'Hot tea selection', 1.00, 1.10, true),
    ('Orange Juice', 'Fresh orange juice', 1.80, 1.90, true),
    ('Mineral Water', 'Sparkling or still mineral water', 1.10, 1.20, true);

-----------------------------------------------------------------------
-- 4. Sample Orders
-----------------------------------------------------------------------
INSERT INTO orders (user_id, canteen_id, order_date, total, status) VALUES
    (1, 1, '2024-02-15 12:30:00', 7.60, 'completed'),
    (2, 1, '2024-02-15 13:15:00', 6.90, 'completed'),
    (3, 2, '2024-02-15 11:45:00', 12.40, 'completed'),
    (4, 3, '2024-02-15 18:30:00', 8.30, 'completed'),
    (5, 1, '2024-02-16 12:00:00', 5.70, 'completed'),
    (6, 4, '2024-02-16 13:30:00', 9.80, 'completed'),
    (7, 1, '2024-02-16 12:45:00', 7.10, 'completed'),
    (8, 5, '2024-02-16 14:00:00', 6.50, 'pending'),
    (9, 2, '2024-02-17 11:30:00', 11.20, 'completed'),
    (10, 3, '2024-02-17 19:00:00', 8.90, 'completed');

-----------------------------------------------------------------------
-- 5. Order Details
-----------------------------------------------------------------------
INSERT INTO order_details (order_id, dish_id, quantity, is_takeaway, applied_price) VALUES
    -- Order 1 (Jakub Novák)
    (1, 1, 1, false, 5.80),  -- Schnitzel dine-in
    (1, 9, 1, false, 1.80),  -- Chicken soup dine-in
    
    -- Order 2 (Petra Svoboda)
    (2, 6, 1, true, 4.60),   -- Vegetarian pasta takeaway
    (2, 14, 1, true, 3.00),  -- Mixed salad takeaway
    (2, 17, 1, true, 1.30),  -- Coffee takeaway
    
    -- Order 3 (Martin Dvořák)
    (3, 2, 1, false, 4.90),  -- Goulash dine-in
    (3, 4, 1, false, 6.10),  -- Pork tenderloin dine-in
    (3, 18, 1, false, 1.00), -- Tea dine-in
    (3, 15, 1, false, 0.60), -- Bread roll dine-in
    
    -- Order 4 (Anna Kováčová)
    (4, 8, 1, true, 4.90),   -- Halusky takeaway
    (4, 11, 1, true, 2.40),  -- Bean soup takeaway
    (4, 20, 1, true, 1.20),  -- Mineral water takeaway
    
    -- Order 5 (Tomáš Procházka)
    (5, 7, 1, false, 5.70),  -- Beef stroganoff dine-in
    
    -- Order 6 (Zuzana Varga)
    (6, 3, 1, false, 5.20),  -- Chicken breast dine-in
    (6, 10, 1, false, 2.10), -- Mushroom soup dine-in
    (6, 13, 1, false, 2.30), -- French fries dine-in
    (6, 19, 1, false, 1.80), -- Orange juice dine-in
    
    -- Order 7 (Michal Horváth)
    (7, 5, 1, true, 5.90),   -- Fish fillet takeaway
    (7, 17, 1, true, 1.30),  -- Coffee takeaway
    
    -- Order 8 (Lucia Balog)
    (8, 6, 1, false, 4.20),  -- Vegetarian pasta dine-in
    (8, 12, 1, false, 1.90), -- Tomato soup dine-in
    (8, 15, 1, false, 0.60), -- Bread roll dine-in
    
    -- Order 9 (David Krištof)
    (9, 1, 1, false, 5.80),  -- Schnitzel dine-in
    (9, 4, 1, false, 6.10),  -- Pork tenderloin dine-in
    (9, 16, 1, false, 2.90), -- Apple strudel dine-in
    
    -- Order 10 (Elena Machová)
    (10, 8, 1, true, 4.90),  -- Halusky takeaway
    (10, 14, 1, true, 3.00), -- Mixed salad takeaway
    (10, 20, 1, true, 1.20); -- Mineral water takeaway