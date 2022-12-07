from flask import Flask, request, abort
import json
import random
from config import me
from mock_data import catalog
from config import db
from bson import ObjectId

app = Flask("server")


@app.get("/")  # the root endpoint
def home():
    return "hello from flask"


@app.get("/test")
def test():
    return "this is another endpoint"


#  CATALOG API

@app.get("/api/version")
def version():
    version = {
        "v": "v1.0.4",
        "name": "zombie rabbit"
    }
# parse a dictionary into a json string  for storage
    return json.dumps(version)


@app.get("/api/about")
def Info():
    return json.dumps(me)


@app.get("/api/catalog")
def catlog():
    # read from the db
    cursor = db.Products.find({})  # {} means filter for more specific searches
    results = []
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)


@app.post("/api/catalog")
def save_product():
    product = request.get_json()

    # validations
    # in statements is used to check for a  specific definition in an array
    if "title" not in product:
        return abort(400, "Title is required")
    if len(product["title"]) < 5:
        return abort(400, "title should contain 5 chars or mroe")
    if "category" not in product:
        return abort(400, "Category is required")
    if "price" not in product:
        return abort(400, "Price is required")
    if not isinstance(product["price"], (float, int)):
        return abort(400, "Price must be a valid number")
    if product["price"] < 0:
        return abort(400, "price must be greater then 0")

# sace products to db (database)
    # save the object, will assign an _id: ObjectID(uniqueValue)
    db.Products.insert_one(product)

    product["_id"] = str(product["_id"])

    return json.dumps(product)


@app.get("/api/test/count")
def Amount():
    count = db.Products.count_documents({})
    return json.dumps({"total": count})


@app.get("/api/catalog/<category>")
def by_category(category):
    # category is to be replaced by a keyword in a URL, so if a keyword in "category" matches with the one placed in the url, it will display the page with the lists.
    results = []
    cursor = db.Products.find({"category": category})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)


@app.get("/api/catalog/search/<text>")
def by_search(text):

    text = text.lower()
    results = []
    cursor = db.Products.find({"title": {"$regex": text, "$options": "i"}})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)

# return a list with all the categories inside


@app.get("/api/categories")
def cat_list():
    results = []
    cursor = db.Products.distinct("category")
    for cat in cursor:
        results.append(cat)

    return json.dumps(results)


@app.get("/api/test/value")
def price_list():
    total = 0
    cursor = db.Products.find({})
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)

    # create an endpoint that returns a poduct based on a given _id


@app.get("/api/product/<id>")
def id(id):
    objID = ObjectId(id)
    prod = db.Products.find_one({"_id": objID})
    if not prod:
        return abort(404, "product not found")

    prod["_id"] = str(prod["_id"])
    return json.dumps(prod)

# this endpoint will run through the array and return the cheapest product.


@app.get("/api/product/cheapest")
def cheap():
    cursor = db.Products.find({})
    cheapest = cursor[0]
    for product in cursor:
        if product["price"] < cheapest["price"]:
            cheapest = product

    return json.dumps(cheapest)


# app.run(debug=True)


# save: post api/coupons
# this allows you to creat new items and push it into the lsit database
@app.post("/api/coupons")
def save_coupon():
    coupon = request.get_json()

    if "code" not in coupon:
        return abort(400, "coupon code is required")

    if "discount" not in coupon:
        return abort(400, "discount is required")
    if not isinstance(coupon["discount"], (float, int)):
        return abort(400, "Price must be a valid number")

    db.Coupons.insert_one(coupon)

    coupon["_id"] = str(coupon)

    return json.dumps(coupon)

# get all get /api/coupons
# this is the list that contains all items created from coupons POST


@app.get("/api/coupons")
def couponlist():
    cursor = db.Coupons.find({})
    results = []
    for coup in cursor:
        coup["_id"] = str(coup["_id"])
        results.append(coup)

    return json.dumps(results)


# get by id
# retreive specific coupon ID from  database list
@app.get("/api/couponid/<id>")
def couponId(id):
    objID = ObjectId(id)
    coup = db.Coupons.find_one({"_id": objID})
    if not coup:
        return abort(404, "coupon not found")

    coup["_id"] = str(coup["_id"])
    return json.dumps(coup)


# get by code

@app.get("/api/coupons/<code>")
def by_code(code):

    coupon = db.Coupons.find_one({"code": code})
    if not coupon:
        return abort(404, "Invalid code")

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)
