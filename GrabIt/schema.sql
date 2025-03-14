CREATE DATABASE IF NOT EXISTS grabit;
USE grabit;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    product_desc TEXT,
    product_cost DECIMAL(10,2) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    product_image_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sub_category VARCHAR(50),
    brand VARCHAR(50),
    availability BOOLEAN DEFAULT true
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Populate products table with sample data
INSERT INTO products (product_name, product_desc, product_cost, product_category, product_image_name) VALUES
-- Shoes
('Nike Air Max', 'Comfortable running shoes', 129.99, 'shoes', 'nike-air-max.jpg'),
('Adidas Ultraboost', 'Premium running shoes', 179.99, 'shoes', 'adidas-ultraboost.jpg'),
('Puma RS-X', 'Casual sneakers', 89.99, 'shoes', 'puma-rsx.jpg'),
('New Balance 990', 'Classic running shoes', 174.99, 'shoes', 'nb-990.jpg'),

-- Clothes
('Levi''s 501 Jeans', 'Classic fit denim', 69.99, 'clothes', 'levis-501.jpg'),
('Nike Dri-FIT Shirt', 'Athletic t-shirt', 34.99, 'clothes', 'nike-drifit.jpg'),
('Adidas Track Jacket', 'Sports jacket', 59.99, 'clothes', 'adidas-jacket.jpg'),
('H&M Sweater', 'Casual cotton sweater', 29.99, 'clothes', 'hm-sweater.jpg'),

-- Electronics
('iPhone 13', 'Latest Apple smartphone', 999.99, 'electronics', 'iphone-13.jpg'),
('Samsung TV', '55-inch 4K Smart TV', 699.99, 'electronics', 'samsung-tv.jpg'),
('Sony Headphones', 'Wireless noise-cancelling', 299.99, 'electronics', 'sony-headphones.jpg'),
('iPad Pro', '12.9-inch tablet', 1099.99, 'electronics', 'ipad-pro.jpg'),

-- Accessories
('Fossil Watch', 'Classic analog watch', 149.99, 'accessories', 'fossil-watch.jpg'),
('Ray-Ban Sunglasses', 'Classic aviator style', 154.99, 'accessories', 'rayban-aviator.jpg'),
('Coach Handbag', 'Leather shoulder bag', 299.99, 'accessories', 'coach-bag.jpg'),
('Casio G-Shock', 'Digital sports watch', 99.99, 'accessories', 'gshock-watch.jpg');

-- Update existing categories to be more specific
UPDATE products SET sub_category = CASE 
    WHEN product_category = 'shoes' THEN 'sneakers'
    WHEN product_category = 'clothes' THEN 'shirts'
    WHEN product_category = 'electronics' THEN 'phones'
    WHEN product_category = 'accessories' THEN 'watches'
END;

-- Add more sample products with new classifications
INSERT INTO products (product_name, product_desc, product_cost, product_category, sub_category, brand, product_image_name) VALUES
-- Shoes Category
('Nike Air Jordan', 'Basketball shoes with air cushioning', 199.99, 'shoes', 'basketball', 'Nike', 'air-jordan.jpg'),
('Adidas Running Boost', 'Professional running shoes', 159.99, 'shoes', 'running', 'Adidas', 'running-boost.jpg'),
('Puma Casual Slip-ons', 'Comfortable casual wear', 79.99, 'shoes', 'casual', 'Puma', 'puma-slip.jpg'),

-- Clothes Category
('Nike Dri-FIT Pro', 'Professional sports jersey', 89.99, 'clothes', 'sports', 'Nike', 'nike-jersey.jpg'),
('H&M Casual Shirt', 'Cotton blend casual shirt', 39.99, 'clothes', 'casual', 'H&M', 'hm-casual.jpg'),
('Zara Formal Blazer', 'Business formal wear', 129.99, 'clothes', 'formal', 'Zara', 'zara-blazer.jpg'),

-- Electronics Category
('Samsung Galaxy S21', '5G Smartphone with 128GB storage', 899.99, 'electronics', 'phones', 'Samsung', 'galaxy-s21.jpg'),
('Apple MacBook Pro', '13-inch laptop with M1 chip', 1299.99, 'electronics', 'laptops', 'Apple', 'macbook-pro.jpg'),
('Sony WH-1000XM4', 'Wireless noise cancelling headphones', 349.99, 'electronics', 'audio', 'Sony', 'sony-headphones.jpg'),

-- Accessories Category
('Ray-Ban Aviator', 'Classic sunglasses', 159.99, 'accessories', 'eyewear', 'Ray-Ban', 'rayban-aviator.jpg'),
('Michael Kors Watch', 'Luxury analog watch', 249.99, 'accessories', 'watches', 'Michael Kors', 'mk-watch.jpg'),
('Coach Leather Wallet', 'Premium leather wallet', 89.99, 'accessories', 'wallets', 'Coach', 'coach-wallet.jpg');