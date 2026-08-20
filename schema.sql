DROP TABLE IF EXISTS store_sales;
DROP TABLE IF EXISTS population;

CREATE TABLE store_sales (
    store_id VARCHAR(50) PRIMARY KEY,
    store_name VARCHAR(255),
    category_large_code VARCHAR(20),  
    category_large VARCHAR(100),
    category_mid_code VARCHAR(20),    
    category_mid VARCHAR(100),
    sigungu VARCHAR(50),
    region_code VARCHAR(50),
    region_name VARCHAR(50),
    lon DOUBLE,
    lat DOUBLE
);

CREATE INDEX idx_store_sigungu ON store_sales(sigungu);
CREATE INDEX idx_store_category ON store_sales(category_mid_code);

CREATE TABLE population (
    sigungu VARCHAR(50) PRIMARY KEY,
    total_pop INT,
    pop_0s INT,
    pop_10s INT,
    pop_20s INT,
    pop_30s INT,
    pop_40s INT,
    pop_50s INT,
    pop_60s INT,
    pop_70s INT,
    pop_65plus INT
);