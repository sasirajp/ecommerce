SELECT current_database();
\c ecommerce_db;
SELECT current_database();
INSERT INTO orders (user_id, item_ids, total_amount, status, created_at, updated_at) VALUES
(101, ARRAY[1, 2, 3], 250.00, 'PENDING', NOW(), NOW()),
(102, ARRAY[4, 5], 150.00, 'PENDING', NOW(), NOW()),
(103, ARRAY[6, 7, 8], 350.50, 'PENDING', NOW(), NOW());