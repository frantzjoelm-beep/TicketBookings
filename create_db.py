from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Base de données créée avec succès !")

with app.app_context():
    db.create_all()
    print("Tables créées avec succès !")