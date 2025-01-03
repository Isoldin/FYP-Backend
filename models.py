from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, JSON, DateTime
from database import Base
from datetime import datetime, timezone

class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)

# class UploadedImages(Base):
#     __tablename__ = 'uploaded_images'
#     image_id = Column(Integer, primary_key=True)
#     image_path = Column(String, nullable=False)
#     geolocation = Column(JSON, nullable=False)
#     type_of_disaster = Column(String, nullable=False)
#     uploaded_by = Column(String, ForeignKey('users.user_id'))
#     uploaded_date = Column(DateTime, default=datetime.now(timezone.utc))