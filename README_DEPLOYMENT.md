# PowerPoint Generator - Deployment Guide

## 🚀 Application Overview

A Flask-based web application that generates 3D-enhanced PowerPoint presentations about "The Chemistry Behind Air Purification in Air Conditioning Units (AUC)".

## 📋 Features

- **Web Interface**: Beautiful, responsive UI for generating presentations
- **REST API**: RESTful endpoints for programmatic access
- **3D Presentations**: Generates professional PowerPoint files with:
  - 6 slides with 3D effects
  - Futuristic dark theme
  - 3D molecule representations
  - Chemistry diagrams and reactions
  - Visual flowcharts

## 🛠️ Technology Stack

- **Backend**: Python 3.9+ with Flask
- **Presentation Generation**: python-pptx
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup Steps

1. **Install Dependencies**
```bash
pip install Flask python-pptx Pillow
```

2. **Run the Application**
```bash
python3 app.py
```

The server will start on `http://0.0.0.0:5000`

## 🌐 API Endpoints

### Health Check
```bash
GET /health
```
Returns server health status

### API Information
```bash
GET /api/info
```
Returns API documentation and available endpoints

### Generate Presentation
```bash
POST /api/generate
```
Generates a new PowerPoint presentation

**Response:**
```json
{
  "success": true,
  "message": "Presentation generated successfully!",
  "filename": "Air_Purification_Chemistry_3D_20251113_020245.pptx",
  "size": "35.53 KB",
  "download_url": "/api/download/Air_Purification_Chemistry_3D_20251113_020245.pptx"
}
```

### Download Generated File
```bash
GET /api/download/<filename>
```
Downloads a specific generated presentation

### Download Pre-generated File
```bash
GET /api/download-existing
```
Downloads the pre-generated presentation file

## 🖥️ Web Interface

Access the web interface at `http://localhost:5000/`

Features:
- Generate new presentations with one click
- Download existing presentations
- View API documentation
- Responsive design for mobile and desktop

## 🐳 Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Create `requirements.txt`:
```
Flask==3.1.2
python-pptx==1.0.2
Pillow==11.3.0
```

Build and run:
```bash
docker build -t ppt-generator .
docker run -p 5000:5000 ppt-generator
```

## ☁️ Cloud Deployment Options

### 1. Heroku
```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### 2. AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init -p python-3.9 ppt-generator
eb create ppt-generator-env
eb deploy
```

### 3. Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/ppt-generator
gcloud run deploy --image gcr.io/PROJECT-ID/ppt-generator --platform managed
```

### 4. DigitalOcean App Platform
- Connect your GitHub repository
- Select Python as the runtime
- Set build command: `pip install -r requirements.txt`
- Set run command: `python app.py`

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Set custom port
export FLASK_PORT=8080

# Optional: Set Flask environment
export FLASK_ENV=production
```

### Production Settings

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Update `Procfile` for Heroku:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

## 📊 Project Structure

```
/vercel/sandbox/
├── app.py                          # Flask application
├── create_3d_ppt.py               # PowerPoint generation logic
├── templates/
│   └── index.html                 # Web interface
├── Air_Purification_Chemistry_3D.pptx  # Pre-generated presentation
├── requirements.txt               # Python dependencies
└── README_DEPLOYMENT.md          # This file
```

## 🧪 Testing

### Test Endpoints with curl

```bash
# Health check
curl http://localhost:5000/health

# API info
curl http://localhost:5000/api/info

# Generate presentation
curl -X POST http://localhost:5000/api/generate

# Download existing
curl -O http://localhost:5000/api/download-existing
```

### Test with Python

```python
import requests

# Generate presentation
response = requests.post('http://localhost:5000/api/generate')
data = response.json()
print(data)

# Download file
if data['success']:
    download_url = f"http://localhost:5000{data['download_url']}"
    file_response = requests.get(download_url)
    
    with open('presentation.pptx', 'wb') as f:
        f.write(file_response.content)
```

## 🔒 Security Considerations

1. **Production Mode**: Disable Flask debug mode in production
2. **HTTPS**: Use HTTPS in production environments
3. **Rate Limiting**: Consider adding rate limiting for API endpoints
4. **File Cleanup**: Implement periodic cleanup of generated files in `/tmp/presentations/`

## 📝 Presentation Content

The generated presentation includes:

1. **Slide 1**: Title with 3D floating molecules
2. **Slide 2**: 3D flowchart of air purification process
3. **Slide 3**: 3D representations of common pollutants
4. **Slide 4**: 3D filter models and methods
5. **Slide 5**: Advanced chemistry with 3D reactions
6. **Slide 6**: Summary with 3D globe visualization

## 🎨 Customization

To customize the presentation, edit `create_3d_ppt.py`:

- Modify colors in the color scheme section
- Add/remove slides
- Change text content
- Adjust 3D effects and shapes

## 📞 Support

For issues or questions:
- Check the logs: `cat /vercel/sandbox/.blackbox/tmp/shell_tool_*.log`
- Review Flask output for errors
- Ensure all dependencies are installed

## 📄 License

See LICENSE file in the project root.

## 🎯 Quick Start Summary

```bash
# 1. Install dependencies
pip install Flask python-pptx Pillow

# 2. Run the application
python3 app.py

# 3. Open browser
# Navigate to http://localhost:5000

# 4. Generate presentation
# Click "Generate New Presentation" button
```

## ✅ Deployment Checklist

- [ ] Install Python 3.9+
- [ ] Install dependencies
- [ ] Test locally
- [ ] Configure environment variables
- [ ] Set up production WSGI server (Gunicorn)
- [ ] Configure reverse proxy (Nginx/Apache)
- [ ] Enable HTTPS
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Test all endpoints

---

**Status**: ✅ Application is running and tested successfully!

**Server**: http://0.0.0.0:5000

**Generated Files**: `/tmp/presentations/`
