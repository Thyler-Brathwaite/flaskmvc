from App.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from .student import student

class leaderboard(db.Model):
   

    leaderboard_id = db.Column(db.Integer, primary_key=True)
    
    
    
    def __init__(self , id):
        self.leaderboard_id = id
        
        

    def rank_students(self):
       
        students = student.query.order_by(student.totalHours.desc()).all()
        
        leaderboard = [{"name": s.name, "hours": s.totalHours} for s in students]
        db.session.commit()
        print(leaderboard)