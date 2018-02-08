import pymongo

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://hiffin:67524106@ds121238.mlab.com:21238/cloudapps")
db = client.cloudapps


 
current_tasks = db.task_list


def save_task(task):
    task_id = current_tasks.insert_one(task).inserted_id
    return str(task_id)

def get_task(task_id):

    object_id = ObjectId(task_id)

    task = current_tasks.find_one({'_id': object_id})
    return task

def get_task_list():
    return list(current_tasks.find())

def delete_task(task_id):
    object_id = ObjectId(task_id)
    task = current_tasks.delete_one({'_id': object_id})
    return

def update_task(task_id, description=None,status=None):
    updates = {}
    object_id = ObjectId(task_id)
    if description:
        updates['description'] = description
    if status:
        updates['status'] = status
    current_tasks.update_one({'_id':object_id}, {"$set": updates},upsert=False)
    return