# Test Data Generation Scripts

This directory contains scripts for generating test data for the Secure Healthcare Data Pipeline project.

## generate_test_data.py

This script generates realistic test data for the healthcare pipeline, including:
- Patient records with various conditions and statuses
- Health metrics (heart rate, blood pressure, temperature, oxygen levels)
- Simulated data flow over time

### Usage

Make sure your FastAPI server is running, then:

```bash
python scripts/generate_test_data.py
```

The script will:
1. Create a test user
2. Generate multiple test patients
3. Add health metrics for each patient
4. Simulate real-world data flow with timestamps

### Configuration

You can modify the following parameters in the script:
- `num_patients`: Number of test patients to create
- `readings_per_patient`: Number of health metric readings per patient
- Base URL for the API (defaults to http://localhost:8000)
