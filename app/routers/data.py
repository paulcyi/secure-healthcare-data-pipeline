from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from prometheus_client import Counter, Histogram, Gauge
import time
from app.auth.auth import get_current_user

# Initialize router
router = APIRouter()

# Prometheus metrics
REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total number of API requests',
    ['endpoint', 'method', 'status']
)

REQUEST_LATENCY = Histogram(
    'api_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

ACTIVE_USERS = Gauge(
    'api_active_users',
    'Number of active users in the system'
)

# Enhanced data models
class PatientRecord(BaseModel):
    patient_id: str
    name: str
    age: int
    condition: str
    status: str
    last_updated: datetime = datetime.now()

class HealthMetrics(BaseModel):
    patient_id: str
    heart_rate: int
    blood_pressure: str
    temperature: float
    oxygen_level: int
    timestamp: datetime = datetime.now()

# Simulated databases
patient_db: Dict[str, PatientRecord] = {}
health_metrics_db: Dict[str, List[HealthMetrics]] = {}

# Enhanced endpoints
@router.post("/patients")
async def create_patient(patient: PatientRecord, current_user: str = Depends(get_current_user)):
    """Create a new patient record"""
    REQUEST_COUNT.labels(
        endpoint="/patients",
        method="POST",
        status="200"
    ).inc()
    
    patient_db[patient.patient_id] = patient
    return {"status": "success", "data": patient}

@router.get("/patients/{patient_id}")
async def get_patient(patient_id: str, current_user: str = Depends(get_current_user)):
    """Retrieve a patient record"""
    if patient_id not in patient_db:
        REQUEST_COUNT.labels(
            endpoint="/patients/{patient_id}",
            method="GET",
            status="404"
        ).inc()
        raise HTTPException(status_code=404, detail="Patient not found")
    
    REQUEST_COUNT.labels(
        endpoint="/patients/{patient_id}",
        method="GET",
        status="200"
    ).inc()
    return patient_db[patient_id]

@router.post("/metrics/{patient_id}")
async def add_health_metrics(
    patient_id: str,
    metrics: HealthMetrics,
    current_user: str = Depends(get_current_user)
):
    """Add health metrics for a patient"""
    if patient_id not in patient_db:
        REQUEST_COUNT.labels(
            endpoint="/metrics/{patient_id}",
            method="POST",
            status="404"
        ).inc()
        raise HTTPException(status_code=404, detail="Patient not found")
    
    if patient_id not in health_metrics_db:
        health_metrics_db[patient_id] = []
    
    health_metrics_db[patient_id].append(metrics)
    
    REQUEST_COUNT.labels(
        endpoint="/metrics/{patient_id}",
        method="POST",
        status="200"
    ).inc()
    return {"status": "success", "data": metrics}

@router.get("/metrics/{patient_id}")
async def get_health_metrics(
    patient_id: str,
    limit: Optional[int] = 10,
    current_user: str = Depends(get_current_user)
):
    """Retrieve health metrics for a patient"""
    if patient_id not in health_metrics_db:
        REQUEST_COUNT.labels(
            endpoint="/metrics/{patient_id}",
            method="GET",
            status="404"
        ).inc()
        raise HTTPException(status_code=404, detail="No metrics found for patient")
    
    REQUEST_COUNT.labels(
        endpoint="/metrics/{patient_id}",
        method="GET",
        status="200"
    ).inc()
    return {"data": health_metrics_db[patient_id][-limit:]}

@router.get("/stats")
async def get_system_stats(current_user: str = Depends(get_current_user)):
    """Get system statistics for monitoring"""
    REQUEST_COUNT.labels(
        endpoint="/stats",
        method="GET",
        status="200"
    ).inc()
    
    return {
        "total_patients": len(patient_db),
        "total_metrics_recorded": sum(len(metrics) for metrics in health_metrics_db.values()),
        "active_users": ACTIVE_USERS._value.get(),
    }