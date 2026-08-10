--#1
SELECT customer_name, grade
FROM tb_customer
WHERE city = '서울';

--#2
SELECT *
FROM tb_customer
WHERE customer_name LIKE '이%';

--#3
SELECT *
FROM tb_product
WHERE unit_price BETWEEN 5000 AND 50000
ORDER BY unit_price ASC;

--#4
SELECT COUNT(*) AS order_cnt
FROM tb_order
WHERE order_dt >= '2024-04-01' 
  AND order_dt < '2024-07-01';

--#5
SELECT *
FROM tb_customer
WHERE grade IS NULL;

--#6
SELECT *
FROM tb_customer
WHERE grade IS NULL;

--#7
SELECT IFNULL(grade, '미지정') AS grade,
       COUNT(*) AS cnt,
       ROUND(COUNT(*) / (SELECT COUNT(*) FROM tb_customer) * 100, 1) AS ratio_pct
FROM tb_customer
GROUP BY grade;

--#8
SELECT DATE_FORMAT(order_dt, '%Y-%m') AS order_month, 
       COUNT(*) AS order_cnt
FROM tb_order
WHERE status != '취소'
GROUP BY DATE_FORMAT(order_dt, '%Y-%m');

--#9
SELECT category_id
FROM tb_product
GROUP BY category_id
HAVING SUM(stock_qty) < 100;

--#10
SELECT MAX(unit_price) - MIN(unit_price) AS price_diff
FROM tb_product;

--#11
SELECT c.customer_name, 
       o.order_dt, 
       SUM(i.qty * i.unit_price) AS total_amount
FROM tb_order o
JOIN tb_customer c ON o.customer_id = c.customer_id
JOIN tb_order_item i ON o.order_id = i.order_id
GROUP BY o.order_id, c.customer_name, o.order_dt;

--#12
SELECT c.*
FROM tb_customer c
LEFT JOIN tb_order o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

--#13
SELECT p.*
FROM tb_product p
LEFT JOIN tb_order_item i ON p.product_id = i.product_id
WHERE i.order_item_id IS NULL;

--#14
SELECT c.customer_name, 
       SUM(i.qty * i.unit_price) AS total_amount
FROM tb_customer c
JOIN tb_order o ON c.customer_id = o.customer_id
JOIN tb_order_item i ON o.order_id = i.order_id
WHERE o.status != '취소'
GROUP BY c.customer_id, c.customer_name
ORDER BY total_amount DESC
LIMIT 5;

--#15
SELECT c.country, 
       p.category_id, 
       SUM(i.qty * i.unit_price) AS total_sales
FROM tb_customer c
JOIN tb_order o ON c.customer_id = o.customer_id
JOIN tb_order_item i ON o.order_id = i.order_id
JOIN tb_product p ON i.product_id = p.product_id
WHERE o.status != '취소'
GROUP BY c.country, p.category_id;

--#16
SELECT category_id,
       COUNT(*) AS product_cnt,
       CASE 
           WHEN COUNT(*) > 3 THEN '많음' 
           ELSE '적음' 
       END AS cnt_status
FROM tb_product
GROUP BY category_id;

--#17
SELECT 
    CASE
        WHEN order_cnt = 0 THEN '0건'
        WHEN order_cnt IN (1, 2) THEN '1~2건'
        ELSE '3건 이상'
    END AS order_group,
    COUNT(*) AS customer_cnt
FROM (
    SELECT c.customer_id, COUNT(o.order_id) AS order_cnt
    FROM tb_customer c
    LEFT JOIN tb_order o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
) t
GROUP BY 
    CASE
        WHEN order_cnt = 0 THEN '0건'
        WHEN order_cnt IN (1, 2) THEN '1~2건'
        ELSE '3건 이상'
    END;

--#18
SELECT YEAR(o.order_dt) AS order_year,
       SUM(CASE WHEN MONTH(o.order_dt) = 1 THEN i.qty * i.unit_price ELSE 0 END) AS m01,
       SUM(CASE WHEN MONTH(o.order_dt) = 2 THEN i.qty * i.unit_price ELSE 0 END) AS m02,
       SUM(CASE WHEN MONTH(o.order_dt) = 3 THEN i.qty * i.unit_price ELSE 0 END) AS m03,
       SUM(CASE WHEN MONTH(o.order_dt) = 4 THEN i.qty * i.unit_price ELSE 0 END) AS m04,
       SUM(CASE WHEN MONTH(o.order_dt) = 5 THEN i.qty * i.unit_price ELSE 0 END) AS m05,
       SUM(CASE WHEN MONTH(o.order_dt) = 6 THEN i.qty * i.unit_price ELSE 0 END) AS m06,
       SUM(CASE WHEN MONTH(o.order_dt) = 7 THEN i.qty * i.unit_price ELSE 0 END) AS m07,
       SUM(CASE WHEN MONTH(o.order_dt) = 8 THEN i.qty * i.unit_price ELSE 0 END) AS m08,
       SUM(CASE WHEN MONTH(o.order_dt) = 9 THEN i.qty * i.unit_price ELSE 0 END) AS m09,
       SUM(CASE WHEN MONTH(o.order_dt) = 10 THEN i.qty * i.unit_price ELSE 0 END) AS m10,
       SUM(CASE WHEN MONTH(o.order_dt) = 11 THEN i.qty * i.unit_price ELSE 0 END) AS m11,
       SUM(CASE WHEN MONTH(o.order_dt) = 12 THEN i.qty * i.unit_price ELSE 0 END) AS m12
FROM tb_order o
JOIN tb_order_item i ON o.order_id = i.order_id
WHERE o.status != '취소'
GROUP BY YEAR(o.order_dt);

--#19
SELECT 
    c.category_name,
    p.product_name,
    IFNULL(s.sold_qty, 0) AS total_sold_qty,
    p.stock_qty AS remaining_stock,
    ROUND(
        IFNULL(s.sold_qty, 0) / (IFNULL(s.sold_qty, 0) + p.stock_qty) * 100, 1
    ) AS exhaustion_rate
FROM tb_product p
LEFT JOIN tb_category c ON p.category_id = c.category_id
LEFT JOIN (
    SELECT i.product_id, SUM(i.qty) AS sold_qty
    FROM tb_order_item i
    JOIN tb_order o ON i.order_id = o.order_id
    WHERE o.status != '취소'
    GROUP BY i.product_id
) s ON p.product_id = s.product_id
ORDER BY exhaustion_rate DESC;

--#20
SELECT 
    IFNULL(c.customer_name, '총계') AS customer_name,
    c.country,
    o.order_dt,
    SUM(i.qty * i.unit_price) AS cancel_amount,
    COUNT(i.order_item_id) AS item_count
FROM tb_order o
JOIN tb_customer c ON o.customer_id = c.customer_id
JOIN tb_order_item i ON o.order_id = i.order_id
WHERE o.status = '취소'
GROUP BY o.order_id, c.customer_name, c.country, o.order_dt WITH ROLLUP
ORDER BY cancel_amount DESC;

--#21
SELECT 
    IFNULL(c.grade, '미지정') AS grade,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT CASE WHEN o.order_id IS NOT NULL THEN c.customer_id END) AS ordered_customers,
    IFNULL(SUM(i.qty * i.unit_price), 0) AS total_sales,
    IFNULL(SUM(i.qty * i.unit_price), 0) / COUNT(DISTINCT c.customer_id) AS avg_sales_per_person
FROM tb_customer c
LEFT JOIN tb_order o ON c.customer_id = o.customer_id AND o.status != '취소'
LEFT JOIN tb_order_item i ON o.order_id = i.order_id
GROUP BY IFNULL(c.grade, '미지정')
ORDER BY avg_sales_per_person DESC;


