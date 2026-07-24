"""
Product Service - Flask Microservice
Handles product catalog management.

Author: Tushar Kumar
"""

from flask import Flask, jsonify, request
from datetime import datetime
import os
import socket

app = Flask(__name__)

products_db = {}


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'product-service',
        'timestamp': datetime.utcnow().isoformat(),
        'hostname': socket.gethostname()
    }), 200


@app.route('/api/v1/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    products = list(products_db.values())
    if category:
        products = [p for p in products if p.get('category') == category]
    return jsonify({'products': products, 'count': len(products)}), 200


@app.route('/api/v1/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('price'):
        return jsonify({'error': 'name and price are required'}), 400

    product_id = str(len(products_db) + 1)
    product = {
        'id': product_id,
        'name': data['name'],
        'price': float(data['price']),
        'category': data.get('category', 'general'),
        'stock': data.get('stock', 0),
        'created_at': datetime.utcnow().isoformat()
    }
    products_db[product_id] = product
    return jsonify(product), 201


@app.route('/api/v1/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = products_db.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product), 200


@app.route('/api/v1/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    if product_id not in products_db:
        return jsonify({'error': 'Product not found'}), 404
    deleted = products_db.pop(product_id)
    return jsonify({'message': 'Product deleted', 'product': deleted}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
