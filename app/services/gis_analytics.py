from sqlalchemy.orm import Session
from geoalchemy2 import functions as geo_func
from shapely.geometry import Polygon, Point
import numpy as np
from sklearn.cluster import DBSCAN

from ..models.map import Gudang, Lahan

def advanced_spatial_analysis(db: Session):
    """
    Analisis spasial kompleks dengan machine learning
    """
    # Ambil semua gudang dan lahan
    gudangs = db.query(
        geo_func.ST_X(Gudang.lokasi),
        geo_func.ST_Y(Gudang.lokasi)
    ).all()
    
    lahan_centroids = db.query(
        geo_func.ST_X(geo_func.ST_Centroid(Lahan.area)),
        geo_func.ST_Y(geo_func.ST_Centroid(Lahan.area))
    ).all()
    
    # Gabungkan koordinat
    all_points = np.array(gudangs + lahan_centroids)
 
    # Clustering untuk identifikasi area potensial
    clustering = DBSCAN(eps=0.1, min_samples=3).fit(all_points)
    
    # Pusat cluster sebagai kandidat lokasi baru
    cluster_centers = [
        all_points[clustering.labels_ == label].mean(axis=0)
        for label in set(clustering.labels_) if label != -1
    ]

    return {
        'cluster_centers': cluster_centers,
        'clustering_labels': clustering.labels_
    }

def optimize_gudang_distribution(db: Session):
    """
    Optimasi distribusi gudang berdasarkan analisis spasial
    """
    # Hitung jarak antar gudang
    distances = db.query(
        Gudang.id,
        geo_func.ST_Distance(
            Gudang.lokasi, 
            db.query(geo_func.ST_Centroid(Lahan.area)).first()
        ).label('distance_to_centroid')
    ).order_by('distance_to_centroid').all()
    
    return distances

def calculate_lahan_metrics(db: Session, lahan_id: int):
    """
    Perhitungan metrik lahan komprehensif
    """
    metrics = db.query(
        geo_func.ST_Area(Lahan.area).label('total_area'),
        geo_func.ST_Perimeter(Lahan.area).label('perimeter'),
        geo_func.ST_NumInteriorRings(Lahan.area).label('interior_rings')
    ).filter(Lahan.id == lahan_id).first()
    
    return {
        'area_m2': metrics.total_area,
        'perimeter_m': metrics.perimeter,
        'complex_index': metrics.perimeter / (4 * np.pi * metrics.total_area)
    }