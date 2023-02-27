from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/rutvik/Documents/colaberry_app/src/db_reset/database.db'
print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Readings(db.Model):
    __tablename__ = 'readings'
    reading_id = db.Column(db.String(18), primary_key=True)
    station_id = db.Column(db.String(11), unique=False,
                           nullable=False, index=True)
    year = db.Column(db.Integer, unique=False, nullable=True, index=True)
    month = db.Column(db.Integer, unique=False, nullable=True, index=True)
    day = db.Column(db.Integer, unique=False, nullable=True, index=True)
    max_temperature = db.Column(db.Float(4), unique=False, nullable=True)
    min_temperature = db.Column(db.Float(4), unique=False, nullable=True)
    precipitation = db.Column(db.Float(4), unique=False, nullable=True)
    schema = 'coding_exercise'

    def __repr__(self):
        return f"Readings('{self.reading_id}', '{self.station_id}', '{self.year}-{self.month}-{self.day}', '{self.max_temperature}', '{self.min_temperature}', '{self.precipitation}')"


class ReadingsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Readings
        ordered = True
        # Fields to expose
        fields = ('reading_id', 'station_id', 'year', 'month', 'day', 'max_temperature',
                  'min_temperature', 'precipitation')
        # Smart hyperlinking
        record = ma.HyperlinkRelated('record_detail')
    reading_id = ma.auto_field()
    station_id = ma.auto_field()
    year = ma.auto_field()
    month = ma.auto_field()
    day = ma.auto_field()
    max_temperature = ma.auto_field()
    min_temperature = ma.auto_field()
    precipitation = ma.auto_field()


reading_schema = ReadingsSchema()
readings_schema = ReadingsSchema(many=True)


class Results(db.Model):
    __tablename__ = 'results'
    result_id = db.Column(db.String(15), primary_key=True)
    year = db.Column(db.Integer, unique=False, nullable=True, index=True)
    station_id = db.Column(db.String(11), unique=False,
                           nullable=False, index=True)
    avg_max_temperature = db.Column(db.Float(4), unique=False, nullable=True)
    avg_min_temperature = db.Column(db.Float(4), unique=False, nullable=True)
    total_accumulated_precipitation = db.Column(
        db.Float(4), unique=False, nullable=True)
    schema = 'coding_exercise'

    def __repr__(self):
        return f"Results('{self.result_id}', '{self.year}', '{self.station_id}', '{self.avg_max_temperature}', '{self.avg_min_temperature}', '{self.total_accumulated_precipitation}')"


class ResultsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Results
        ordered = True
        # Fields to expose
        fields = ('result_id', 'year', 'station_id', 'avg_max_temperature',
                  'avg_min_temperature', 'total_accumulated_precipitation')
        # Smart hyperlinking
        stat = ma.HyperlinkRelated('stat_detail')
    result_id = ma.auto_field()
    year = ma.auto_field()
    station_id = ma.auto_field()
    avg_max_temperature = ma.auto_field()
    avg_min_temperature = ma.auto_field()
    total_accumulated_precipitation = ma.auto_field()


result_schema = ResultsSchema()
results_schema = ResultsSchema(many=True)


if __name__ == '__main__':
    app.run(debug=True)
