from App.database import db
from .serviceLog import serviceLog
class staff(db.Model):
    
    
    staff_id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    

    def __init__(self,  name, email, role):
       
        self.name = name
        self.email = email
        self.role = role

    def log_hours(self, student_id, date, hours):
        new_log = serviceLog(
        student_id=student_id,
        staff_id=self.staff_id,
        date=date,
        hours=hours,
            )
        
        db.session.add(new_log)
        db.session.commit()
        return new_log
        
    def confirm_hours(self, log_id):
        service_log = serviceLog.query.get(log_id)
        
        service_log.status = "confirmed"
        db.session.commit()

    

        
        