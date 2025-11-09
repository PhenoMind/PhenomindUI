from app import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    avatar = db.Column(db.String(255))
    initials = db.Column(db.String(10))
    disorder = db.Column(db.String(50), nullable=False)
    disorder_full = db.Column(db.String(200), nullable=False)
    medications = db.Column(db.JSON)  # List of medication strings
    last_visit = db.Column(db.String(50))
    risk_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ehr = db.relationship('EHR', backref='patient', uselist=False, cascade='all, delete-orphan')
    wearable = db.relationship('Wearable', backref='patient', uselist=False, cascade='all, delete-orphan')
    timeline_events = db.relationship('TimelineEvent', backref='patient', lazy='dynamic', cascade='all, delete-orphan')
    trend_data = db.relationship('TrendData', backref='patient', lazy='dynamic', cascade='all, delete-orphan', order_by='TrendData.day')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'avatar': self.avatar,
            'initials': self.initials,
            'disorder': self.disorder,
            'disorderFull': self.disorder_full,
            'medications': self.medications or [],
            'lastVisit': self.last_visit,
            'riskScore': self.risk_score,
            'ehr': self.ehr.to_dict() if self.ehr else None,
            'wearables': self.wearable.to_dict() if self.wearable else None,
            'timeline': [event.to_dict() for event in self.timeline_events.all()],
            'trendData': [data.to_dict() for data in self.trend_data.all()]
        }
    
    def __repr__(self):
        return f'<Patient {self.name}>'

