#!/usr/bin/env python3
"""
Flask Web Application for PowerPoint Generation
Deploys the 3D Air Purification Chemistry Presentation Generator
"""

from flask import Flask, render_template, send_file, jsonify, request
import os
import sys
from datetime import datetime
from create_3d_ppt import create_presentation

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = '/tmp/presentations'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_presentation():
    """Generate a new PowerPoint presentation"""
    try:
        # Generate the presentation
        prs = create_presentation()
        
        # Save to temporary file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Air_Purification_Chemistry_3D_{timestamp}.pptx"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        prs.save(filepath)
        
        file_size = os.path.getsize(filepath)
        
        return jsonify({
            'success': True,
            'message': 'Presentation generated successfully!',
            'filename': filename,
            'size': f"{file_size / 1024:.2f} KB",
            'download_url': f'/api/download/{filename}'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download a generated presentation"""
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download-existing')
def download_existing():
    """Download the pre-generated presentation"""
    try:
        filepath = '/vercel/sandbox/Air_Purification_Chemistry_3D.pptx'
        
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'Pre-generated file not found'
            }), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name='Air_Purification_Chemistry_3D.pptx',
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/info')
def info():
    """Get application information"""
    return jsonify({
        'name': 'PowerPoint Generator API',
        'version': '1.0.0',
        'description': 'Generate 3D-enhanced PowerPoint presentations about Air Purification Chemistry',
        'endpoints': {
            'GET /': 'Web interface',
            'POST /api/generate': 'Generate new presentation',
            'GET /api/download/<filename>': 'Download generated presentation',
            'GET /api/download-existing': 'Download pre-generated presentation',
            'GET /api/info': 'API information'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting PowerPoint Generator Web Application...")
    print("📊 Topic: Chemistry Behind Air Purification in AUC")
    print("🌐 Server will be available at: http://0.0.0.0:5000")
    print()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
