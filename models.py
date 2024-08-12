from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Stock(db.Model):
    __tablename__ = 'stocks'

    symbol = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'name': self.name
        }

class History(db.Model):
    __tablename__ = 'history'

    symbol = db.Column(db.Text, nullable=False, primary_key=True)
    date = db.Column(db.Date, nullable=False, primary_key=True)
    open = db.Column(db.Numeric, nullable=False)
    high = db.Column(db.Numeric, nullable=False)
    low = db.Column(db.Numeric, nullable=False)
    close = db.Column(db.Numeric, nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'date': self.date,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume
        }

class MovingAverage(db.Model):
    __tablename__ = "moving_average"

    date = db.Column(db.Date, nullable=False, primary_key=True)
    symbol = db.Column(db.Text, nullable=False, primary_key=True)
    close = db.Column(db.Numeric, nullable=False)
    average = db.Column(db.Numeric, nullable=False)
    std_dev = db.Column(db.Numeric, nullable=False)

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'date': self.date,
            'close': self.close,
            'average': self.average,
            'std_dev': self.std_dev
        }

class ZScore(db.Model):
    symbol = db.Column(db.Text, primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    close = db.Column(db.Numeric)
    average = db.Column(db.Numeric)
    z_score = db.Column(db.Numeric)
    signal = db.Column(db.Text)

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'date': self.date,
            'close': self.close,
            'average': self.average,
            'z_score': self.z_score,
            'signal': self.signal
        }
