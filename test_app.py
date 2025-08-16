#!/usr/bin/env python3
"""
Unit tests for the GitOps demo application.
"""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Test the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'GitOps Demo Application' in response.data


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'version' in data


def test_app_info(client):
    """Test the application info endpoint."""
    response = client.get('/api/info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['name'] == 'GitOps Demo Application'
    assert 'version' in data
    assert 'environment' in data
    assert 'endpoints' in data
    assert len(data['endpoints']) > 0


def test_metrics(client):
    """Test the metrics endpoint."""
    response = client.get('/api/metrics')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'uptime_seconds' in data
    assert 'environment' in data
    assert 'version' in data
    assert 'timestamp' in data


def test_not_found(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['error'] == 'Not found'


def test_health_check_content_type(client):
    """Test that health check returns JSON content type."""
    response = client.get('/health')
    assert response.content_type == 'application/json'


def test_api_endpoints_return_json(client):
    """Test that all API endpoints return JSON."""
    endpoints = ['/api/info', '/api/metrics', '/health']
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.content_type == 'application/json'
        assert response.status_code == 200
