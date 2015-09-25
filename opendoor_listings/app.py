from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from opendoor_listings.helpers import *
from opendoor_listings.models.home import Home, db
from geojson import Point, Feature, FeatureCollection
import geojson as geojson
import json as json

app = Flask(__name__)


# Handle 404 - not found errors
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


# Handle 500 - internal server errors
@app.errorhandler(Exception)
def internal_server_error(e):
    return jsonify(error=500, text=str(e)), 500


# Takes a dict of arguments and return a query that can be called to get Home objects
def create_query(args):
'''
I chose to use this function to 'sanitize' queries by checking certain inputs.
The posgresql 404(when badly formatted input was present) was much slower and not as informative as some of the input errors that I have documented.
I also chose to check the get requestes params, so sending random get params wouldn't return any data.
'''
    q = Home.query

    # If there are any unexpected get variables return -1
    for arg in args.keys():
        if not arg in ["min_bath", "max_bath", "min_bed", "max_bed", "min_price", "max_price"]:
            return -1

    # Parse all the arguments and get the required ones
    min_bath = args.get("min_bath")
    max_bath = args.get("max_bath")
    min_bed = args.get("min_bed")
    max_bed = args.get("max_bed")
    min_price = args.get("min_price")
    max_price = args.get("max_price")

    # For each parameter pair (min & max) check if max >= min and check if both min & max are properly formatted
    if min_bath and max_bath:
       if check_input(min_bath) and check_input(max_bath):
            if check_max_min(max_bath, min_bath):
                q = q.filter(Home.bathrooms >= min_bath)
                q = q.filter(Home.bathrooms <= max_bath)
            else:
                return -1
       else:
            return -1

    # For each single parameter check if the input is properly defined 
    elif min_bath:
        if check_input(min_bath):
            q = q.filter(Home.bathrooms >= min_bath)
        else:
            return -1

    elif max_bath:
        if check_input(max_bath):
            q = q.filter(Home.bathrooms <= max_bath)
        else:
            return -1

    if min_price and max_price:
       if check_input(min_price) and check_input(max_price):
            if check_max_min(max_price, min_price):
                q = q.filter(Home.price >= min_price)
                q = q.filter(Home.price <= max_price)
            else:
                return -1
       else:
            return -1

    elif min_price:
        if check_input(min_price):
            q = q.filter(Home.price >= min_price)
        else:
            return -1

    elif max_price:
        if check_input(max_price):
            q = q.filter(Home.price <= max_price)
        else:
            return -1

    if min_bed and max_bed:
       if check_input(min_bed) and check_input(max_bed):
            if check_max_min(max_bed, min_bed):
                q = q.filter(Home.bedrooms >= min_bed)
                q = q.filter(Home.bedrooms <= max_bed)
            else:
                return -1
       else:
            return -1

    elif min_bed:
        if check_input(min_bed):
            q = q.filter(Home.bedrooms >= min_bed)
        else:
            return -1

    elif max_bed:
        if check_input(max_bed):
            q = q.filter(Home.bedrooms <= max_bed)
        else:
            return -1

    # Return the query 
    return q


# Call listings based on get variables
@app.route("/listings", methods=["GET"])
def pull_listings():
    # Only support GET requests for now
    if request.method != "GET":
        return jsonify(error=500, text="Bad Request. We only support GET Operations")

    results = create_query(request.args)

    if results == -1:
        return jsonify(error=500, text="Bad Request. Bad parameters")

    features = []

    # if there are no results, return no results
    if len(results.all()) < 1:
        return jsonify(error=404, text="No Houses found for given parameters")

    # Format our output to GeoJson
    for row in results.all():
        row = row.serialize
        try:
            p = Point((row['lon'], row['lat']))
            row.pop('lat')
            row.pop('lon')
        except Exception, e:
            return jsonify(error=500, text="Data returned is not properly formatted")

        f = Feature(geometry=p, properties=row)
        features.append(f)

    return geojson.dumps(FeatureCollection(features), indent=4)
