import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from schemas.prediction import FertilizerPredictionRequest, FertilizerPredictionResponse
from inference.model_registry import model_registry
from inference.predictor import predictor

model_ready = False
model_load_error = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_ready, model_load_error
    try:
        active_ver = model_registry.get_active_version_name()
        model_registry.load_bundle(active_ver)
        model_ready = True
        model_load_error = None
        print(f"[ML Service] Successfully loaded model version: {active_ver}")
    except Exception as e:
        model_ready = False
        model_load_error = str(e)
        print(f"[ML Service] FAILED to load active model: {e}", file=sys.stderr)
    yield

app = FastAPI(
    title="Fertilizer Recommendation ML Service",
    description="Internal ML inference service for XGBoost fertilizer recommendation model",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    active_version = model_registry.get_active_version_name()
    return {
        "status": "healthy",
        "model_version": active_version
    }

@app.get("/ready")
def readiness_check():
    active_version = model_registry.get_active_version_name()
    if not model_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "model_loaded": False,
                "model_version": active_version,
                "error": model_load_error
            }
        )
    return {
        "status": "ready",
        "model_loaded": True,
        "model_version": active_version
    }

@app.post("/predict", response_model=FertilizerPredictionResponse)
def predict_fertilizer(request: FertilizerPredictionRequest):
    if not model_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML Service is not ready. Model failed to load."
        )

    try:
        input_features = request.model_dump()
        active_ver = model_registry.get_active_version_name()
        res = predictor.predict(input_features, version=active_ver)
        return FertilizerPredictionResponse(**res)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Inference error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
