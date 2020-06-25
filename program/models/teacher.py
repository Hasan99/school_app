from program.db import db
from datetime import datetime

class_teacher = db.Table("class_teacher",
                         db.Column("class_id", db.Integer, db.ForeignKey('classes.id'), primary_key=True),
                         db.Column("teacher_id", db.String(13), db.ForeignKey('teachers.cnic'), primary_key=True)
                         )


class TeacherModel(db.Model):
    __tablename__ = "teachers"

    cnic = db.Column(db.String(13), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now)

    classes = db.relationship("ClassModel", secondary=class_teacher, lazy="dynamic",
                              backref=db.backref("teachers", lazy="dynamic"))

    def __init__(self, cnic, name, gender, date_of_birth, phone_number):
        self.cnic = cnic
        self.name = name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number

    def json(self):
        return {
            "teacher": {
                "cnic": self.cnic,
                "name": self.name,
                "gender": self.gender,
                "date_of_birth": self.date_of_birth,
                "phone_number": self.phone_number,
                "registration_date": self.registration_date
            },
            "classes": [class_.json() for class_ in self.classes.all()],
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_cnic(cls, cnic):
        return cls.query.filter_by(cnic=cnic).first()
