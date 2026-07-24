"""
Unit Tests for User Service
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app', 'service1'))
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'user-service'


def test_get_users_empty(client):
    response = client.get('/api/v1/users')
    assert response.status_code == 200
    data = response.get_json()
    assert 'users' in data
    assert 'count' in data


def test_create_user(client):
    response = client.post('/api/v1/users', json={
        'username': 'testuser',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'
    assert 'id' in data


def test_create_user_missing_fields(client):
    response = client.post('/api/v1/users', json={})
    assert response.status_code == 400


def test_get_user_not_found(client):
    response = client.get('/api/v1/users/999')
    assert response.status_code == 404
