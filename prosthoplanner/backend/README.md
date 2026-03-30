# ProsthoPlanner Backend

This is the Python Flask backend for the ProsthoPlanner Android application. It handles patient data storage and provide AI-driven treatment suggestions.

## Requirements
- Python 3.x
- MySQL (via XAMPP)
- Libraries (installed via pip): `flask`, `flask-cors`, `mysql-connector-python`, `pandas`, `scikit-learn`, `joblib`

## Setup Instructions

1.  **Start MySQL**: Open XAMPP Control Panel and click "Start" next to MySQL.
2.  **Initialize Database**:
    ```bash
    python backend/db_setup.py
    ```
3.  **Run Backend**:
    ```bash
    python backend/app.py
    ```

## API Endpoints
- `GET /health`: Check if backend is running.
- `POST /api/suggest-treatment`: Submit patient info and get AI suggestion.

### Sample Response for `/api/suggest-treatment`:
```json
{
  "patient_db_id": 1,
  "plans": {
    "A": {"treatment": "Full Ceramic Implants", "cost": 180000, "time": "5 Months"},
    "B": {"treatment": "Metal-Ceramic Bridge", "cost": 50000, "time": "2 Weeks"},
    "C": {"treatment": "Acrylic RPD", "cost": 18000, "time": "10 Days"}
  },
  "status": "success"
}
```

- `POST /api/select-plan`: Select one of the suggested plans.
  - Payload: `{"patient_db_id": 1, "selection": "B"}`
