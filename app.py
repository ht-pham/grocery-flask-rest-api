import uuid

from flask import Flask
from flask_smorest import abort
from db import depts,items

app = Flask(__name__)


@app.get("/dept/all")
def listAllDepts():
    # Should return all departments name
    return { "all_depts": list(depts.keys()) }

@app.get("/dept/<value>")
def listOfItems(value):
    # Should return all sub-categories in one dept 'value'
    return { value: list(depts[value]["subcategories"].values())} 

@app.get("/dept/<value>/items")
def listItemsOf(value):
    # Should return all items of one particular dept
    return { value: list(depts[value]["items"].values()) }

@app.get("/items/all")
def listAllItems():
    # Should return all items from all departments
    return { "all_items":list(items["all"].values())} 
    
@app.get("/items/<item_id>")
def getItemInfo(item_id):
    # Should return name, price, department (and subcategory), and short description
    try:
        return items[item_id]
    except:
        abort(404,message="Item not found")

@app.post("/item/new-registry")
def postNewItem(item_id):
    pass


