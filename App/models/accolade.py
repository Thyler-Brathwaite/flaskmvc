from App.database import db

student_accolade = db.Table(
    "student_accolade",
    db.Column("student_id", db.Integer, db.ForeignKey("student.student_id"), primary_key=True),
    db.Column("accolade_id", db.Integer, db.ForeignKey("accolade.accolade_id"), primary_key=True)
)

class accolade(db.Model):

    
    accolade_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    requirement_hours_upper = db.Column(db.Integer, nullable=False)
    requirement_hours_lower = db.Column(db.Integer, nullable=False)
    students = db.relationship('student', secondary='student_accolade', backref=db.backref('accolades', lazy='dynamic'))
    
    def __init__(self, name, lower, upper):
        
        self.name = name
        self.requirement_hours_lower = lower
        self.requirement_hours_upper = upper
    
    def check_eligibility(self, student):
        if student.totalHours >= self.requirement_hours_lower and (student.totalHours <= self.requirement_hours_upper or student.totalHours > self.requirement_hours_upper ):
            return True

        return False 