import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db, User, File, Settings
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.files import files_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'dashboard_app_secret_key_2024'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Configuração CORS
CORS(app)

# Configuração de upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(files_bp, url_prefix='/api')

def create_admin_user():
    """Cria o usuário admin padrão se não existir"""
    admin = User.query.filter_by(username='Admin').first()
    if not admin:
        admin = User(
            username='Admin',
            role='admin',
            can_upload=True
        )
        admin.set_password('Admin')
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado: Admin/Admin")

def create_default_settings():
    """Cria configurações padrão"""
    default_settings = [
        ('default_display_time', '10', 'Tempo padrão de exibição em segundos'),
        ('auto_rotation', 'true', 'Rotação automática ativada'),
        ('app_title', 'Dashboard App', 'Título da aplicação')
    ]
    
    for key, value, description in default_settings:
        setting = Settings.query.filter_by(key=key).first()
        if not setting:
            setting = Settings(key=key, value=value, description=description)
            db.session.add(setting)
    
    db.session.commit()

with app.app_context():
    db.create_all()
    create_admin_user()
    create_default_settings()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

