from App.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY



class student(db.Model):
 
    
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    leaderboard_id = db.Column(db.Integer, db.ForeignKey('leaderboard.leaderboard_id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    totalHours = db.Column(db.Integer, nullable=False)
    
    leaderboard=db.relationship('leaderboard', backref=db.backref('students', lazy=True))

    def __init__(self, name, email, totalHours):
       
        self.name = name
        self.email = email
        self.totalHours = totalHours
       

    
    def set_totalHours(self, totalHours):
        """Set totalHours."""
        self.totalHours = totalHours    
 
    
    def set_email(self, email):
        """Set email."""
        self.email = email

    def request_confirmation(self, log_id):
        from .serviceLog import serviceLog
        service_log = serviceLog.query.get(log_id)

        if service_log and service_log.student_id == self.student_id:
            if service_log.status == "pending":
                service_log.status = "confirmation_requested"
                return "confirmation_requested"
                db.session.commit()
            else:
                return "Hours have already been confirmed or confirmation already requested"
        
        else:
            return "Invalid log ID or unauthorized access"
           
    def view_accolades(self): 
        from .accolade import accolade
        accolades = accolade.query.all()
        earned = []

        for acc in accolades:
            if acc.check_eligibility(self):
                earned.append({
                "accolade_id": acc.accolade_id,
                "name": acc.name,
                "range": f"{acc.requirement_hours_lower}-{acc.requirement_hours_upper} hours"
                })
    
        return earned
    
    def view_leaderboard(leaderboard_id):
        from .leaderboard import leaderboard
        board = leaderboard.query.get(leaderboard_id)
        if board:
            board.rank_students()
        else:
            return "Leaderboard not found"
