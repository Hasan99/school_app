from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from program.models.teacher import TeacherModel
from program.models.class_ import ClassModel


class Teacher(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument("gender", type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument("date_of_birth", type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument("phone_number", type=str, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, cnic):
        teacher = TeacherModel.find_by_cnic(cnic)
        if teacher:
            return teacher.json()
        return {"message": "teacher not found"}, 404

    @jwt_required()
    def post(self, cnic):
        if TeacherModel.find_by_father_cnic(cnic):
            return {"message": f"A teacher with cnic '{cnic}' already exists."}, 400

        data = Teacher.parser.parse_args()

        teacher = TeacherModel(cnic, **data)
        try:
            teacher.save_to_db()
        except:
            return {"message": "An error occurred while inserting the teacher data."}, 500

        return teacher.json(), 201

    @jwt_required()
    def put(self, cnic):
        data = Teacher.parser.parse_args()

        teacher = TeacherModel.find_by_cnic(cnic)

        if teacher is None:
            teacher = TeacherModel(cnic, **data)
        else:
            teacher.name = data["name"]
            teacher.gender = data["gender"]
            teacher.date_of_birth = data["date_of_birth"]
            teacher.phone_number = data["phone_number"]
        teacher.save_to_db()
        return teacher.json()

    @jwt_required()
    def delete(self, cnic):
        teacher = TeacherModel.find_by_cnic(cnic)
        if teacher:
            teacher.delete_from_db()

        return {"message": "teacher deleted"}


class TeacherList(Resource):
    @jwt_required()
    def get(self):
        return {"teachers": [teacher.json() for teacher in TeacherModel.query.all()]}


class ClassTeacher(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("class_id", type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument("teacher_id", type=str, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def post(self):
        data = ClassTeacher.parser.parse_args()

        class_id = data["class_id"]

        class_ = ClassModel.find_by_id(class_id)

        if class_ is None:
            return {"message": "class not found"}, 404

        teacher_id = data["teacher_id"]

        teacher = TeacherModel.find_by_cnic(teacher_id)

        if teacher is None:
            return {"message": "teacher not found"}, 404

        from program.db import db

        try:
            class_.teachers.append(teacher)
            db.session.commit()
        except:
            return {"message": "An error occurred while inserting data."}, 500

        return {"message": "teacher assigned successfully"}, 201
