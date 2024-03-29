from flask.views import MethodView
from flask_smorest import Blueprint, abort


from db import db
from models import DeptModel

blp = Blueprint("depts",__name__,description="Operations on departments")

""" @blp.route("/dept/<string:dept_name>/items")
class Dept(MethodView):
    def get(self,dept_name):
        dept_name = dept_name[0].upper()+dept_name[1:]
        try: 
            return { dept_name: list(depts[dept_name]["items"].values()) }, 200
        except:
            abort(404,message="Department not found") """

@blp.route("/dept/<string:dept_name>/")
class Dept(MethodView):
    @blp.response(200, DeptModel)
    def get(self, dept_id):
        #dept_name = dept_name[0].upper()+dept_name[1:]
        dept = DeptModel.query.get_or_404(dept_id)
        return dept
    
    
    
""" @blp.route("/dept/<string:dept_name>")
class DeptList(MethodView):
    def get(self,dept_name):
        dept_name = dept_name[0].upper()+dept_name[1:]
        dept = DeptModel.query.get_or_404(dept_name)
        return dept.
            
    def delete(self, dept_name):
        raise NotImplementedError("Deleting a dept is not forbidden.")
        
        """




    