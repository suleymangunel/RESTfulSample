from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from random import *

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cafes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def random():
    cafes = Cafe.query.all()
    random_item = choice(cafes)
    return random_item.name


@app.route("/search", methods=["GET"])
def search():
    _name = request.args.get("name")
    cafe = db.session.query(Cafe).filter_by(name=_name.replace("\"", "")).first()
    return str(cafe.id)


@app.route("/add", methods=["POST"])
def add():
    _id = request.args.get("id")
    _name = request.args.get("name")
    _name = _name.replace("\"", "")
    _map_url = "map_url"
    _img_url = "img_url"
    _location = "location"
    s1 = choice(["10", "20", "30", "40"])
    s2 = (choice(["10", "20", "30", "40"])+"-"+choice(["10", "20", "30", "40"]))
    _seats = choice([s1, s2, "50+"])
    _has_toilet = choice([True, False])
    _has_wifi = choice([True, False])
    _has_sockets = choice([True, False])
    _can_take_calls = choice([True, False])
    _coffee_price = "£"+choice(["1", "2"])+"."+choice(["10", "20", "30", "40", "50", "60", "70", "80", "90"])
    _Cafe = Cafe(id=_id,
                 name=_name,
                 map_url=_map_url,
                 img_url=_img_url,
                 location=_location,
                 seats=_seats,
                 has_toilet=_has_toilet,
                 has_wifi=_has_wifi,
                 has_sockets=_has_sockets,
                 can_take_calls=_can_take_calls,
                 coffee_price=_coffee_price)
    db.session.add(_Cafe)
    db.session.commit()
    cafe = db.session.query(Cafe).filter_by(name=_name).first()
    return str(cafe.name)


@app.route("/update", methods=["PATCH"])
def update():
    _id = request.args.get("id")
    _coffee_price = request.args.get("coffee_price")
    cafe = db.session.query(Cafe).get(_id)
    cafe.coffee_price = _coffee_price
    db.session.commit()
    return cafe.name


@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    cafe = db.session.query(Cafe).get(id)
    db.session.delete(cafe)
    db.session.commit()
    return cafe.name


@app.route("/random", methods=["TEST"])
def deneme():
    return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200


if __name__ == '__main__':
    app.run(debug=True)
