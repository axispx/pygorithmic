CREATE MATERIALIZED VIEW moving_average AS
SELECT
  date,
  symbol,
  close,
  avg(close) over (partition by symbol order by date range between interval '50 days' preceding and current row) as average,
  stddev(close) over (partition by symbol order by date range between interval '50 days' preceding and current row) as std_dev
FROM history;
