# 🚀 Quick Start Guide - Smart Farmer System

## ⚡ Super Fast Setup (Using Batch Files)

### Option 1: Automated Setup (Easiest)

1. **Setup Backend** (First time only):
   - Double-click `setup_backend.bat`
   - Wait for models to train (5-10 minutes)
   - Models will be saved automatically

2. **Setup Frontend** (First time only):
   - Double-click `setup_frontend.bat`
   - Wait for dependencies to install

3. **Start the System**:
   - Double-click `start_backend.bat` (keep window open)
   - Double-click `start_frontend.bat` (keep window open)
   - Open browser: http://localhost:3000

---

## 🔧 Manual Setup (Full Control)

### Backend Setup

```powershell
# 1. Navigate to backend
cd "d:\Final IoE Project\backend"

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Train models
python train_models.py

# 6. Start server
python app.py
```

### Frontend Setup

```powershell
# 1. Open NEW terminal, navigate to frontend
cd "d:\Final IoE Project\frontend"

# 2. Install dependencies
npm install

# 3. Start dev server
npm run dev
```

---

## 📋 System Requirements

- ✅ Python 3.8+
- ✅ Node.js 16+
- ✅ 2GB RAM minimum
- ✅ 500MB disk space
- ✅ Modern web browser

---

## 🎯 What You'll Get

### Backend (Flask API)
- ✅ 4 trained ML models
- ✅ 9 REST API endpoints
- ✅ 80%+ accuracy on recommendations
- ✅ Runs on http://localhost:5000

### Frontend (React App)
- ✅ 8 interactive pages
- ✅ Beautiful Material-UI design
- ✅ Charts and visualizations
- ✅ Runs on http://localhost:3000

---

## 🧪 Testing the System

### 1. Test Backend API
Open browser: http://localhost:5000/health

Should show:
```json
{
  "status": "healthy",
  "models_loaded": true
}
```

### 2. Test Frontend
Open browser: http://localhost:3000

- Should see green "Connected" chip
- Dashboard shows statistics
- Try Crop Recommendation:
  - District: Pune
  - Soil: Black
  - Weather: Post-Monsoon
  - Click "Get Recommendations"

---

## 📊 Features Overview

### 1. Dashboard
- Quick statistics
- Maharashtra zones
- Direct navigation

### 2. Crop Recommendation
- Select district, soil, weather
- Get top 3 crop suggestions
- View confidence scores

### 3. Nutrient Analysis
- Predict NPK requirements
- View micronutrients
- See deficiency alerts

### 4. Water Quality
- pH analysis
- Turbidity check
- Temperature assessment

### 5. Crop Comparison
- Compare up to 3 crops
- Economic analysis
- Risk assessment

### 6. District Insights
- District-specific data
- Soil distribution charts
- Popular crops

### 7. Weather Planning
- Seasonal recommendations
- Monsoon planning
- Crop calendar

### 8. Economic Analysis
- ROI calculator
- Cost estimation
- Profit analysis

---

## 🔄 Daily Usage

**Start System:**
1. Run `start_backend.bat`
2. Run `start_frontend.bat`
3. Open http://localhost:3000

**Stop System:**
- Press `Ctrl + C` in both terminals
- Or close the windows

---

## ⚠️ Common Issues

### "Models not found"
**Fix**: Run `python train_models.py` or `setup_backend.bat`

### "Port already in use"
**Fix**: Close other applications using port 5000/3000

### "Module not found"
**Fix**: Reinstall dependencies
- Backend: `pip install -r requirements.txt`
- Frontend: `npm install`

### Frontend shows "Offline"
**Fix**: Ensure backend is running on port 5000

---

## 📁 Important Files

```
backend/
├── app.py              # Main Flask server
├── train_models.py     # Train ML models
├── config.py           # Configuration
└── models/             # Trained models (generated)

frontend/
├── src/
│   ├── App.jsx         # Main app
│   ├── pages/          # All pages
│   └── services/api.js # API calls
└── package.json        # Dependencies
```

---

## 🎓 Learning Path

1. **Start**: Use the system through UI
2. **Explore**: Check API responses in browser console (F12)
3. **Understand**: Read `app.py` for backend logic
4. **Customize**: Modify `config.py` for your needs
5. **Extend**: Add new features to pages

---

## 🆘 Need Help?

1. Check `SETUP_GUIDE.md` for detailed instructions
2. Read `README.md` for full documentation
3. Review error messages in terminals
4. Ensure dataset file exists in project root

---

## ✅ Success Checklist

- [ ] Backend setup completed
- [ ] Frontend setup completed
- [ ] Models trained (4 .pkl files in backend/models/)
- [ ] Flask server starts without errors
- [ ] React app loads in browser
- [ ] "Connected" status shows in navbar
- [ ] Crop recommendation works
- [ ] All pages accessible

---

## 🎉 You're Ready!

The system is now set up and ready to help Maharashtra farmers make informed agricultural decisions.

**Enjoy exploring the features!** 🌾

---

## 📞 Quick Commands Reference

```powershell
# Backend
cd backend
.\venv\Scripts\Activate.ps1
python train_models.py     # Train models
python app.py              # Start server

# Frontend
cd frontend
npm install                # Install deps
npm run dev                # Start dev server
npm run build              # Production build
```

---

Built with ❤️ using Python, Flask, React, and Machine Learning
