from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    item_id = fields.Int(dump_only=True)
    upc = fields.Str(required=True)
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    price = fields.Float()
    cost = fields.Float()
    department=fields.Str()
    subcategory = fields.Str()

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    cost = fields.Float()
    performance=fields.Float()

class PlainDeptSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class DeptSchema(PlainDeptSchema):
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    