from App.database import db

class serviceLog(db.Model):

    
    log_id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    student_id = db.Column(db.Integer,db.ForeignKey('student.student_id') ,nullable=False)
    staff_id= db.Column(db.Integer,db.ForeignKey('staff.staff_id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    
    student = db.relationship('student', backref=db.backref('service_logs', lazy=True))
    staff = db.relationship('staff', backref=db.backref('service_logs', lazy=True))
    
    def __init__(self, student_id, staff_id, date, hours):
        
        self.student_id = student_id
        self.staff_id = staff_id
        self.date = date
        self.hours = hours
        self.status = "pending"
        
    def set_status(self, status):
        """Set status."""
        if status in ["confirmation_requested","pending", "confirmed"]:
            self.status = status
            
        else:
            raise ValueError("Invalid status value")
    
    def get_log_details(self):
        return {
            'log_id': self.log_id,
            'student': self.student_id,
            'staff_id ': self.staff_id,
            'date': self.date,
            'hours': self.hours,
            'status': self.status
        }
    
    def check_status(self):
        """Check status."""
        return self.status
    