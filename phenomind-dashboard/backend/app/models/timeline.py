from app import db

class TimelineEvent(db.Model):
    __tablename__ = 'timeline_events'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    label = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20))  # 'med', 'alert', 'visit', 'survey'
    
    def to_dict(self):
        return {
            'date': self.date,
            'label': self.label,
            'type': self.type
        }
    
    def __repr__(self):
        return f'<TimelineEvent {self.date} for Patient {self.patient_id}>'

