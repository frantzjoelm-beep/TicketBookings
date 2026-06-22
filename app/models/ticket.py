from app.models import db

class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)

    evenement = db.Column(db.String(100), nullable=False)

    date_evenement = db.Column(db.String(50), nullable=False)

    nombre_places = db.Column(db.Integer, nullable=False)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="PENDING"
)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Ticket {self.evenement}>"