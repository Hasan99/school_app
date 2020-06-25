from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from program.security import authenticate, identity
from program.resources.user import User
from program.resources.parent import Parent, ParentList
from program.resources.student import Student, StudentList
from program.resources.class_ import Class, ClassList
from program.resources.teacher import Teacher, TeacherList, ClassTeacher

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "hello"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(Parent, "/parent")
api.add_resource(ParentList, "/parents")
api.add_resource(Student, "/student")
api.add_resource(StudentList, "/students")
api.add_resource(Class, "/class")
api.add_resource(ClassList, "/classes")
api.add_resource(Teacher, "/teacher")
api.add_resource(TeacherList, "/teachers")
api.add_resource(ClassTeacher, "/class_teacher")
api.add_resource(User, "/register")

if __name__ == '__main__':
    from program.db import db

    db.init_app(app)
    app.run(debug=True)
