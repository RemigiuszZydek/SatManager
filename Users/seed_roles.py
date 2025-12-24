from ..database.database import SessionLocal
from .models import Role

def seed_roles():
    db = SessionLocal()

    roles = [
        Role(name="ADMIN", ),
        Role(name="KOORDYNATOR", ),
        Role(name="MONTER", ),
    ]

    for role in roles:
        exists = db.query(Role).filter(Role.name == role.name).first()
        if not exists:
            db.add(role)

    db.commit()
    db.close()