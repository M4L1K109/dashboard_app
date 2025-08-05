from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # admin or user
    can_upload = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com arquivos
    uploaded_files = db.relationship('File', backref='uploader', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Define a senha do usuário com hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Verifica se o usuário é admin"""
        return self.role == 'admin'

    def can_manage_files(self):
        """Verifica se o usuário pode gerenciar arquivos"""
        return self.role == 'admin' or self.can_upload

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'can_upload': self.can_upload,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # video, document, pdf
    file_path = db.Column(db.String(500), nullable=False)
    display_time = db.Column(db.Integer, default=10, nullable=False)  # segundos
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    upload_order = db.Column(db.Integer, default=0, nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<File {self.original_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_name': self.original_name,
            'file_type': self.file_type,
            'file_path': self.file_path,
            'display_time': self.display_time,
            'is_active': self.is_active,
            'upload_order': self.upload_order,
            'uploaded_by': self.uploaded_by,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'uploader_name': self.uploader.username if self.uploader else None
        }


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Settings {self.key}>'

    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description
        }

