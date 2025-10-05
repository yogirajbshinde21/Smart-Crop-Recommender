# Smart Farmer Backend

Flask-based REST API with Machine Learning models for agricultural recommendations.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Train models (first time):
```bash
python train_models.py
```

3. Run server:
```bash
python app.py
```

Server runs on: http://localhost:5000

## API Endpoints

- `GET /health` - Health check
- `GET /dropdown-data` - Get all options
- `POST /recommend-crop` - Crop recommendations
- `POST /predict-nutrients` - Nutrient predictions
- `POST /water-quality-analysis` - Water analysis
- `POST /fertilizer-recommendation` - Fertilizer suggestions
- `POST /compare-crops` - Compare crops
- `GET /district-insights/<district>` - District data
- `GET /statistics` - System stats

## Models

1. **Crop Recommender** - Random Forest (>80% accuracy)
2. **Nutrient Predictor** - MLP Neural Network (R²>0.75)
3. **Water Quality** - Random Forest Regressor
4. **Fertilizer Recommender** - Random Forest Classifier

All models saved in `models/` directory.
