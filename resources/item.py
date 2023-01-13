import uuid
import re

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items,depts

blp = Blueprint("Items",__name__,description="Operations on items")

@blp.route("item/<int:item_id>")
class Item(MethodView):
    def get(self,item_id):
        try:
            return items[item_id], 200
        except:
            abort(404,message="Item not found")

    def put(self,item_id):
        new_info = request.get_json()

        missing_key_info = ("name" not in new_info) and ("upc" not in new_info)
        no_change_of_dept = "department" not in new_info 
        no_change_of_price = "finance" not in new_info 
        no_statistics = "performance" not in new_info 
        if (missing_key_info) and (no_change_of_dept or no_change_of_price or no_statistics):
            abort(400,message="Bad request. Ensure either 'name' or 'upc' is in JSON payload")
        
        try:
            # get the latest info of the item_id item
            item = items[item_id]
            # append the new info into the saved data
            item |= new_info 

            return item
        except:
            abort("404",message="Item not found")

    def delete(self,item_id):
        try:
            del items[item_id]
        except:
            abort(404,message="Item not found.")    
        
        msg = "Deleted Item #"+str(item_id)
        return msg, 202

@blp.route("/item/new-registry")
class NewItem(MethodView):
    def post(self):
        item_info = request.get_json()

        if ("upc" not in item_info 
            or "name" not in item_info 
            or "price" not in item_info 
            or "department" not in item_info):
            abort(400,message="Bad request. One or more required fields (UPC number, name, price, and category) are needed.")
        
        item_id = int((uuid.uuid1().int)/10**35)
        if item_id in items.keys():
            abort(500,message="Failed to register the item due to internal server error.")
        
        item = {**item_info,"id":item_id}
        
        if "cost" in item.keys():
            cost = item["cost"]
        else:
            cost = 0
        
        if type(item["department"])==str:
            main_dept = item_info["department"][0].upper()+item_info["department"][1:]
            subcate = None
        elif type(item["department"])==dict:
            main_dept = item["department"]["main"]
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
                "main":main_dept,
                "subcategory":subcate,
            },
            "performance":{
                "biweekly":0.00,
                "monthly":0.00
            }
        }
        
        depts[main_dept]["items"][item_id]=items[item_id]

        return item, 201

@blp.route("/item/all")
class ItemList(MethodView):
    def get(self):
        return items, 202
    def delete(self):
        try:
            items.clear()
        except:
            abort(404,message="List of items was empty")    
        
        return "Deleted All Items", 202