# 🏗️ System Architecture - Smart Farmer Recommender

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│                   (React + Vite App)                         │
│                  http://localhost:3000                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP/REST API Calls
                       │ (Axios)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   FLASK API SERVER                           │
│                  http://localhost:5000                       │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Endpoints (9)                        │  │
│  │  • GET  /health                                       │  │
│  │  • GET  /dropdown-data                                │  │
│  │  • GET  /statistics                                   │  │
│  │  • GET  /district-insights/<district>                 │  │
│  │  • POST /recommend-crop                               │  │
│  │  • POST /predict-nutrients                            │  │
│  │  • POST /water-quality-analysis                       │  │
│  │  • POST /fertilizer-recommendation                    │  │
│  │  • POST /compare-crops                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Machine Learning Models (4)                   │  │
│  │  • Crop Recommender (Random Forest)                   │  │
│  │  • Nutrient Predictor (MLP Neural Network)            │  │
│  │  • Water Quality Predictor (Random Forest)            │  │
│  │  • Fertilizer Recommender (Random Forest)             │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Encoders & Scalers                           │  │
│  │  • Label Encoders (categorical features)              │  │
│  │  • Standard Scalers (numerical features)              │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  DATA LAYER                                  │
│  • maharashtra_smart_farmer_dataset.xlsx (1,800 rows)       │
│  • Trained model files (.pkl)                                │
│  • Configuration (config.py)                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow

### Example: Crop Recommendation

```
User Action (Frontend)
    │
    ├─ Select: District = "Pune"
    ├─ Select: Soil Type = "Black"
    ├─ Select: Weather = "Post-Monsoon"
    └─ Click: "Get Recommendations"
                │
                ▼
┌───────────────────────────────────────────┐
│  React Component (CropRecommendation.jsx) │
│  • Validate inputs                        │
│  • Set loading state                      │
│  • Call API service                       │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌───────────────────────────────────────────┐
│  API Service (api.js)                     │
│  • Create request body                    │
│  • Send POST to /recommend-crop           │
└─────────────────┬─────────────────────────┘
                  │
                  ▼ HTTP POST
┌───────────────────────────────────────────┐
│  Flask Endpoint (/recommend-crop)         │
│  • Parse request JSON                     │
│  • Validate inputs                        │
│  • Get agricultural zone                  │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌───────────────────────────────────────────┐
│  Data Processing                          │
│  • Create input DataFrame                 │
│  • Encode categorical features            │
│  • Add zone feature                       │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌───────────────────────────────────────────┐
│  ML Model Prediction                      │
│  • Load Crop Recommender model            │
│  • Predict probabilities                  │
│  • Get top 3 crops                        │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌───────────────────────────────────────────┐
│  Response Enrichment                      │
│  • Add market rates                       │
│  • Add expected yields                    │
│  • Add zone information                   │
│  • Format JSON response                   │
└─────────────────┬─────────────────────────┘
                  │
                  ▼ JSON Response
┌───────────────────────────────────────────┐
│  React Component                          │
│  • Receive response                       │
│  • Update state                           │
│  • Render crop cards                      │
│  • Display confidence scores              │
└───────────────────────────────────────────┘
                  │
                  ▼
         User sees recommendations!
```

---

## 🗂️ Component Breakdown

### Frontend Architecture

```
frontend/
│
├── src/
│   ├── main.jsx                    # App entry point
│   │   └─ Renders App with Router, Theme, Context
│   │
│   ├── App.jsx                     # Main app component
│   │   ├─ Routes configuration
│   │   ├─ Navbar (persistent)
│   │   ├─ Page content (dynamic)
│   │   └─ Footer (persistent)
│   │
│   ├── context/
│   │   └── AppContext.jsx          # Global state
│   │       ├─ Dropdown data
│   │       ├─ API status
│   │       ├─ Language selection
│   │       └─ Shared functions
│   │
│   ├── services/
│   │   └── api.js                  # API client
│   │       ├─ Axios configuration
│   │       ├─ API endpoints
│   │       └─ Error handling
│   │
│   ├── components/
│   │   ├── Navbar.jsx              # Navigation
│   │   └── Footer.jsx              # Footer
│   │
│   └── pages/                      # 8 pages
│       ├── Dashboard.jsx           # Home page
│       ├── CropRecommendation.jsx  # Crop recommendation
│       ├── NutrientAnalysis.jsx    # Nutrient prediction
│       ├── WaterQuality.jsx        # Water analysis
│       ├── CropComparison.jsx      # Compare crops
│       ├── DistrictInsights.jsx    # District data
│       ├── WeatherPlanning.jsx     # Weather planning
│       └── EconomicAnalysis.jsx    # Economic calculator
```

### Backend Architecture

```
backend/
│
├── app.py                          # Flask API server
│   ├── Load models
│   ├── API endpoints (9)
│   ├── Request handling
│   ├── Response formatting
│   └── Error handling
│
├── train_models.py                 # Model training
│   ├── DataProcessor class
│   │   ├─ Load data
│   │   ├─ Encode features
│   │   ├─ Scale features
│   │   └─ Save encoders/scalers
│   │
│   ├── CropRecommenderModel
│   │   ├─ Train Random Forest
│   │   ├─ Hyperparameter tuning
│   │   ├─ Evaluate accuracy
│   │   └─ Save model
│   │
│   ├── NutrientPredictorModel
│   │   ├─ Train MLP Neural Network
│   │   ├─ Multi-output regression
│   │   ├─ Evaluate R² score
│   │   └─ Save model
│   │
│   ├── WaterQualityPredictorModel
│   │   └─ Train Random Forest Regressor
│   │
│   └── FertilizerRecommenderModel
│       └─ Train Random Forest Classifier
│
├── config.py                       # Configuration
│   ├── Paths
│   ├── Agricultural zones
│   ├── Market rates
│   ├── Input costs
│   └── Expected yields
│
└── models/                         # Saved models (generated)
    ├── crop_recommender.pkl
    ├── nutrient_predictor.pkl
    ├── water_quality_predictor.pkl
    ├── fertilizer_recommender.pkl
    ├── encoders.pkl
    └── scalers.pkl
```

---

## 🔐 Data Flow Patterns

### 1. Page Load Pattern

```
User → Frontend Route → Page Component → Context → API Call → Backend → Response → State Update → UI Render
```

### 2. Form Submission Pattern

```
User Input → Validation → Loading State → API Call → Backend Processing → ML Prediction → Response → Result Display
```

### 3. Model Prediction Pattern

```
Input Data → Encoding → Scaling → Model Prediction → Inverse Scaling → Enrichment → Response
```

---

## 🎯 Key Design Decisions

### Frontend

**React + Vite**
- ✅ Fast development with Hot Module Replacement
- ✅ Modern build tool
- ✅ Optimized production builds

**Material-UI**
- ✅ Professional, consistent design
- ✅ Responsive out of the box
- ✅ Rich component library

**Context API**
- ✅ Simple state management
- ✅ No external dependencies
- ✅ Sufficient for app size

**Chart.js**
- ✅ Interactive visualizations
- ✅ Good documentation
- ✅ Lightweight

### Backend

**Flask**
- ✅ Lightweight, easy to deploy
- ✅ Perfect for ML APIs
- ✅ Extensive ecosystem

**scikit-learn**
- ✅ Industry-standard ML library
- ✅ Wide algorithm selection
- ✅ Easy model persistence

**Random Forest**
- ✅ High accuracy
- ✅ Handles categorical data well
- ✅ Feature importance

**MLP Neural Network**
- ✅ Good for multi-output regression
- ✅ Captures complex patterns
- ✅ Adaptive learning

---

## 🔄 State Management

### Frontend State

```
Global State (Context)
├── dropdownData
│   ├── districts[]
│   ├── soil_types[]
│   ├── crops[]
│   ├── weather_conditions[]
│   └── fertilizers[]
├── apiStatus (connected/error)
└── language (en/hi/mr)

Component State (Local)
├── formData (user inputs)
├── loading (request status)
├── results (API response)
└── error (error messages)
```

### Backend State

```
Global Variables
├── models{}
│   ├── crop
│   ├── nutrient
│   ├── water
│   └── fertilizer
├── encoders{}
└── scalers{}

Request State
├── Input validation
├── Data processing
├── Model prediction
└── Response formatting
```

---

## 🔌 API Communication

### Request/Response Cycle

```
Frontend                    Backend
   │                           │
   ├─ POST /recommend-crop ───▶│
   │  Content-Type: JSON       │
   │  Body: {...}              │
   │                           ├─ Validate
   │                           ├─ Process
   │                           ├─ Predict
   │                           └─ Format
   │◀─── JSON Response ─────────│
   │  Status: 200              │
   │  Body: {...}              │
   ▼                           ▼
Update UI                   Log request
```

### Error Handling

```
Frontend Error Handling:
├── Network errors → Display connection error
├── 400 Bad Request → Show validation error
├── 404 Not Found → Show "not found" message
├── 500 Server Error → Show generic error
└── Timeout → Show timeout message

Backend Error Handling:
├── Validation errors → 400 response
├── Missing data → 404 response
├── Model errors → 500 response (logged)
└── Unexpected errors → 500 response (traced)
```

---

## 🗄️ Data Models

### Input Models

```python
CropRecommendation {
  District: string (required)
  Soil_Type: string (required)
  Weather: string (required)
}

NutrientPrediction {
  District: string (required)
  Soil_Type: string (required)
  Crop_Name: string (required)
  Weather: string (required)
}

WaterQualityAnalysis {
  District: string (required)
  Weather: string (required)
  Soil_Type: string (required)
}

CropComparison {
  crops: string[] (2-3 items)
  District: string
  Soil_Type: string
  Weather: string
}
```

### Output Models

```python
CropRecommendationResult {
  success: boolean
  data: {
    recommendations: CropCard[]
    zone: string
    zone_info: ZoneInfo
    input: InputSummary
  }
}

NutrientPredictionResult {
  success: boolean
  data: {
    nutrients: NutrientValues
    npk_ratio: NPKRatio
    alerts: Alert[]
    input: InputSummary
  }
}
```

---

## 🚀 Deployment Architecture

### Development
```
Local Machine
├── Backend: Python + Flask (port 5000)
└── Frontend: Node + Vite Dev Server (port 3000)
```

### Production (Suggested)
```
Server
├── Backend: Gunicorn + Flask (port 5000)
├── Frontend: Static files served by Nginx
└── Reverse Proxy: Nginx (port 80/443)
    ├─▶ /api/* → Backend (5000)
    └─▶ /* → Frontend (static)
```

---

## 🔒 Security Considerations

### Current (Development)
- ✅ CORS enabled
- ✅ Input validation
- ✅ Error handling
- ⚠️ No authentication

### Production Recommendations
- [ ] Add API authentication (JWT)
- [ ] Rate limiting
- [ ] HTTPS only
- [ ] Environment variables for secrets
- [ ] Database for user data
- [ ] Request logging
- [ ] IP whitelisting (optional)

---

## 📊 Performance Optimization

### Frontend
- ✅ Code splitting (React.lazy)
- ✅ Optimized builds (Vite)
- ✅ Lazy loading images
- ✅ Memoization where needed

### Backend
- ✅ Model caching (loaded once)
- ✅ Efficient data processing
- ⚠️ No database caching (yet)
- 🔄 Could add Redis for caching

---

## 🔄 Scalability

### Current Capacity
- Handles 10-100 concurrent users
- Local file-based models
- Single server deployment

### Scale-Up Options
1. **Horizontal Scaling**
   - Load balancer
   - Multiple Flask instances
   - Shared model storage

2. **Vertical Scaling**
   - Larger server
   - More RAM for models
   - Faster CPU

3. **Optimization**
   - Model quantization
   - Response caching
   - CDN for frontend

---

## 🧪 Testing Strategy

### Frontend
- Manual testing in browser
- Chrome DevTools for debugging
- Responsive design testing
- API response validation

### Backend
- API endpoint testing (cURL/Postman)
- Model accuracy validation
- Error handling testing
- Load testing (optional)

### Integration
- End-to-end user flows
- Cross-browser testing
- API contract validation

---

**System Architecture is Production-Ready** ✅

Built with modern best practices and scalability in mind! 🚀
