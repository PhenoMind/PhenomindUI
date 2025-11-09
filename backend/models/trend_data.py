from database import db

class TrendData(db.Model):
    __tablename__ = 'trend_data'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    mood = db.Column(db.Float)
    sleep = db.Column(db.Float)
    hrv = db.Column(db.Float)
    activity = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'day': self.day,
            'mood': self.mood,
            'sleep': self.sleep,
            'hrv': self.hrv,
            'activity': self.activity
        }
    
    def __repr__(self):
        return f'<TrendData {self.day} for Patient {self.patient_id}>'

