CREATE TABLE IF NOT EXISTS stocks (
  symbol  TEXT,
  name    TEXT,

  PRIMARY KEY (symbol)
);

COPY stocks(symbol, name) from '/Users/ashish/Developer/georgian/data_programming/algorithmic/data/stock_info.csv' delimiter ',' csv;
