import uuid
import re

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests

#from db import items,depts
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel

from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items",__name__,description="Operations on items")

""" @blp.route("/item/<int:item_id>")
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
"""
@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting an item is not implemented.")
       
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
            item.cost = item_data["cost"]
            item.performance = item_data["performance"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item
""" 
@blp.route("/item/new-registry")
class NewItem(MethodView):
    @blp.arguments(ItemSchema)
    def post(self, item_info): 
        
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
        
        return item, 201 """

@blp.route("/item/new-registry")
class NewItem(MethodView):
    @blp.arguments(ItemSchema)    
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        #item_id = int((uuid.uuid1().int)/10**35)

        #item = {**item_data,"id":item_id}
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item

""" @blp.route("/item/all")
class ItemList(MethodView):
    def get(self):
        return items, 202
    
    def delete(self):
        try:
            items.clear()
        except:
            abort(404,message="List of items was empty")    
        
        return "Deleted All Items", 202 """