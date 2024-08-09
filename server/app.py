#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class Restaurants(Resource):
    def get(self):
        try:
            return make_response([restaurant.to_dict() for restaurant in Restaurant.query.all()], 200)
        except Exception as e:
                return make_response({
  "error": "Restaurant not found"
}, 404)   
        
api.add_resource(Restaurants, '/restaurants')
        

class RestaurantsById(Resource):
    def get(self, id):
        try:
            restaurant = db.session.get(Restaurant, id)
            if restaurant is None:
                return make_response({
  "error": "Restaurant not found"
}, 404)   
            else:
                return make_response(restaurant.to_dict(rules=('restaurant_pizzas',)),200)
        except:
                return make_response({
  "error": "Restaurant not found"
}, 404)   
        
    def delete(self,id):
        try:
            restaurant = db.session.get(Restaurant, id)
            if restaurant is None:
                return make_response({
  "error": "Restaurant not found"
}, 404)    
            else:
                db.session.delete(restaurant)
                db.session.commit()
                return make_response('', 204)
        except:
                return make_response("Restaurant not found", 404)

        
api.add_resource(RestaurantsById, '/restaurants/<int:id>')


class Pizzas(Resource):
    def get(self):
        try:
            return make_response([pizza.to_dict() for pizza in Pizza.query.all()], 200)
        except Exception as e:
            return make_response(str(e), 404)
        
api.add_resource(Pizzas, '/pizzas')


class RestaurantsPizzas(Resource):
    def post(self):

        try:
            data = request.get_json()
            new_rp = RestaurantPizza(**data)
            db.session.add(new_rp)
            db.session.commit()
            return make_response(new_rp.to_dict(),201)
        except Exception as e:
            db.session.rollback()
            return make_response({
  "errors": ["validation errors"]
}, 400)
        
api.add_resource(RestaurantsPizzas, '/restaurant_pizzas')






if __name__ == "__main__":
    app.run(port=5555, debug=True)
