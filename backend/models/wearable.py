from database import db

class Wearable(db.Model):
    __tablename__ = 'wearables'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, unique=True)
    device = db.Column(db.String(100))
    last_sync = db.Column(db.String(50))
    heart_rate_avg = db.Column(db.Integer)
    heart_rate_resting = db.Column(db.Integer)
    heart_rate_max = db.Column(db.Integer)
    steps_avg = db.Column(db.Integer)
    steps_goal = db.Column(db.Integer)
    sleep_avg = db.Column(db.Float)
    sleep_goal = db.Column(db.Float)
    sleep_quality = db.Column(db.String(50))
    hrv_avg = db.Column(db.Integer)
    hrv_baseline = db.Column(db.Integer)
    active_minutes = db.Column(db.Integer)
    calories = db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'device': self.device,
            'lastSync': self.last_sync,
            'heartRate': {
                'avg': self.heart_rate_avg,
                'resting': self.heart_rate_resting,
                'max': self.heart_rate_max
            },
            'steps': {
                'avg': self.steps_avg,
                'goal': self.steps_goal
            },
            'sleep': {
                'avg': self.sleep_avg,
                'goal': self.sleep_goal,
                'quality': self.sleep_quality
            },
            'hrv': {
                'avg': self.hrv_avg,
                'baseline': self.hrv_baseline
            },
            'activity': {
                'activeMinutes': self.active_minutes,
                'calories': self.calories
            }
        }
    
    def __repr__(self):
        return f'<Wearable for Patient {self.patient_id}>'

