from datetime import datetime, timedelta
from typing import Optional
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import yfinance as yf
from sqlalchemy import or_, text
from models import db, Stock, History, MovingAverage, ZScore

app = Flask(__name__, static_folder="web/build")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/pygorithmic'

db.init_app(app)


@app.route("/")
def index():
  return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
  return send_from_directory(app.static_folder, path)


@app.route("/api/stocks")
def get_stocks():
    stocks = Stock.query.all()
    stocks_list = [stock.to_dict() for stock in stocks]
    return jsonify(stocks_list)

@app.route("/api/stocks/<symbol>")
def get_stock(symbol):
    stock = Stock.query.filter(Stock.symbol == symbol).one()
    return jsonify(stock.to_dict())

@app.route("/api/search")
def search_stock():
    text = request.args.get("text")
    stocks = Stock.query.filter(or_(Stock.symbol.ilike(f'%{text}%'), Stock.name.ilike(f'%{text}%'))).all()
    stocks_list = [stock.to_dict() for stock in stocks]
    return jsonify(stocks_list)


@app.route("/api/history/<symbol>")
def get_history(symbol):
    start_date = '1900-01-01'
    latest_history = History.query.filter(History.symbol == symbol).order_by(History.date.desc()).first()
    if latest_history is not None:
        start = latest_history.date + timedelta(days=2)
        start_date = start.strftime('%Y-%m-%d')

    ticker = yf.Ticker(symbol)
    new_history = ticker.history(start=start_date, end=datetime.today().strftime('%Y-%m-%d'))

    if len(new_history) > 0:
        new_history = new_history.reset_index()
        new_history['symbol'] = symbol
        new_history.columns = [col.lower() for col in new_history.columns]

        fields = ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']
        new_history = new_history[fields]
        new_history['date'] = new_history['date'].dt.strftime("%Y-%m-%d")

        db.session.bulk_insert_mappings(History, new_history.to_dict(orient='records'))
        db.session.execute(text('REFRESH MATERIALIZED VIEW moving_average'))
        db.session.commit();

    history = History.query.filter(History.symbol == symbol).order_by(History.date.asc()).all()
    history_list = [h.to_dict() for h in history]

    return jsonify(history_list)

@app.route("/api/history/<symbol>/zscore")
def get_zscore(symbol):
    row = db.session.execute(text("""
        select
            date,
            symbol,
            close,
            average,
            (close - average) / NULLIF(std_dev, 0) as z_score,
            case
            when (close - average) / NULLIF(std_dev, 0) < -2 then 'BUY'
            when (close - average) / NULLIF(std_dev, 0) > 2 then 'SELL'
            else 'HOLD'
            end as signal
        from
            moving_average
        where
            symbol = :symbol
        order by
            date
        desc
        limit 1;
    """), {'symbol': symbol}).fetchone();

    zscore = ZScore(
        date = row[0],
        symbol = row[1],
        close = row[2],
        average = row[3],
        z_score = row[4],
        signal = row[5],
    )

    return jsonify(zscore.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
