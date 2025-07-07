from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tool_name = db.Column(db.String(100))
    sub_tool = db.Column(db.String(100))  # ✅ Add this line
    campaign_name = db.Column(db.String(255))
    message_body = db.Column(db.Text)
    upload_file_id = db.Column(db.Integer, db.ForeignKey('uploaded_file.id'))
    daily_limit = db.Column(db.Integer)
    delay_seconds = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    filename = db.Column(db.String(255))
    filepath = db.Column(db.String(255))
    upload_type = db.Column(db.String(50))  # ✅ Add this line
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    folder_name = db.Column(db.String(150))
