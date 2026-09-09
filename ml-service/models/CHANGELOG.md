# Model Changelog

## v1

- **Status**: production
- **Date**: 2026-09-04
- **Architecture**: Hierarchical Gate Classifier + SSP/NPK Specialists
- **Gate Classifier**: RandomForest (200 trees, balanced class weights), 7-class
- **SSP Specialist**: Binary RandomForest (SSP vs NPK)
- **NPK Specialist**: Binary RandomForest (NPK vs SSP)
- **Features**: Soil_pH, Nitrogen_Level, Phosphorus_Level, Potassium_Level, Temperature, Humidity, Rainfall, Soil_Moisture, Crop_Growth_Stage, Soil_Type, Crop_Type
- **Dataset**: fertilizer_recommendation.csv (dataset-v1, 10,000 samples)
- **Gate Accuracy**: 87.70%
- **Gate CV Accuracy**: 88.32%
- **SSP F1 (specialist)**: 0.6355
- **NPK F1 (specialist)**: 0.8251
- **Notes**: Initial production model. SSP/NPK boundary remains the hardest classification problem due to similar nutrient profiles.
