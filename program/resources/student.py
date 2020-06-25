from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from program.models.student import StudentModel


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument("gender", type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument("date_of_birth", type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument("phone_number", type=str)
    parser.add_argument("class_id", type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument("parent_id", type=str, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, b_form_cnic):
        student = StudentModel.find_by_b_form_cnic(b_form_cnic)
        if student:
            return student.json()
        return {"message": "student not found"}, 404

    @jwt_required()
    def post(self, b_form_cnic):
        if StudentModel.find_by_b_form_cnic(b_form_cnic):
            return {"message": f"A student with b_form_cnic '{b_form_cnic}' already exists."}, 400

        data = Student.parser.parse_args()

        student = StudentModel(b_form_cnic, **data)

        try:
            student.save_to_db()
        except:
            return {"message": "An error occurred while inserting the student data."}, 500

        return student.json(), 201

    @jwt_required()
    def delete(self, b_form_cnic):
        student = StudentModel.find_by_b_form_cnic(b_form_cnic)
        if student:
            student.delete_from_db()
        return {"message": "student deleted"}

    @jwt_required()
    def put(self, b_form_cnic):
        data = Student.parser.parse_args()

        student = StudentModel.find_by_b_form_cnic(b_form_cnic)

        if student is None:
            student = StudentModel(b_form_cnic, **data)
        else:
            student.name = data["name"]
            student.gender = data["gender"]
            student.date_of_birth = data["date_of_birth"]
            student.phone_number = data["phone_number"]
            student.class_id = data["class_id"]
            student.parent_id = data["parent_id"]

        student.save_to_db()
        return student.json()


class StudentList(Resource):
    @jwt_required()
    def get(self):
        return {"students": [student.json() for student in StudentModel.query.all()]}
