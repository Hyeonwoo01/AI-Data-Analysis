-- #1
CREATE DATABASE shopping_db;
USE shopping_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price INT NOT NULL DEFAULT 0,
    stock_quantity INT NOT NULL DEFAULT 0
);

ALTER TABLE users ADD COLUMN phone VARCHAR(20) NULL;


--#2
INSERT INTO users (username, email, phone) 
VALUES 
    ('철수', 'chulsoo@test.com', NULL),
    ('길동', 'hong@test.com', '010-1111-2222'),
    ('영희', 'young@test.com', '010-3333-4444');

INSERT INTO products (product_name, price, stock_quantity) 
VALUES 
    ('무선 마우스', 25000, 50),
    ('기계식 키보드', 89000, 30),
    ('4K 모니터', 350000, 10),
    ('USB 허브', 15000, 100);

UPDATE users 
    SET phone = '010-1234-5678' 
    WHERE email = 'chulsoo@test.com';

DELETE FROM products 
    WHERE product_name = 'USB 허브';


--#3
SELECT DISTINCT stock_quantity 
FROM products;

SELECT product_name, price 
FROM products 
ORDER BY price DESC;

SELECT * 
FROM users 
ORDER BY user_id DESC 
LIMIT 2;