from db import db

class DeptModel(db.Model):
    __tablename__ = "depts"

    id = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    items = db.relationship("ItemModel",back_populates="department",lazy="dynamic")
    