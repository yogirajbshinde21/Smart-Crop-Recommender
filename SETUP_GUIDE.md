# 🚀 Smart Farmer System - Complete Setup Guide

## 🎯 Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or higher
- ✅ Node.js 16 or higher
- ✅ npm or yarn
- ✅ Git (optional)

Check versions:
```powershell
python --version
node --version
npm --version
```

## 📦 Step-by-Step Setup

### Step 1: Backend Setup

1. Open PowerShell and navigate to the backend folder:
```powershell
cd "d:\Final IoE Project\backend"
```

2. Create a Python virtual environment (recommended):
```powershell
python -m venv venv
```

3. Activate the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```
If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

4. Install Python dependencies:
```powershell
pip install -r requirements.txt
```

5. Train the ML models (this takes 5-10 minutes):
```powershell
python train_models.py
```

You should see output like:
```
Loading dataset...
Training Crop Recommendation Model...
✓ Crop Recommendation Model Accuracy: 85.23%
Training Nutrient Prediction Model...
✓ Nutrient Prediction Model R² Score: 0.8124
...
All models saved!
```

6. Start the Flask server:
```powershell
python app.py
```

Server will start on http://localhost:5000

**Keep this terminal open!**

---

### Step 2: Frontend Setup

1. Open a NEW PowerShell window and navigate to the frontend folder:
```powershell
cd "d:\Final IoE Project\frontend"
```

2. Install Node.js dependencies:
```powershell
npm install
```

This will install all required packages (React, Material-UI, Chart.js, etc.)

3. Start the development server:
```powershell
npm run dev
```

Frontend will start on http://localhost:3000

4. Open your browser and visit:
```
http://localhost:3000
```

---

## ✅ Verification Steps

### Test Backend API

1. Open a browser or use curl to test:
```
http://localhost:5000/health
```

You should see:
```json
{
  "status": "healthy",
  "message": "Smart Farmer API is running",
  "models_loaded": true
}
```

2. Test dropdown data:
```
http://localhost:5000/dropdown-data
```

### Test Frontend

1. Visit http://localhost:3000
2. You should see the Dashboard with:
   - Green "Connected" chip (if backend is running)
   - Statistics cards showing 36 districts, 19 crops, etc.
   - Maharashtra zone cards
   - Feature cards

3. Test Crop Recommendation:
   - Click "Crop Recommendation" in the navbar
   - Select: District (e.g., Pune), Soil Type (e.g., Black), Weather (e.g., Post-Monsoon)
   - Click "Get Recommendations"
   - You should see top 3 crop recommendations with confidence scores

---

## 🔧 Common Issues and Solutions

### Issue 1: "Models not found"
**Solution**: Run `python train_models.py` in the backend directory

### Issue 2: "Dataset not found"
**Solution**: Ensure `maharashtra_smart_farmer_dataset.xlsx` is in the project root directory

### Issue 3: "Port 5000 already in use"
**Solution**: 
- Stop any other Flask applications
- Or change the port in `backend/config.py`:
```python
PORT = 5001  # Change to any available port
```

### Issue 4: "CORS error" in browser console
**Solution**: Ensure Flask-CORS is installed and the backend is running

### Issue 5: Frontend shows "Offline"
**Solution**: 
- Check if backend is running on http://localhost:5000
- Test the health endpoint in your browser
- Check firewall settings

### Issue 6: "Module not found" errors
**Backend**: Make sure virtual environment is activated and requirements are installed
**Frontend**: Run `npm install` again

---

## 📁 Project Structure After Setup

```
Final IoE Project/
├── backend/
│   ├── venv/                    # Virtual environment (created)
│   ├── models/                  # Trained models (created)
│   │   ├── crop_recommender.pkl
│   │   ├── nutrient_predictor.pkl
│   │   ├── water_quality_predictor.pkl
│   │   ├── fertilizer_recommender.pkl
│   │   ├── encoders.pkl
│   │   └── scalers.pkl
│   ├── app.py
│   ├── train_models.py
│   ├── config.py
│   └── requirements.txt
├── frontend/
│   ├── node_modules/            # Dependencies (created)
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── maharashtra_smart_farmer_dataset.xlsx
```

---

## 🎮 Using the Application

### Dashboard
- View overall statistics
- Explore Maharashtra agricultural zones
- Quick navigation to features

### Crop Recommendation
1. Select your district
2. Choose soil type
3. Select weather condition
4. Click "Get Recommendations"
5. View top 3 crops with confidence scores, yields, and market rates

### Nutrient Analysis
1. Select district, soil type, crop, and weather
2. Click "Predict Nutrients"
3. View NPK requirements, micronutrients, and radar chart
4. Check for deficiency alerts

### Crop Comparison
1. Select 2-3 crops to compare
2. Enter district, soil type, and weather
3. Click "Compare Crops"
4. View side-by-side economic analysis, nutrients, and risk assessment

### District Insights
1. Select any Maharashtra district
2. View soil distribution, popular crops, and weather patterns
3. See average nutrient requirements and water quality stats
4. Explore charts and visualizations

---

## 🔄 Starting the System (After Initial Setup)

Every time you want to use the system:

1. **Start Backend**:
```powershell
cd "d:\Final IoE Project\backend"
.\venv\Scripts\Activate.ps1
python app.py
```

2. **Start Frontend** (in a new terminal):
```powershell
cd "d:\Final IoE Project\frontend"
npm run dev
```

3. Open browser: http://localhost:3000

---

## 🛑 Stopping the System

- Press `Ctrl + C` in both terminal windows
- Close the terminals

---

## 📊 Model Retraining

To retrain models with updated data:

1. Update `maharashtra_smart_farmer_dataset.xlsx`
2. Run:
```powershell
cd "d:\Final IoE Project\backend"
.\venv\Scripts\Activate.ps1
python train_models.py
```
3. Restart the Flask server

---

## 🎓 Learning the Code

### Backend Key Files
- `app.py` - Flask API endpoints
- `train_models.py` - ML model training
- `config.py` - Configuration and constants

### Frontend Key Files
- `src/App.jsx` - Main app component
- `src/pages/*.jsx` - Page components
- `src/services/api.js` - API client
- `src/context/AppContext.jsx` - Global state

---

## 🆘 Getting Help

1. Check the README.md for detailed documentation
2. Review error messages in the terminal
3. Check browser console (F12) for frontend errors
4. Verify all dependencies are installed
5. Ensure dataset file is in the correct location

---

## 🎉 Success Checklist

- [ ] Python virtual environment created
- [ ] Backend dependencies installed
- [ ] ML models trained successfully
- [ ] Flask server running on port 5000
- [ ] Frontend dependencies installed
- [ ] React app running on port 3000
- [ ] Dashboard loads with statistics
- [ ] API shows "Connected" status
- [ ] Crop recommendation works
- [ ] All pages accessible

---

**Happy Farming! 🌾**

For any issues, check the troubleshooting section or review the error messages carefully.
