from pprint import pprint
from bson import ObjectId

from flask import Flask, jsonify, request
import pymongo

from linkedin import LinkedIn

app = Flask(__name__)
mongo_url = "mongodb+srv://tom:jHq13Y2ru1y5Dijb@cluster0.crkabz3.mongodb.net/?retryWrites=true&w=majority"

def update_autoapply(id, update={}):
    client = pymongo.MongoClient(mongo_url)
    db = client.get_database('tools')
    collection = db.get_collection('automnations')
    collection.update_one({"_id": ObjectId(id)}, update)


@app.route('/multi_apply', methods=['POST'])
def multi_apply():
    pprint(request.json)

    _id = request.json['_id']

    update_autoapply(_id, {
        "$set": {
            "status": "active",
            "active": True,
            "message": "Initialisation ..."
        }
    })

    client = pymongo.MongoClient(mongo_url)
    db = client.get_database('tools')
    collection = db.get_collection('automnations')
    automnation = collection.find_one({"_id": ObjectId(_id)})
    pprint('------------')
    pprint(automnation)

    try:
        if automnation.get('website') == 'linkedin.com':
            bot = LinkedIn(automnation)
        bot.multi_apply()
        pprint(bot.data)
    except:
        update_autoapply(_id, {
            "$set": {
                "status": "inactif",
                "active": False,
                "message": "Une erreur est survenue"
            },
            "$inc": {
                "result.error": 1
            }
        })
    return jsonify(bot.data)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
    return response


if __name__ == '__main__':
    app.run(debug=True)
