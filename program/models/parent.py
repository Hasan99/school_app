from program.db import db


class ParentModel(db.Model):
    __tablename__ = "parents"

    father_cnic = db.Column(db.String(13), primary_key=True)
    father_name = db.Column(db.String(50), nullable=False)
    mother_name = db.Column(db.String(50), nullable=False)
    father_occupation = db.Column(db.String(50))
    mobile_number = db.Column(db.String(11), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)

    children = db.relationship("StudentModel", lazy="dynamic", cascade="all, delete, delete-orphan",
                               single_parent=True, backref="parent")

    def __init__(self, father_cnic, father_name, mother_name, father_occupation, mobile_number, address):
        self.father_cnic = father_cnic
        self.father_name = father_name
        self.mother_name = mother_name
        self.father_occupation = father_occupation
        self.mobile_number = mobile_number
        self.address = address

    def json(self):
        return {
            "parent": {
                "father cnic": self.father_cnic,
                "father name": self.father_name,
                "mother name": self.mother_name,
                "father occupation": self.father_occupation,
                "mobile number": self.mobile_number,
                "address": self.address,
            },
            "children": [child.json() for child in self.children.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_father_cnic(cls, father_cnic):
        return cls.query.filter_by(father_cnic=father_cnic).first()
