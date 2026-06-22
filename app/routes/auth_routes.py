from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
import bcrypt
from flask_login import login_user
from flask_login import logout_user
from app.models.booking import Booking

from app.models import db
from app.models.user import User
from app.models.event import Event
from datetime import datetime
from app.utils.password import hash_password
from app.utils.password import check_password
from flask import Blueprint


auth_bp = Blueprint("auth", __name__)
booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/payer/<int:booking_id>")
@login_required
def payer(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id:
        abort(403)

    if booking.statut != "CONFIRMED":
        return "Paiement impossible"

    booking.statut = "PAID"
    db.session.commit()

    return redirect(url_for("booking.mes_reservations"))


@auth_bp.route("/admin")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        abort(403)

    users = User.query.all()

    events = Event.query.all()

    bookings = Booking.query.all()

    return render_template(
        "admin_dashboard.html",
        users=users,
        events=events,
        bookings=bookings
    )

@auth_bp.route("/")
def home():

    events = Event.query.all()

    return render_template(
        "home.html",
        events=events
    )

@auth_bp.route("/admin/events")
@login_required
def admin_events():

    if current_user.role != "admin":
        abort(403)

    events = Event.query.all()

    return render_template("dashboard.html", user=current_user, events=events)

@auth_bp.route("/create-event", methods=["GET", "POST"])
@login_required
def create_event():

    if request.method == "POST":

        print(request.form["date"])
        print(type(request.form["date"]))

        titre = request.form["titre"]
        description = request.form["description"]
        categorie = request.form["categorie"]

        capacite = int(request.form["capacite"])

        # CONVERSION OBLIGATOIRE
        date_str = request.form["date"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        event = Event(
            titre=titre,
            date=date_obj,
            description=description,
            capacite=capacite,
            categorie=categorie,
            user_id=current_user.id
        )

        db.session.add(event)
        db.session.commit()

        return redirect(url_for("auth.dashboard"))

    return render_template("create_event.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        nom = request.form.get("nom")
        email = request.form.get("email")
        password = request.form.get("password")

        user_exists = User.query.filter_by(email=email).first()

        if user_exists:
            return "Email déjà utilisé"

        user = User(
            nom=nom,
            email=email,
            password=hash_password(password),
            role="user"
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()


        if user:
            print("Mot de passe stocké :", user.password)

        if user and check_password(password, user.password):

            login_user(user)

            return redirect(url_for("auth.dashboard"))

        return "Email ou mot de passe incorrect"

    return render_template("login.html")

@auth_bp.route("/dashboard")
@login_required
def dashboard():

    events = Event.query.filter_by(
        user_id=current_user.id
    ).all()

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "dashboard.html",
        user=current_user,
        events=events,
        bookings=bookings
    )
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))