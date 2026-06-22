from app.models import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    statut = db.Column(db.String(20), default="PENDING")

    date_reservation = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Booking user={self.user_id} event={self.event_id}>"
    
    __table_args__ = (
    db.UniqueConstraint("user_id", "event_id", name="unique_user_event"),
    )

    def __repr__(self):
        return f"<Booking {self.id}>"