import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Setup database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)


class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(200))
    status = db.Column(db.String(30))
    price = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    sq_ft = db.Column(db.Integer)
    lat = db.Column(db.Float())
    lon = db.Column(db.Float())

    @property
    # Serialize helps geojsonify the model
    def serialize(self):
        return {
                "id"       : self.id,
                "street"   : self.street,
                "status"   : self.status,
                "price"    : self.price,
                "bedrooms" : self.bedrooms,
                "bathrooms": self.bathrooms,
                "sq_ft"    : self.sq_ft,
                "lat"      : self.lat,
                "lon"      : self.lon
               }


    def __init__(self, id, street, status, price, bedrooms, bathrooms, sq_ft, lat, lon):
        self.id = id
        self.street = street
        self.status = status
        self.price = price
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.sq_ft = sq_ft
        self.lat = lat
        self.lon = lon


    def __repr__(self):
        return "<Home %r>" % self.street
