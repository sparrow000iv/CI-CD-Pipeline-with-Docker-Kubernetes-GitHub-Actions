"""
Unit Tests for Product Service
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app', 'service2'))
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
    assert data['service'] == 'product-service'


def test_get_products_empty(client):
    response = client.get('/api/v1/products')
    assert response.status_code == 200
    data = response.get_json()
    assert 'products' in data


def test_create_product(client):
    response = client.post('/api/v1/products', json={
        'name': 'Test Product',
        'price': 29.99,
        'category': 'electronics'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test Product'
    assert data['price'] == 29.99


def test_create_product_missing_fields(client):
    response = client.post('/api/v1/products', json={})
    assert response.status_code == 400


def test_get_product_not_found(client):
    response = client.get('/api/v1/products/999')
    assert response.status_code == 404


def test_filter_by_category(client):
    # Create products in different categories
    client.post('/api/v1/products', json={'name': 'Laptop', 'price': 999, 'category': 'electronics'})
    client.post('/api/v1/products', json={'name': 'Shirt', 'price': 29, 'category': 'clothing'})

    response = client.get('/api/v1/products?category=electronics')
    assert response.status_code == 200
