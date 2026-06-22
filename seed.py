from app import create_app
from app.models import db
from app.models.user import User
from app.utils.password import hash_password

app = create_app()

with app.app_context():

    admin = User(
        nom="Admin",
        email="admin@test.com",
        password=hash_password("admin123"),
        role="admin"
    )

    db.session.add(admin)
    db.session.commit()

    print("Admin créé avec succès")