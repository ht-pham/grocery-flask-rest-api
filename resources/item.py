import uuid
import re

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items,depts

blp = Blueprint("Items",__name__,description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    def get(self,item_id):
        try:
            return items[item_id], 200
        except:
            abort(404,message="Item not found")

    def put(self,item_id):
        '''
        Example: PUT /item/0

        JSON Payload:
            0:{
                "upc":"01234567891011",
                "name":"a product",
                
                "performance":{
                    "biweekly":3.25,
                    "monthly":2.00
                }
            }
        Example: PUT /item/<int>
            <int>:{
                "name":"Rebranded product",
                
                "performance":{
                    "biweekly":5.25,
                    "monthly":3.00
                }
            }
        
        Example: PUT /item/<int>
            <int>:{
                "name":"that new product",
                
                "department":{
                    "main":<dept_name>,
                    "subcategory":<subcategory>
                }
            }
        '''
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