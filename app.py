import uuid

from flask import Flask,request
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
    try:
        return { value: list(depts[value]["subcategories"].values())} 
    except:
        abort(404,"Department not found")

@app.get("/dept/<value>/items")
def listItemsOf(value):
    # Should return all items of one particular dept
    try: 
        return { value: list(depts[value]["items"].values()) }
    except:
        abort(404,"Department not found")

@app.get("/items/all")
def listAllItems():
    # Should return all items from all departments
    return items
    
@app.get("/items/<item_id>")
def getItemInfo(item_id):
    # Should return name, price, department (and subcategory), and short description
    try:
        return items[item_id]
    except:
        abort(404,message="Item not found")

@app.post("/item/new-registry")
def postNewItem():
    item_info = request.get_json()

    if ("upc" not in item_info 
        or "name" not in item_info 
        or "price" not in item_info 
        or "category" not in item_info):
        abort(400,"Bad request. One or more required fields (UPC number, name, price, and category) are needed.")
    
    item_id = int((uuid.uuid1().int)/10**32)
    if item_id in items.keys():
        abort(500,"Failed to register the item due to internal server error.")
    
    item = {**item_info,"id":item_id}
    items[item_id]=item

    return 201, item
    
@app.delete("/item/<item_id>")
def deleteItem(item_id):
    try:
        del items[item_id]
    except:
        abort(404,"Item not found.")    
    return 200, "Successfully deleted the item."

