from datetime import datetime, timedelta
import requests
import random
import json
import time

def generate_patient():
    conditions = ["Hypertension", "Diabetes", "Asthma", "COPD", "Heart Disease"]
    statuses = ["Stable", "Critical", "Improving", "Under Observation", "Recovery"]
    
    return {
        "patient_id": f"P{random.randint(1000, 9999)}",
        "name": f"Test Patient {random.randint(1, 100)}",
        "age": random.randint(25, 85),
        "condition": random.choice(conditions),
        "status": random.choice(statuses)
    }

def generate_health_metrics():
    return {
        "heart_rate": random.randint(60, 100),
        "blood_pressure": f"{random.randint(110, 140)}/{random.randint(70, 90)}",
        "temperature": round(random.uniform(36.5, 37.5), 1),
        "oxygen_level": random.randint(95, 100)
    }

class HealthcareDataGenerator:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.auth_token = None
        self.patients = []

    def setup_auth(self):
        """Create a test user and get authentication token"""
        # Create test user
        signup_data = {
            "username": f"testuser_{random.randint(1000, 9999)}",
            "password": "testpass123!"
        }
        
        try:
            # Sign up
            requests.post(f"{self.base_url}/auth/signup", json=signup_data)
            
            # Login to get token
            response = requests.post(f"{self.base_url}/auth/login", json=signup_data)
            self.auth_token = response.json()["access_token"]
            return True
        except Exception as e:
            print(f"Auth setup failed: {e}")
            return False

    def generate_data(self, num_patients=5, readings_per_patient=10):
        """Generate test patients and their health readings"""
        if not self.auth_token:
            if not self.setup_auth():
                return False

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Create patients
        for _ in range(num_patients):
            patient_data = generate_patient()
            try:
                response = requests.post(
                    f"{self.base_url}/data/patients",
                    json=patient_data,
                    headers=headers
                )
                if response.status_code == 200:
                    self.patients.append(patient_data["patient_id"])
                    print(f"Created patient {patient_data['patient_id']}")

                    # Generate health metrics for this patient
                    for _ in range(readings_per_patient):
                        metrics_data = {
                            "patient_id": patient_data["patient_id"],
                            **generate_health_metrics()
                        }
                        
                        metrics_response = requests.post(
                            f"{self.base_url}/data/metrics/{patient_data['patient_id']}",
                            json=metrics_data,
                            headers=headers
                        )
                        
                        if metrics_response.status_code == 200:
                            print(f"Added health metrics for {patient_data['patient_id']}")
                        
                        # Small delay to simulate real-world data flow
                        time.sleep(0.5)

            except Exception as e:
                print(f"Error generating data: {e}")
                continue

        return True

if __name__ == "__main__":
    generator = HealthcareDataGenerator()
    generator.generate_data(num_patients=10, readings_per_patient=20)