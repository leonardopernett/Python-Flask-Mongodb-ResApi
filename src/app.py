from flask import Flask,jsonify,request, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util,ObjectId
app = Flask(__name__)

app.config['MONGO_URI']='mongodb://localhost/pythondb'
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def createUser():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
         password_hash = generate_password_hash(password)
         id = mongo.db.users.insert_many([
            {
            "username":username,
             "password":password_hash,
             "email":email
            }
         ])

         response = {
             "id":str(id),
             "username":username,
             "password":password_hash,
             "email":email
         }
         return response
    else:
        return error_found()

@app.route('/users', methods=['GET'])
def getUsers():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")

@app.route('/users/<id>', methods=['GET'])
def getOneUser(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response)


@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    mongo.db.users.delete_one({'_id':ObjectId(id)})
    return jsonify({
        "message":"user with id " + id + " was deleted"
    })

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    username= request.json['username']
    password = request.json['password']
    email = request.json['email']
    hash_password = generate_password_hash(password)
    mongo.db.users.update_one({"_id":ObjectId(id)}, {'$set':{
        "usernaame":username,
        "password":hash_password,
        "email":email
    }})
    return jsonify({
        "message":"user updated"
    })

@app.errorhandler(404)
def error_found(error=None):
    response =jsonify({
        "message":"request no found "+ request.url,
        "status":404
    })
    response.status_code = 404
    return response

#server
if __name__ == '__main__':
    app.run(debug=True, port=4000)
