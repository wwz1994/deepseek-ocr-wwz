# 🚀 Quick Start Guide

## PowerPoint Generator - Air Purification Chemistry

---

## ⚡ Instant Access

### Web Interface
```
http://localhost:5000
```

### API Base URL
```
http://localhost:5000/api
```

---

## 🎯 One-Line Commands

### Start Server
```bash
python3 app.py
```

### Generate Presentation (API)
```bash
curl -X POST http://localhost:5000/api/generate
```

### Download Existing
```bash
curl -O http://localhost:5000/api/download-existing
```

### Health Check
```bash
curl http://localhost:5000/health
```

---

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/health` | GET | Health check |
| `/api/info` | GET | API documentation |
| `/api/generate` | POST | Generate new presentation |
| `/api/download/<filename>` | GET | Download specific file |
| `/api/download-existing` | GET | Download pre-generated file |

---

## 🎨 What You Get

### 6 Professional Slides
1. **Title** - 3D floating molecules
2. **Process** - Air purification flowchart
3. **Pollutants** - 3D molecule representations
4. **Methods** - Filter technologies
5. **Chemistry** - Advanced reactions
6. **Summary** - Key takeaways

### Features
- ✓ Futuristic dark theme
- ✓ 3D-style graphics
- ✓ Chemistry equations
- ✓ Professional layout
- ✓ ~35 KB file size
- ✓ Ready for animations

---

## 🔧 Installation

```bash
# Install dependencies
pip3 install Flask python-pptx Pillow

# Run application
python3 app.py
```

---

## 📦 Files Created

```
/vercel/sandbox/
├── app.py                    # Flask application
├── create_3d_ppt.py         # PowerPoint generator
├── templates/
│   └── index.html           # Web interface
├── requirements_web.txt     # Dependencies
├── Procfile                 # Heroku config
├── runtime.txt              # Python version
├── deploy.sh                # Deployment script
├── README_DEPLOYMENT.md     # Full documentation
├── DEPLOYMENT_SUCCESS.md    # Deployment report
└── QUICK_START.md          # This file
```

---

## 🌐 Production Deployment

### Heroku
```bash
git init
git add .
git commit -m "Deploy PowerPoint Generator"
heroku create
git push heroku main
```

### Docker
```bash
docker build -t ppt-gen .
docker run -p 5000:5000 ppt-gen
```

### Manual
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## ✅ Current Status

**Server**: ✅ Running on port 5000  
**Health**: ✅ Healthy  
**Endpoints**: ✅ All operational  
**UI**: ✅ Responsive and functional  
**Generation**: ✅ Working perfectly  

---

## 📞 Quick Help

### Server won't start?
```bash
lsof -i :5000  # Check port
kill -9 <PID>  # Kill process
python3 app.py # Restart
```

### Missing dependencies?
```bash
pip3 install -r requirements_web.txt --user
```

### Test everything?
```bash
./deploy.sh
```

---

## 🎉 Success!

Your PowerPoint Generator is **LIVE** and ready to use!

**Access now**: http://localhost:5000

---

*Generated: November 13, 2025*  
*Version: 1.0.0*  
*Status: ✅ OPERATIONAL*
