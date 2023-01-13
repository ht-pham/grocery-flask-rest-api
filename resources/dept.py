from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import depts

blp = Blueprint("depts",__name__,description="Operations on departments")

@blp.route("/dept/<string:value>/items")
class Dept(MethodView):
    def get(self,value):
        value = value[0].upper()+value[1:]
        try: 
            return { value: list(depts[value]["items"].values()) }, 200
        except:
            abort(404,message="Department not found")

@blp.route("/dept/<string:dept_name>")
class DeptList(MethodView):
    def get(self,dept_name):
        if dept_name=="all":
            return { "all_depts": list(depts.keys()) }, 200

        dept_name = dept_name[0].upper()+dept_name[1:]
        try:
            return { dept_name: list(depts[dept_name]["subcategories"])} , 200
        except KeyError:
            abort(404,message="Store not found")


