from marshmallow import Schema, fields

class ItemSchema(Schema):
    item_id = fields.Int(dump_only=True)
    upc = fields.Str(required=True)
    name = fields.Str(required=True)
    price = fields.Float()
    cost = fields.Float()
    department=fields.Dict()

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    cost = fields.Float()
    performance=fields.Float()
