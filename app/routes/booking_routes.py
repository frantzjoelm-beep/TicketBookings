from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user

from app.models import db
from app.models.booking import Booking
from app.models.event import Event
from app.models.user import User

booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/payer/<int:booking_id>")
@login_required
def payer(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    # sécurité : seul le propriétaire peut payer
    if booking.user_id != current_user.id:
        abort(403)

    # on ne peut payer qu'une réservation confirmée
    if booking.statut != "CONFIRMED":
        return "Cette réservation ne peut pas être payée."

    booking.statut = "PAID"

    db.session.commit()

    return redirect(url_for("booking.mes_reservations"))

# Réserver un événement
@booking_bp.route("/reserver/<int:event_id>")
@login_required
def reserver(event_id):

    event = Event.query.get_or_404(event_id)

    existing = Booking.query.filter_by(
        user_id=current_user.id,
        event_id=event_id
    ).first()

    if existing:
        return "Déjà réservé"

    total = Booking.query.filter_by(event_id=event_id).count()

    if total >= event.capacite:
        return "Événement complet"

    booking = Booking(
        user_id=current_user.id,
        event_id=event_id,
        statut="PENDING"
    )

    print("Utilisateur :", current_user.id)
    print("Événement :", event_id)
    print("Réservation en cours de création")

    db.session.add(booking)
    db.session.commit()

    print("Réservation enregistrée avec succès")

    return redirect(url_for("booking.mes_reservations"))


#  Mes réservations
@booking_bp.route("/mes-reservations")
@login_required
def mes_reservations():

    bookings = Booking.query.filter_by(user_id=current_user.id).all()

    return render_template("mes_reservations.html", bookings=bookings)


# Annuler réservation (USER)
@booking_bp.route("/annuler/<int:booking_id>")
@login_required
def annuler(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id:
        abort(403)

    if booking.statut == "PAID":
        return "Impossible d'annuler une réservation déjà payée."

    booking.statut = "CANCELLED"
    db.session.commit()

    return redirect(url_for("booking.mes_reservations"))


# Admin dashboard
@booking_bp.route("/admin")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        abort(403)

    users = User.query.all()
    events = Event.query.all()
    bookings = Booking.query.all()

    return render_template("admin_dashboard.html", users=users,
        events=events, bookings=bookings
                           
    )


# Confirmer
@booking_bp.route("/confirmer/<int:booking_id>")
@login_required
def confirmer(booking_id):

    if current_user.role != "admin":
        abort(403)

    booking = Booking.query.get_or_404(booking_id)
    booking.statut = "CONFIRMED"

    db.session.commit()

    return redirect(url_for("booking.admin_dashboard"))


# Refuser
@booking_bp.route("/refuser/<int:booking_id>")
@login_required
def refuser(booking_id):

    if current_user.role != "admin":
        abort(403)

    booking = Booking.query.get_or_404(booking_id)
    booking.statut = "CANCELLED"

    db.session.commit()

    return redirect(url_for("booking.admin_dashboard"))