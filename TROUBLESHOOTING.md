# 🔧 Troubleshooting Guide - Smart Farmer System

## 🚨 Common Issues and Solutions

---

## Backend Issues

### Issue 1: "ModuleNotFoundError: No module named 'flask'"

**Cause**: Dependencies not installed or virtual environment not activated

**Solution**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### Issue 2: "FileNotFoundError: maharashtra_smart_farmer_dataset.xlsx"

**Cause**: Dataset file not in correct location

**Solution**:
1. Ensure `maharashtra_smart_farmer_dataset.xlsx` is in project root
2. Check file name spelling (case-sensitive on some systems)
3. Verify path in `config.py`:
```python
DATASET_PATH = os.path.join(BASE_DIR, '..', 'maharashtra_smart_farmer_dataset.xlsx')
```

---

### Issue 3: "Models not found" when starting Flask

**Cause**: ML models not trained yet

**Solution**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python train_models.py
```

Wait 5-10 minutes for training to complete.

---

### Issue 4: "Port 5000 is already in use"

**Cause**: Another application using port 5000

**Solution 1** - Stop conflicting application:
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Solution 2** - Change port in `config.py`:
```python
PORT = 5001  # Use any available port
```

Then update frontend `vite.config.js`:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:5001',  // Match new port
    ...
  }
}
```

---

### Issue 5: "Permission denied" when running scripts

**Cause**: PowerShell execution policy restriction

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try again:
```powershell
.\venv\Scripts\Activate.ps1
```

---

### Issue 6: Training takes too long or crashes

**Cause**: Insufficient RAM or large dataset

**Solution**:
1. Close other applications to free RAM
2. Reduce GridSearchCV parameters in `train_models.py`:
```python
param_grid = {
    'n_estimators': [100],  # Reduce from [100, 200]
    'max_depth': [15],      # Reduce options
}
```
3. Use simpler model temporarily

---

### Issue 7: "ValueError: Unknown label type"

**Cause**: Encoding issues with categorical data

**Solution**:
1. Check dataset for empty values
2. Verify column names match exactly
3. Re-run training:
```powershell
python train_models.py
```

---

## Frontend Issues

### Issue 8: "npm: command not found"

**Cause**: Node.js not installed or not in PATH

**Solution**:
1. Install Node.js from https://nodejs.org (LTS version)
2. Restart terminal after installation
3. Verify: `node --version` and `npm --version`

---

### Issue 9: "Module not found" errors during npm install

**Cause**: Corrupted node_modules or cache

**Solution**:
```powershell
cd frontend
rm -rf node_modules
rm package-lock.json
npm cache clean --force
npm install
```

---

### Issue 10: Frontend shows "Offline" status

**Cause**: Backend not running or CORS issue

**Solution**:
1. Verify backend is running:
   - Open http://localhost:5000/health in browser
   - Should return JSON with status "healthy"

2. Check console errors (F12 in browser)

3. Verify proxy in `vite.config.js`:
```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
    }
  }
}
```

4. Check CORS in backend `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

---

### Issue 11: "Port 3000 already in use"

**Cause**: Another app using port 3000

**Solution 1** - Kill process:
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Solution 2** - Use different port:
```powershell
npm run dev -- --port 3001
```

---

### Issue 12: Charts not displaying

**Cause**: Chart.js not properly imported

**Solution**:
1. Reinstall dependencies:
```powershell
npm install chart.js react-chartjs-2
```

2. Verify imports in component files:
```javascript
import { Chart as ChartJS, ... } from 'chart.js';
ChartJS.register(...);
```

---

### Issue 13: Material-UI components look broken

**Cause**: MUI packages not installed correctly

**Solution**:
```powershell
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material
```

---

### Issue 14: "Network Error" when making API calls

**Cause**: Backend not running or wrong URL

**Solution**:
1. Check backend is running on port 5000
2. Verify API URL in `src/services/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

3. Test API directly in browser:
```
http://localhost:5000/dropdown-data
```

4. Check browser console for CORS errors

---

## Data Issues

### Issue 15: Predictions seem inaccurate

**Cause**: Models need retraining or data quality issues

**Solution**:
1. Check dataset integrity:
   - No missing values
   - Correct data types
   - Consistent formatting

2. Retrain models:
```powershell
cd backend
python train_models.py
```

3. Verify model accuracy metrics in training output

---

### Issue 16: "KeyError" when accessing data

**Cause**: Column name mismatch

**Solution**:
1. Verify dataset columns match expected names:
   - District
   - Soil_Type
   - Crop_Name
   - Weather
   - etc.

2. Check case sensitivity (e.g., "District" not "district")

---

## Performance Issues

### Issue 17: API responses are slow

**Cause**: Large dataset or inefficient queries

**Solution**:
1. Check backend logs for bottlenecks
2. Consider caching frequently accessed data
3. Optimize model loading (load once at startup)
4. Use production WSGI server (Gunicorn) instead of Flask dev server

---

### Issue 18: Frontend loads slowly

**Cause**: Large bundle size or unoptimized assets

**Solution**:
1. Build for production:
```powershell
npm run build
```

2. Serve optimized build:
```powershell
npm run preview
```

3. Lazy load heavy components
4. Optimize images and assets

---

## Database/Model Issues

### Issue 19: "Pickle load error"

**Cause**: Model files corrupted or version mismatch

**Solution**:
1. Delete all .pkl files in `backend/models/`
2. Retrain models:
```powershell
python train_models.py
```

3. Ensure scikit-learn version matches:
```powershell
pip install scikit-learn==1.3.2
```

---

### Issue 20: "Shape mismatch" errors

**Cause**: Input feature mismatch with trained model

**Solution**:
1. Check input feature order matches training
2. Verify all encoders are loaded correctly
3. Retrain models if feature engineering changed

---

## Environment Issues

### Issue 21: Different results on different machines

**Cause**: Different package versions

**Solution**:
1. Use exact versions from requirements.txt:
```powershell
pip install -r requirements.txt --upgrade
```

2. Use virtual environment to isolate dependencies

3. Document Python version used

---

### Issue 22: ".env file not found" warnings

**Cause**: Environment file not created

**Solution**:
1. Copy example file:
```powershell
copy .env.example .env
```

2. Edit .env with your settings
3. Not critical for development (has defaults)

---

## Windows-Specific Issues

### Issue 23: "Access denied" errors

**Cause**: Administrator privileges required

**Solution**:
- Run PowerShell as Administrator
- Or install packages with `--user` flag:
```powershell
pip install --user -r requirements.txt
```

---

### Issue 24: Long path errors

**Cause**: Windows MAX_PATH limitation

**Solution**:
1. Enable long paths in Windows:
   - Run as Admin: `gpedit.msc`
   - Navigate to: Computer Configuration > Administrative Templates > System > Filesystem
   - Enable "Enable Win32 long paths"

2. Or move project closer to root:
```
C:\SmartFarmer\
```

---

## Browser Issues

### Issue 25: API calls blocked by browser

**Cause**: CORS policy or HTTPS/HTTP mixed content

**Solution**:
1. Use same protocol (both HTTP in development)
2. Check browser console for specific error
3. Disable browser extensions temporarily
4. Try different browser (Chrome, Firefox, Edge)

---

### Issue 26: Charts/UI not responsive

**Cause**: Browser zoom or responsive design issues

**Solution**:
1. Reset browser zoom to 100%
2. Clear browser cache (Ctrl + Shift + Delete)
3. Try responsive design mode (F12 > Toggle device toolbar)

---

## Debugging Tips

### Enable Debug Mode

**Backend**:
```python
# In config.py
DEBUG = True
```

**Frontend**:
```javascript
// Check console.log statements
// Use React DevTools
```

### Check Logs

**Backend logs**:
- Look at terminal where Flask is running
- Check for error traces and stack traces

**Frontend logs**:
- Open browser DevTools (F12)
- Check Console tab for errors
- Check Network tab for failed API calls

### Test API Directly

Use browser or cURL:
```bash
# Test health
curl http://localhost:5000/health

# Test with data
curl -X POST http://localhost:5000/recommend-crop \
  -H "Content-Type: application/json" \
  -d '{"District":"Pune","Soil_Type":"Black","Weather":"Monsoon"}'
```

---

## Still Having Issues?

### Checklist
- [ ] Virtual environment activated (backend)
- [ ] All dependencies installed (pip install -r requirements.txt)
- [ ] Models trained (python train_models.py)
- [ ] Dataset file in correct location
- [ ] Node modules installed (npm install)
- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Browser console checked for errors
- [ ] Firewall not blocking ports

### Clean Reinstall

**Backend**:
```powershell
cd backend
rm -rf venv
rm -rf models
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train_models.py
python app.py
```

**Frontend**:
```powershell
cd frontend
rm -rf node_modules
rm package-lock.json
npm install
npm run dev
```

### Get Help

1. Check error message carefully
2. Search error in documentation
3. Review SETUP_GUIDE.md
4. Check API_DOCUMENTATION.md
5. Verify system requirements met

---

## Prevention Tips

1. **Always use virtual environment** for Python
2. **Keep dependencies updated** regularly
3. **Commit working code** before major changes
4. **Test after each change** incrementally
5. **Read error messages** completely
6. **Check documentation** first
7. **Use version control** (Git)

---

## Emergency Reset

If nothing works, complete reset:

```powershell
# 1. Delete everything except source code and dataset
rm -rf backend/venv
rm -rf backend/models
rm -rf frontend/node_modules

# 2. Follow SETUP_GUIDE.md from scratch

# 3. Or use automated scripts:
.\setup_backend.bat
.\setup_frontend.bat
```

---

**Remember**: Most issues are due to:
1. Missing dependencies
2. Wrong directory
3. Port conflicts
4. File path issues
5. Untrained models

Always check these first! 🔍
