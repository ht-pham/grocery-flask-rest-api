import uuid
import re

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests

from db import items,depts
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items",__name__,description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    def get(self,item_id):
        try:
            return items[item_id], 200
        except:
            abort(404,message="Item not found")

    @blp.arguments(ItemUpdateSchema)
    def put(self,new_info,item_id):
        try:
            # get the latest info of the item_id item
            item = items[item_id]
            # append the new info into the saved data
            item |= new_info 

            return item
        except requests.HTTPError:
            abort("404",message= "Item not found")

    def delete(self,item_id):
        try:
            del items[item_id]
        except:
            abort(404,message="Item not found.")    
        
        msg = "Deleted Item #"+str(item_id)
        return msg, 202

@blp.route("/item/new-registry")
class NewItem(MethodView):
    @blp.arguments(ItemSchema)
    def post(self, item_info):
        ''' 
        JSON examples for item registry:
        {
            "upc":"035000671226",
            "name":"Colgate - Total Advanced Mouthwash - Peppermint 16.90 fl oz.",
            "price":8.99,
            "department": { "main":"Beauty", "subcategory":"Personal Care" }
        }
        
        {
            "upc":"037000009924",
            "name":"Tide Pods Spring Meadow Laundry Detergent Pacs, 42 Count",
            "price":12.97,
            "cost":10.49,
            "department": { "main":"Household", "subcategory":"Laundry Detergent" }
        }
        
        {
            "upc":"075070104446",
            "name":"Peace Cereal Clusters and Flakes Cereal Wild Berry 10 oz.",
            "price":5.99,
            "cost":3.99,
            "department":"Breakfast"
        }

        { 
            "upc":"036632071132",
            "name":"Horizon Organic Whole Milk 12Pack x 8 fl oz",
            "cost": 8.99,
            "price": 13.79,
            "department":"Dairy"
        }

        {
            "upc":"041570056707",
            "name": "Almond Breeze - Unsweetened Original Almond Milk 64.00 fl oz",
            "price":4.99,
            "cost":3.49,
            "department":{"main":"Dairy","subcategory":"Non-dairy"}
        }
        '''
        item_id = int((uuid.uuid1().int)/10**35)
        if item_id in items.keys():
            abort(500,message="Failed to register the item due to internal server error.")
        
        item = {**item_info,"id":item_id}
        
        items[item_id]= { 
            "id":item_id,
            "upc":item_info["upc"],
            "name":item_info["name"],
            "brand":re.split("\s",item_info["name"])[0],
            "finance": {"price":item_info["price"], "cost":item_info["cost"]},
            "display": {
                "dims":"local/disk/path/product/dimensions.pdf",
                "image":"local/disk/path/product/image.png"
            },
            "department":item_info["department"],
            "performance":{
                "biweekly":0.00,
                "monthly":0.00
            }
        }
        main = item_info["department"]["main"]
        depts[main]["items"][item_id]=items[item_id]
        
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