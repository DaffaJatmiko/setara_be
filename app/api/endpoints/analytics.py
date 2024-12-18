from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.gis_analytics import (
    advanced_spatial_analysis, 
    optimize_gudang_distribution,
    calculate_lahan_metrics
)
from app.schemas.map import LahanCreate, LahanRead, GudangCreate, GudangRead

lahan_router = APIRouter(prefix="/lahan", tags=["Lahan"])
gudang_router = APIRouter(prefix="/gudang", tags=["Gudang"])

@lahan_router.get("/distributions")
def analyze_lahan_distribution(db: Session = Depends(get_db)):
    """
    Endpoint analisis distribusi lahan dengan ML
    """
    try:
        analysis_result = advanced_spatial_analysis(db)
        return {
            "status": "success",
            "cluster_centers": analysis_result['cluster_centers']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@gudang_router.get("/optimize")
def optimize_gudang(db: Session = Depends(get_db)):
    """
    Endpoint optimasi distribusi gudang
    """
    try:
        optimization_result = optimize_gudang_distribution(db)
        return {
            "status": "success",
            "gudang_distribution": optimization_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@lahan_router.get("/{lahan_id}/metrics")
def get_lahan_metrics(
    lahan_id: int, 
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk mendapatkan metrik detail lahan
    """
    metrics = calculate_lahan_metrics(db, lahan_id)
    return metrics