import uuid
import re
from flask import Flask,request
from flask_smorest import abort
from db import depts,items

app = Flask(__name__)


@app.get("/dept/all")
def getAllDepts():
    # Should return all departments name
    return { "all_depts": list(depts.keys()) }, 200

@app.get("/dept/<string:value>")
def getSubcategories(value):
    # Should return all sub-categories in one dept 'value'
    if value in depts.keys():
        return { value: list(depts[value]["subcategories"])} , 200
    else:
        abort(404,"Department not found")

@app.get("/dept/<string:value>/items")
def getItems(value):
    # Should return all items of one particular dept
    try: 
        return { value: list(depts[value]["items"].values()) }
    except:
        abort(404,"Department not found")

@app.get("/items/all")
def getAllItems():
    # Should return all items from all departments
    return items, 200
    
@app.get("/items/<int:item_id>")
def getItemInfo(item_id):
    # Should return name, price, department (and subcategory), and short description
    try:
        return items[item_id], 200
    except:
        abort(404,message="Item not found")

@app.post("/item/new-registry")
def postNewItem():
    ''' JSON examples for item registry:
    {
        "upc":"035000671226",
        "name":"Colgate - Total Advanced Mouthwash - Peppermint 16.90 fl oz.",
        "price":8.99,
        "department": { "main":"Beauty", "subcategory":"Personal Care" }
    }

    { 
        "upc":"036632071132",
        "name":"Horizon Organic Whole Milk 12Pack x 8 fl oz",
        "cost": 8.99,
        "price": 13.79,
        "department":"Dairy"
    }
    '''
    item_info = request.get_json()

    if ("upc" not in item_info 
        or "name" not in item_info 
        or "price" not in item_info 
        or "department" not in item_info):
        abort(400,"Bad request. One or more required fields (UPC number, name, price, and category) are needed.")
    
    item_id = int((uuid.uuid1().int)/10**35)
    if item_id in items.keys():
        abort(500,"Failed to register the item due to internal server error.")
    
    item = {**item_info,"id":item_id}
    
    if "cost" in item.keys():
        cost = item["cost"]
    else:
        cost = 0
    
    if type(item["department"])==str:
        subcate = None
    elif type(item["department"])==dict:
        subcate = item["department"]["subcategory"]
    items[item_id]= { 
        "id":item_id,
        "upc":item_info["upc"],
        "name":item_info["name"],
        "brand":re.split("\s",item_info["name"])[0],
        "finance": {"price":item_info["price"], "cost":cost},
        "display": {
            "dims":"local/disk/path/product/dimensions.pdf",
            "image":"local/disk/path/product/image.png"
        },
        "department":{
            "main":item_info["department"],
            "subcategory":subcate,
        },
        "performance":{
            "biweekly":0.00,
            "monthly":0.00
        }
    }

    return item, 201
    
@app.delete("/item/<int:item_id>")
def deleteItem(item_id):
    try:
        del items[item_id]
    except:
        abort(404,"Item not found.")    
    
    return "Deleted Item #"+str(item_id), 202

