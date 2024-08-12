CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS history (
    symbol    TEXT            NOT NULL,
    date      DATE            NOT NULL,
    open      NUMERIC(15, 6)  NOT NULL,
    high      NUMERIC(15, 6)  NOT NULL,
    low       NUMERIC(15, 6)  NOT NULL,
    close     NUMERIC(15, 6)  NOT NULL,
    volume    BIGINT          NOT NULL,

    PRIMARY KEY (symbol, date)
);

SELECT create_hypertable ('history', 'date', migrate_data => true);
