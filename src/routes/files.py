import os
import uuid
from flask import Blueprint, request, jsonify, session, send_from_directory, current_app
from werkzeug.utils import secure_filename
from src.models.user import db, File, User
from src.routes.auth import require_upload_permission, require_login

files_bp = Blueprint('files', __name__)

# Extensões permitidas
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi'}
ALLOWED_DOCUMENT_EXTENSIONS = {'xlsx', 'xls', 'csv', 'ods'}
ALLOWED_PDF_EXTENSIONS = {'pdf'}

def allowed_file(filename, file_type):
    """Verifica se o arquivo tem extensão permitida"""
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'video':
        return ext in ALLOWED_VIDEO_EXTENSIONS
    elif file_type == 'document':
        return ext in ALLOWED_DOCUMENT_EXTENSIONS
    elif file_type == 'pdf':
        return ext in ALLOWED_PDF_EXTENSIONS
    
    return False

def get_file_type(filename):
    """Determina o tipo do arquivo baseado na extensão"""
    if '.' not in filename:
        return None
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if ext in ALLOWED_VIDEO_EXTENSIONS:
        return 'video'
    elif ext in ALLOWED_DOCUMENT_EXTENSIONS:
        return 'document'
    elif ext in ALLOWED_PDF_EXTENSIONS:
        return 'pdf'
    
    return None

@files_bp.route('/upload', methods=['POST'])
@require_upload_permission
def upload_file():
    """Upload de arquivo"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Determinar tipo do arquivo
        file_type = get_file_type(file.filename)
        if not file_type:
            return jsonify({'error': 'Tipo de arquivo não suportado'}), 400
        
        if not allowed_file(file.filename, file_type):
            return jsonify({'error': f'Extensão não permitida para {file_type}'}), 400
        
        # Gerar nome único para o arquivo
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Determinar pasta de destino
        if file_type == 'video':
            subfolder = 'videos'
        elif file_type == 'document':
            subfolder = 'documents'
        else:  # pdf
            subfolder = 'pdfs'
        
        # Criar pasta se não existir
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(upload_folder, exist_ok=True)
        
        # Salvar arquivo
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # Obter tempo de exibição do formulário
        display_time = request.form.get('display_time', 10, type=int)
        
        # Obter próxima ordem
        max_order = db.session.query(db.func.max(File.upload_order)).scalar() or 0
        
        # Salvar no banco de dados
        new_file = File(
            filename=unique_filename,
            original_name=original_filename,
            file_type=file_type,
            file_path=file_path,
            display_time=display_time,
            upload_order=max_order + 1,
            uploaded_by=session['user_id']
        )
        
        db.session.add(new_file)
        db.session.commit()
        
        return jsonify({
            'message': 'Arquivo enviado com sucesso',
            'file': new_file.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@files_bp.route('/files', methods=['GET'])
@require_login
def get_files():
    """Lista todos os arquivos"""
    try:
        files = File.query.order_by(File.upload_order.asc()).all()
        return jsonify([file.to_dict() for file in files]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@files_bp.route('/files/active', methods=['GET'])
def get_active_files():
    """Lista arquivos ativos para exibição no dashboard"""
    try:
        files = File.query.filter_by(is_active=True).order_by(File.upload_order.asc()).all()
        return jsonify([file.to_dict() for file in files]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@files_bp.route('/files/<int:file_id>', methods=['GET'])
@require_login
def get_file(file_id):
    """Obtém dados de um arquivo específico"""
    try:
        file = File.query.get_or_404(file_id)
        return jsonify(file.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@files_bp.route('/files/<int:file_id>', methods=['PUT'])
@require_upload_permission
def update_file(file_id):
    """Atualiza dados de um arquivo"""
    try:
        file = File.query.get_or_404(file_id)
        data = request.get_json()
        
        if 'display_time' in data:
            file.display_time = data['display_time']
        
        if 'is_active' in data:
            file.is_active = data['is_active']
        
        if 'upload_order' in data:
            file.upload_order = data['upload_order']
        
        db.session.commit()
        return jsonify(file.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@files_bp.route('/files/<int:file_id>', methods=['DELETE'])
@require_upload_permission
def delete_file(file_id):
    """Remove um arquivo"""
    try:
        file = File.query.get_or_404(file_id)
        
        # Remover arquivo físico
        if os.path.exists(file.file_path):
            os.remove(file.file_path)
        
        # Remover do banco
        db.session.delete(file)
        db.session.commit()
        
        return jsonify({'message': 'Arquivo removido com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@files_bp.route('/files/<int:file_id>/toggle-active', methods=['POST'])
@require_upload_permission
def toggle_file_active(file_id):
    """Ativa/desativa um arquivo"""
    try:
        file = File.query.get_or_404(file_id)
        file.is_active = not file.is_active
        db.session.commit()
        
        return jsonify({
            'message': f'Arquivo {"ativado" if file.is_active else "desativado"} com sucesso',
            'file': file.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@files_bp.route('/files/reorder', methods=['POST'])
@require_upload_permission
def reorder_files():
    """Reordena arquivos"""
    try:
        data = request.get_json()
        file_orders = data.get('file_orders', [])
        
        for item in file_orders:
            file_id = item.get('id')
            new_order = item.get('order')
            
            file = File.query.get(file_id)
            if file:
                file.upload_order = new_order
        
        db.session.commit()
        return jsonify({'message': 'Ordem dos arquivos atualizada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@files_bp.route('/serve/<path:filename>')
def serve_file(filename):
    """Serve arquivos estáticos"""
    try:
        # Procurar o arquivo nas subpastas
        for subfolder in ['videos', 'documents', 'pdfs']:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
            if os.path.exists(os.path.join(file_path, filename)):
                return send_from_directory(file_path, filename)
        
        return jsonify({'error': 'Arquivo não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

