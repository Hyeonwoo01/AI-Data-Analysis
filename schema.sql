CREATE TABLE IF NOT EXISTS tb_nf_stock (
    bas_dt DATE NOT NULL, 
    srtn_cd CHAR(6) NOT NULL, 
    itms_nm VARCHAR(100), 
    clpr BIGINT, vs BIGINT, mkp BIGINT, hipr BIGINT, lopr BIGINT, trqu BIGINT, raw_id BIGINT,
    PRIMARY KEY (bas_dt, srtn_cd)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tb_fsc_stock (
    bas_dt DATE NOT NULL, 
    srtn_cd CHAR(6) NOT NULL, 
    itms_nm VARCHAR(100), 
    clpr BIGINT, vs BIGINT, mkp BIGINT, hipr BIGINT, lopr BIGINT, trqu BIGINT, raw_id BIGINT,
    PRIMARY KEY (bas_dt, srtn_cd)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tb_mart_stock_monthly (
    srtn_cd     CHAR(6)     NOT NULL,
    ym          CHAR(7)     NOT NULL,
    trd_days    INT,
    open_clpr   BIGINT,
    close_clpr  BIGINT,
    avg_clpr    BIGINT,
    max_clpr    BIGINT,
    min_clpr    BIGINT,
    sum_trqu    BIGINT,
    avg_trqu    BIGINT,
    PRIMARY KEY (srtn_cd, ym)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tb_mart_stock_daily (
    bas_dt     DATE        NOT NULL,
    srtn_cd    CHAR(6)     NOT NULL,
    clpr       BIGINT,
    trqu       BIGINT,
    chg_pct    DOUBLE,
    ma5        DOUBLE,
    ma20       DOUBLE,
    vol_ratio  DOUBLE,
    PRIMARY KEY (bas_dt, srtn_cd)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;