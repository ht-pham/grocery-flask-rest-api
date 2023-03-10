from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    upc = db.Column(db.String(14),unique=True,nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    price = db.Column(db.Float(precision=2),unique=False,nullable=False)
    cost = db.Column(db.Float(precision=2),unique=False,nullable=False)
    
    brand = db.Column(db.String(40),unique=False)
    
    dept_id = db.Column(db.String(2),db.ForeignKey("depts.id"))
    dept = db.relationship("DeptModel",back_populates="items")
    subcategory = db.Column(db.String(40))

    biweek_mvmt = db.Column(db.Float(precision=2),unique=False,nullable=False)
    monthly_mvmt = db.Column(db.Float(precision=2),unique=False,nullable=False)