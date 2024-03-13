from flask import request, Response
from bson import json_util, ObjectId
from pymongo import MongoClient

from config.mongodb import coll
 
def create_todo_service():
    data = request.get_json()
    title = data.get("title", None)
    description = data.get("description", None)
    if title:
      response = coll.insert_one({
        "title": title,
        "description": description,
        "done": False
      })
      result = {
        "id": str(response.inserted_id),
        "title": title,
        "description": description,
        "done": False
      }
      return result
    else:
      return 'Invalid payload', 400
    
def get_todos_service():
    data = coll.find()
    result = json_util.dumps(data)
    return Response(result, mimetype='application/json')

def get_todo_service(id):
    data = coll.find_one({'_id': ObjectId(id)})
    result = json_util.dumps(data)
    return Response(result, mimetype='application/json')

def update_todo_service(id):
    data = request.get_json()
    if len(data) == 0:
      return 'Invalid payload', 400
    
    response = coll.update_one({'_id': ObjectId(id)}, {'$set': data})

    if response.modified_count >= 1:
        return 'Todo updated successfully', 200
    else:
        return 'Todo not found', 404

def delete_todo_service(id):
    response = coll.delete_one({'_id': ObjectId(id)})
    if response.deleted_count >= 1:
        return 'Todo deleted successfully', 200
    else:
        return 'Todo not found', 404