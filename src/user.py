from flask import Blueprint, jsonify, request, session
from src.models.user import User, db
from src.routes.auth import require_admin, require_login

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@require_admin
def get_users():
    """Lista todos os usuários (apenas admin)"""
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@require_login
def get_user(user_id):
    """Obtém dados de um usuário específico"""
    try:
        # Usuários podem ver apenas seus próprios dados, admin pode ver todos
        current_user = User.query.get(session['user_id'])
        if not current_user.is_admin() and current_user.id != user_id:
            return jsonify({'error': 'Acesso negado'}), 403
        
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@require_admin
def update_user(user_id):
    """Atualiza dados de um usuário (apenas admin)"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.json
        
        # Atualizar campos permitidos
        if 'username' in data:
            # Verificar se o username já existe
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({'error': 'Username já existe'}), 400
            user.username = data['username']
        
        if 'role' in data:
            user.role = data['role']
        
        if 'can_upload' in data:
            user.can_upload = data['can_upload']
        
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    """Remove um usuário (apenas admin)"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Não permitir deletar o próprio usuário admin
        current_user = User.query.get(session['user_id'])
        if user.id == current_user.id:
            return jsonify({'error': 'Não é possível deletar seu próprio usuário'}), 400
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuário removido com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>/toggle-upload', methods=['POST'])
@require_admin
def toggle_upload_permission(user_id):
    """Alterna permissão de upload de um usuário"""
    try:
        user = User.query.get_or_404(user_id)
        user.can_upload = not user.can_upload
        db.session.commit()
        
        return jsonify({
            'message': f'Permissão de upload {"ativada" if user.can_upload else "desativada"} para {user.username}',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile', methods=['GET'])
@require_login
def get_profile():
    """Obtém perfil do usuário logado"""
    try:
        user = User.query.get(session['user_id'])
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile', methods=['PUT'])
@require_login
def update_profile():
    """Atualiza perfil do usuário logado"""
    try:
        user = User.query.get(session['user_id'])
        data = request.json
        
        # Usuários podem alterar apenas sua própria senha
        if 'password' in data and data['password']:
            user.set_password(data['password'])
            db.session.commit()
            return jsonify({'message': 'Senha atualizada com sucesso'}), 200
        
        return jsonify({'error': 'Nenhum campo válido para atualização'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

