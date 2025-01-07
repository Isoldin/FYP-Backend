from models import Users
from dependencies import bcrypt_context
from database import SessionLocal

session = SessionLocal()

def create_admin():
    create_admin_model = Users(
        username="admin",
        hashed_password=bcrypt_context.hash("admin123"),
        role="admin"
    )
    session.add(create_admin_model)
    session.commit()

def delete_admin():
    session.query(Users).filter_by(username="admin").delete()
    session.commit()