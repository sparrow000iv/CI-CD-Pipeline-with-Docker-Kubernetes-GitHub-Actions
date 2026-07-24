"""
User Service - Flask Microservice
Handles user authentication, registration, and profile management.

Author: Tushar Kumar
"""

from flask import Flask, jsonify, request
from datetime import datetime
import os
import socket

app = Flask(__name__)

# In-memory database (replace with actual DB in production)
users_db = {}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes probes"""
    return jsonify({
        'status': 'healthy',
        'service': 'user-service',
        'timestamp': datetime.utcnow().isoformat(),
        'hostname': socket.gethostname()
    }), 200


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify({
        'users': list(users_db.values()),
        'count': len(users_db)
    }), 200


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': 'username and email are required'}), 400

    user_id = str(len(users_db) + 1)
    user = {
        'id': user_id,
        'username': data['username'],
        'email': data['email'],
        'created_at': datetime.utcnow().isoformat()
    }
    users_db[user_id] = user

    return jsonify(user), 201


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = users_db.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200


@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if data.get('username'):
        users_db[user_id]['username'] = data['username']
    if data.get('email'):
        users_db[user_id]['email'] = data['email']
    users_db[user_id]['updated_at'] = datetime.utcnow().isoformat()

    return jsonify(users_db[user_id]), 200


@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404

    deleted_user = users_db.pop(user_id)
    return jsonify({'message': 'User deleted', 'user': deleted_user}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
