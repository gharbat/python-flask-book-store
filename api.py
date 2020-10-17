from flask import Flask, request
from pymongo import MongoClient
import json
from bson import json_util, ObjectId

app = Flask(__name__)
client = MongoClient()
db = client['gdg']
collection = db['books']


@app.route("/", methods=["GET"])
def index():
    return {"result": "Hello World"}


@app.route("/create", methods=["POST"])
def create():
    payload = json.loads(request.get_data())
    collection.insert_one(payload)
    return {}


@app.route("/show", methods=["GET"])
def show_all():
    books = list(collection.find())
    return json.dumps(books, default=json_util.default)


@app.route("/show/<id>", methods=["GET"])
def show(id):
    book = list(collection.find({"_id": ObjectId(id)}))
    return json.dumps(book, default=json_util.default)


@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    collection.remove({"_id": ObjectId(id)})
    return {"status": "ok"}


@app.route("/update", methods=["GET"])
def update():
    payload = json.loads(request.get_data())
    id = payload.get("id")
    update = payload.get("update")
    collection.update_one({"_id": ObjectId(id)}, {"$set": update})
    return {}


app.run()
