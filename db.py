""" from flask_sqlalchemy import SQLAlchemy

db1 = SQLAlchemy()
 """
depts = {
    "Bakery":{
        "id":"BK",
        "subcategories":[],
        "brands":[],
        "items":{}
    },
    "Breakfast":{
        "id":"BF",
        "subcategories":[],
        "brands":[],
        "items":{}
    },
    "Beauty":{
        "id":"BT",
        "subcategories":[],
        "brands":[],
        "items":{}
    },
    "Dairy":{
        "id":"DR",
        "subcategories":["Whole Milk","Skim Milk","2%","Non-dairy"],
        "brands":[],
        "items":{}
    },
    "Fresh":{
        "id":"FR",
        "subcategories":[],
        "brands":[],
        "items":{}
    },
    "Frozen":{
        "id":"FZ",
        "subcategories":[],
        "brands":[],
        "items":{}
    },
    "General Merchandise":{
        "id":"GM",
        "subcategories":[],
        "brands":[],
        "items":{}
    },
    "Household":{
        "id":"HH",
        "subcategories":[],
        "brands":[],
        "items":{}
    },
    "Home Office":{
        "id":"HO",
        "subcategories":[],
        "brands":[],
        "items":{}
    },
    "Health":{
        "id":"HE",
        "subcategories":[],
        "brands":[],
        "items":{}
    }
}
items = {
    0:{
        "id":0,
        "upc":"01234567891011",
        "name":"a product",
        "brand":"Private brand",
        "finance": {"price":3.99, "cost":0.99},
        "display": {
            "dims":"local/disk/path/product/dimensions.pdf",
            "image":"local/disk/path/product/image.png"
        },
        "department":{
            "main":"uncategorized",
            "subcategory":"uncategorized"
        },
        "performance":{
            "biweekly":0.00,
            "monthly":0.00
        }
    }
    
}