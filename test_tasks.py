import tasks

import pymongo

from pymongo import MongoClient


def test_get_tasks():
    task_l = tasks.get_task_list()
    assert type(task_l) is list

def test_save_task():
    tasks.save_task({"description":"Do something", "status": "1"})
    task_list = tasks.get_task_list()
    assert type(task_list) is list

    found = False
    for task in task_list:
        if task["description"] =="Do something":
            found = True
    
    assert found


def test_get_task():
    task_id = tasks.save_task({"description":"this is a test task", "status": "1"})
    assert type(task_id) is str
    task = tasks.get_task(task_id)
    print(task)
    print(type(task))

    assert task['description'] == "this is a test task"
   

def test_mongo_client():
    assert type(tasks.client) is MongoClient
    assert tasks.db
    print (type(tasks.db))

def test_delete_task():
    task_id = tasks.save_task({"description":"this is a delete task", "status": "1"})
    task_list = tasks.get_task_list()

    found = False
    for task in task_list:
        if "delete" in task['description']:
            found = True
    assert found
    tasks.delete_task(task_id)

    task_list = tasks.get_task_list()
    found = False
    for task in task_list:
        if "delete" in task['description']:
            found = True
           
    
    assert not found
   

def test_update_task():
    task_id = tasks.save_task({"description":"before update", "status": "1"})
    task = tasks.get_task(task_id)
    assert task['description'] == "before update"

    tasks.update_task(task_id,"after update")

    task = tasks.get_task(task_id)

    assert task['description'] == "after update"
