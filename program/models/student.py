from datetime import datetime

from program.db import db


class StudentModel(db.Model):
    __tablename__ = "students"

    b_form_cnic = db.Column(db.String(13), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(11))
    registration_date = db.Column(db.DateTime, default=datetime.now)

    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    parent_id = db.Column(db.String(13), db.ForeignKey("parents.father_cnic"), nullable=False)

    class_ = db.relationship("ClassModel")
    parent = db.relationship("ParentModel")

    def __init__(self, b_form_cnic, name, gender, date_of_birth, phone_number, class_id, parent_id):
        self.b_form_cnic = b_form_cnic
        self.name = name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.class_id = class_id
        self.parent_id = parent_id

    def json(self):
        return {
            "b_form_cnic": self.b_form_cnic,
            "name": self.name,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "phone_number": self.phone_number,
            "registration_date": self.registration_date,
            "class_id": self.class_id,
            "parent_id": self.parent_id
        }

    @classmethod
    def find_by_b_form_cnic(cls, b_form_cnic):
        return cls.query.filter_by(b_form_cnic=b_form_cnic).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
