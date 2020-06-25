from flask_restful import Resource
from flask_jwt import jwt_required
from program.models.class_ import ClassModel


class Class(Resource):
    @jwt_required()
    def get(self, name):
        class_ = ClassModel.find_by_name(name)
        if class_:
            return class_.json()
        return {"message": "class not found"}, 404

    @jwt_required()
    def post(self, name):
        if ClassModel.find_by_name(name):
            return {"message": f"A class with name '{name}' already exists."}, 400

        class_ = ClassModel(name)
        try:
            class_.save_to_db()
        except:
            return {"message": "An error occurred while inserting the class data."}, 500

        return class_.json(), 201

    @jwt_required()
    def put(self, name):
        class_ = ClassModel.find_by_name(name)

        if class_ is None:
            class_ = ClassModel(name)
        else:
            class_.name = name
        try:
            class_.save_to_db()
        except:
            return {"message": "An error occurred while inserting data."}, 500
        return class_.json()

    @jwt_required()
    def delete(self, name):
        class_ = ClassModel.find_by_name(name)
        if class_:
            try:
                class_.delete_from_db()
            except:
                return {"message": "An error occurred while deleting data."}, 500

        return {"message": "class deleted"}


class ClassList(Resource):
    @jwt_required()
    def get(self):
        return {"stores": [class_.json() for class_ in ClassModel.query.all()]}
