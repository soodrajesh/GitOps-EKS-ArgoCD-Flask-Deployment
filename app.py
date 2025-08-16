#!/usr/bin/env python3
"""
Simple Flask web application for GitOps demonstration.
This app provides basic endpoints and health checks for Kubernetes deployment.
"""

from flask import Flask, jsonify, render_template_string
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# HTML template for the main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GitOps Demo Application</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px; 
            background-color: #f5f5f5; 
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 8px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
        }
        h1 { 
            color: #333; 
            text-align: center; 
        }
        .info { 
            background: #e7f3ff; 
            padding: 15px; 
            border-radius: 5px; 
            margin: 20px 0; 
        }
        .endpoint { 
            background: #f0f0f0; 
            padding: 10px; 
            margin: 10px 0; 
            border-radius: 3px; 
            font-family: monospace; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 GitOps Demo Application</h1>
        <div class="info">
            <h3>Application Information</h3>
            <p><strong>Version:</strong> {{ version }}</p>
            <p><strong>Environment:</strong> {{ environment }}</p>
            <p><strong>Timestamp:</strong> {{ timestamp }}</p>
            <p><strong>Pod Name:</strong> {{ pod_name }}</p>
        </div>
        
        <h3>Available Endpoints:</h3>
        <div class="endpoint">GET /health - Health check endpoint</div>
        <div class="endpoint">GET /api/info - Application information (JSON)</div>
        <div class="endpoint">GET /api/metrics - Basic metrics (JSON)</div>
        
        <div class="info">
            <p>This application demonstrates a complete GitOps workflow with:</p>
            <ul>
                <li>Automated CI/CD with GitHub Actions</li>
                <li>Container deployment to AWS EKS</li>
                <li>ArgoCD for GitOps deployment</li>
                <li>Terraform for infrastructure provisioning</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Main application page with information about the GitOps demo."""
    return render_template_string(HTML_TEMPLATE,
        version=os.getenv('APP_VERSION', '1.0.0'),
        environment=os.getenv('ENVIRONMENT', 'development'),
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        pod_name=os.getenv('HOSTNAME', 'local')
    )

@app.route('/health')
def health_check():
    """Health check endpoint for Kubernetes liveness and readiness probes."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': os.getenv('APP_VERSION', '1.0.0')
    }), 200

@app.route('/api/info')
def app_info():
    """Application information endpoint."""
    return jsonify({
        'name': 'GitOps Demo Application',
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'pod_name': os.getenv('HOSTNAME', 'local'),
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Main application page'},
            {'path': '/health', 'method': 'GET', 'description': 'Health check'},
            {'path': '/api/info', 'method': 'GET', 'description': 'Application info'},
            {'path': '/api/metrics', 'method': 'GET', 'description': 'Basic metrics'}
        ]
    })

@app.route('/api/metrics')
def metrics():
    """Basic metrics endpoint for monitoring."""
    return jsonify({
        'uptime_seconds': int((datetime.now() - app.start_time).total_seconds()),
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'pod_name': os.getenv('HOSTNAME', 'local'),
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Record start time for uptime metrics
    app.start_time = datetime.now()
    
    # Get configuration from environment variables
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 80))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting GitOps Demo Application on {host}:{port}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Version: {os.getenv('APP_VERSION', '1.0.0')}")
    
    app.run(host=host, port=port, debug=debug)
