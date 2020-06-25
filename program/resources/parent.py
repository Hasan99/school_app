from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from program.models.parent import ParentModel


class Parent(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("father_name", type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument("mother_name", type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument("father_occupation", type=str)
    parser.add_argument("mobile_number", type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument("address", type=str, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, father_cnic):
        parent = ParentModel.find_by_father_cnic(father_cnic)
        if parent:
            return parent.json()
        return {"message": "parent not found"}, 404

    @jwt_required()
    def post(self, father_cnic):
        if ParentModel.find_by_father_cnic(father_cnic):
            return {"message": f"A parent with cnic '{father_cnic}' already exists."}, 400

        data = Parent.parser.parse_args()

        parent = ParentModel(father_cnic, **data)
        try:
            parent.save_to_db()
        except:
            return {"message": "An error occurred while inserting the parent data."}, 500

        return parent.json(), 201

    @jwt_required()
    def put(self, father_cnic):
        data = Parent.parser.parse_args()

        parent = ParentModel.find_by_father_cnic(father_cnic)

        if parent is None:
            parent = ParentModel(**data)
        else:
            parent.father_name = data["father_name"]
            parent.mother_name = data["mother_name"]
            parent.father_occupation = data["father_occupation"]
            parent.mobile_number = data["mobile_number"]
            parent.address = data["address"]

        try:
            parent.save_to_db()
        except:
            return {"message": "An error occurred while inserting data."}, 500
        return parent.json()

    @jwt_required()
    def delete(self, father_cnic):
        parent = ParentModel.find_by_father_cnic(father_cnic)
        if parent:
            try:
                parent.delete_from_db()
            except:
                return {"message": "An error occurred while deleting data."}, 500

        return {"message": "parent deleted"}


class ParentList(Resource):
    @jwt_required()
    def get(self):
        return {"stores": [parent.json() for parent in ParentModel.query.all()]}
