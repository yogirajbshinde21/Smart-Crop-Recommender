# 🌾 Smart Farmer Recommender System - Maharashtra Edition

A comprehensive AI-powered agricultural decision support system specifically designed for Maharashtra farmers, using machine learning to provide data-driven recommendations for crop selection, nutrient management, and agricultural planning.

## 📊 Project Overview

This system helps Maharashtra farmers make informed decisions about:
- **Crop Selection**: AI-powered recommendations based on district, soil type, and weather
- **Nutrient Management**: Precise NPK and micronutrient predictions
- **Water Quality Analysis**: pH, turbidity, and temperature optimization
- **Economic Planning**: Cost-benefit analysis and ROI calculations
- **Crop Comparison**: Side-by-side analysis of multiple crops
- **District Insights**: Comprehensive agricultural data for all 36 Maharashtra districts

## 🎯 Key Features

### Backend (Flask + ML)
- **4 Machine Learning Models**:
  - Crop Recommendation (Random Forest Classifier)
  - Nutrient Prediction (MLP Neural Network)
  - Water Quality Prediction (Random Forest Regressor)
  - Fertilizer Recommendation (Random Forest Classifier)
- **Model Performance**:
  - Crop Recommendation Accuracy: >80%
  - Nutrient Prediction R² Score: >0.75
  - Comprehensive API with 9 endpoints

### Frontend (React + Vite)
- **8 Main Pages**:
  - Dashboard with statistics
  - Crop Recommendation
  - Nutrient Analysis
  - Water Quality Assessment
  - Crop Comparison
  - District Insights
  - Weather Planning
  - Economic Analysis
- **Modern UI/UX**: Material-UI components, responsive design
- **Data Visualization**: Charts.js for interactive visualizations

## 📁 Project Structure

```
Final IoE Project/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── train_models.py        # ML model training
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── models/                # Trained ML models (generated)
│   └── data/                  # Data directory
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   ├── context/           # React context
│   │   └── utils/             # Utility functions
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
└── maharashtra_smart_farmer_dataset.xlsx  # Training dataset
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd "d:\Final IoE Project\backend"
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Train ML models** (first time only):
```bash
python train_models.py
```
This will:
- Load the Maharashtra farmer dataset
- Train 4 ML models
- Save models to `models/` directory
- Takes approximately 5-10 minutes

5. **Run Flask server**:
```bash
python app.py
```
Server will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd "d:\Final IoE Project\frontend"
```

2. **Install dependencies**:
```bash
npm install
```

3. **Run development server**:
```bash
npm run dev
```
Frontend will start on `http://localhost:3000`

## 🔧 API Endpoints

### GET Endpoints
- `GET /health` - Health check
- `GET /dropdown-data` - Get all dropdown options
- `GET /district-insights/<district>` - District-specific insights
- `GET /statistics` - Overall system statistics

### POST Endpoints
- `POST /recommend-crop` - Get top 3 crop recommendations
- `POST /predict-nutrients` - Predict nutrient requirements
- `POST /water-quality-analysis` - Analyze water quality
- `POST /fertilizer-recommendation` - Recommend fertilizers
- `POST /compare-crops` - Compare multiple crops

## 📊 Dataset Information

- **Total Records**: 1,800 rows
- **Districts**: All 36 Maharashtra districts
- **Crops**: 19 major crop varieties
- **Soil Types**: 7 types (Black, Clay, Red, Laterite, Alluvial, Sandy, Loamy)
- **Weather Conditions**: 10 types
- **Columns**: 13 (District, Soil_Type, Crop_Name, N, P, K, Zn, S, pH, Turbidity, Temperature, Weather, Fertilizer)

## 🗺️ Maharashtra Agricultural Zones

1. **Konkan** (6 districts): Coastal, high rainfall, rice & coconut
2. **Vidarbha** (11 districts): Cotton belt, soybean
3. **Marathwada** (8 districts): Drought-prone, pulses & sorghum
4. **Western Maharashtra** (5 districts): Sugarcane & grapes
5. **North Maharashtra** (5 districts): Cotton & wheat

## 💡 Usage Examples

### Crop Recommendation
```python
POST /recommend-crop
{
  "District": "Pune",
  "Soil_Type": "Black",
  "Weather": "Post-Monsoon"
}
```

### Nutrient Prediction
```python
POST /predict-nutrients
{
  "District": "Nashik",
  "Soil_Type": "Red",
  "Crop_Name": "Grapes",
  "Weather": "Winter"
}
```

### Crop Comparison
```python
POST /compare-crops
{
  "crops": ["Cotton", "Soybean", "Wheat"],
  "District": "Nagpur",
  "Soil_Type": "Black",
  "Weather": "Monsoon"
}
```

## 🎨 Frontend Features

### Dashboard
- Quick statistics overview
- Maharashtra zone information
- Feature cards with direct navigation

### Crop Recommendation
- Interactive form with dropdowns
- Top 3 crop cards with confidence scores
- Zone-specific insights
- Market rate and yield information

### Nutrient Analysis
- Multi-step input form
- Detailed nutrient breakdown
- Radar chart visualization
- NPK ratio display
- Deficiency alerts

### Crop Comparison
- Select up to 3 crops
- Side-by-side economic comparison
- ROI calculation
- Risk assessment
- Nutrient requirement comparison

### District Insights
- District-specific statistics
- Soil type distribution (Pie chart)
- Popular crops (Bar chart)
- Average nutrient requirements
- Water quality parameters

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0
- **ML Libraries**: scikit-learn, pandas, numpy
- **Models**: Random Forest, MLP Neural Network
- **Data Processing**: openpyxl, joblib

### Frontend
- **Framework**: React 18 + Vite
- **UI Library**: Material-UI (MUI)
- **Charts**: Chart.js, Recharts
- **HTTP Client**: Axios
- **Routing**: React Router

## 📈 Model Details

### Crop Recommendation Model
- **Algorithm**: Random Forest Classifier
- **Features**: District, Soil_Type, Weather, Zone
- **Output**: Top 3 crops with confidence scores
- **Accuracy**: >80%

### Nutrient Prediction Model
- **Algorithm**: MLP Neural Network
- **Architecture**: 128-64-32 hidden layers
- **Features**: District, Soil_Type, Crop_Name, Weather, Zone
- **Outputs**: N, P2O5, K2O, Zn, S (kg/ha)
- **R² Score**: >0.75

### Water Quality Predictor
- **Algorithm**: Random Forest Regressor
- **Features**: District, Weather, Soil_Type, Zone
- **Outputs**: pH, Turbidity, Temperature

### Fertilizer Recommender
- **Algorithm**: Random Forest Classifier
- **Features**: Crop_Name, Soil_Type, N, P, K requirements
- **Output**: Optimal fertilizer type

## 🔍 Advanced Features

- **Regional Risk Assessment**: Climate suitability analysis
- **Economic Viability**: Cost-benefit with Maharashtra market rates
- **Sustainability Index**: Environmental impact scoring
- **Resource Efficiency**: Water and nutrient optimization
- **Seasonal Planning**: Weather-based crop scheduling

## 📝 Development Notes

### Training Models
- Models are trained on first run using `train_models.py`
- Training takes 5-10 minutes
- Models are saved in `backend/models/` directory
- Retraining updates all models

### Encoders and Scalers
- Label encoders for categorical features
- Standard scalers for numerical features
- Saved alongside models for consistent predictions

### API Configuration
- Default port: 5000 (backend), 3000 (frontend)
- CORS enabled for cross-origin requests
- Configurable in `config.py` and `vite.config.js`

## 🚨 Troubleshooting

### Backend Issues
- **Models not found**: Run `python train_models.py`
- **Dataset not found**: Ensure `maharashtra_smart_farmer_dataset.xlsx` is in project root
- **Port already in use**: Change PORT in `config.py`

### Frontend Issues
- **API connection error**: Ensure Flask server is running on port 5000
- **Module not found**: Run `npm install`
- **Port conflict**: Change port in `vite.config.js`

## 📊 Success Metrics

- ✅ District-specific crop recommendation accuracy >80%
- ✅ Nutrient prediction R² score >0.75
- ✅ All 36 Maharashtra districts covered
- ✅ 19 major crops supported
- ✅ 4 trained ML models
- ✅ 8 functional frontend pages
- ✅ 9 API endpoints

## 🎯 Future Enhancements

- [ ] Multi-language support (Marathi, Hindi)
- [ ] Real-time weather API integration
- [ ] Mobile app development
- [ ] PDF report generation
- [ ] User authentication
- [ ] Farmer dashboard with history
- [ ] SMS/WhatsApp alerts
- [ ] Market price integration
- [ ] Pest and disease prediction
- [ ] Satellite imagery analysis

## 👨‍💻 Author

Created with ❤️ for Maharashtra farmers

## 📄 License

This project is for educational and agricultural development purposes.

## 🙏 Acknowledgments

- Maharashtra Agricultural Department
- Farmers of Maharashtra
- Open-source ML community

---

**Note**: This system provides recommendations based on historical data and ML models. Always consult with local agricultural experts for final decisions.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Ensure all dependencies are installed
4. Verify dataset is in correct location

---

**Built with Python, Flask, React, and Machine Learning** 🚀
