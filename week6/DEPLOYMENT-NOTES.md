
# Deployment & Monitoring Notes

## 1. API Deployment
The Model API is built with FastAPI and can be deployed using Docker.

### Local Execution
```bash
# Install dependencies
pip install -r requirements.txt

# Run API
uvicorn deployment.api:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Deployment
```bash
# Build Image
docker build -t adult-income-api -f deployment/Dockerfile .

# Run Container
docker run -p 8000:8000 adult-income-api
```

### API Usage
**Endpoint:** `POST /predict`
**Example Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "age": 45,
           "workclass": "Private",
           "fnlwgt": 83311,
           "education": "Bachelors",
           "education.num": 13,
           "marital.status": "Married-civ-spouse",
           "occupation": "Exec-managerial",
           "relationship": "Husband",
           "race": "White",
           "sex": "Male",
           "capital.gain": 15000,
           "capital.loss": 0,
           "native.country": "United-States"
         }'
```

**Response:**
```json
{
    "request_id": "35eb7309-6e69-4b39-ada8-c8a3fa312f2d",
    "prediction": "<=50K",
    "probability": 0.8915197253227234
}
```

## 2. Monitoring
Implement basic monitoring for data drift and prediction logging.

### Logs
- Predictions are logged to `monitoring/prediction_logs.csv`.
- Format: `request_id, timestamp, inputs..., prediction, probability`

### Drift Detection
Run the drift checker to compare current logs against training data:
```bash
python monitoring/drift_checker.py
```
Outputs a report to `monitoring/drift_report.json`.

### Dashboard
Launch the monitoring dashboard to visualize logs and drift status:
```bash
streamlit run monitoring/dashboard.py
```
- Custom Dashboard: [http://localhost:8501](http://localhost:8501)

## 3. Prediction Frontend (Streamlit)
To use the user-friendly prediction interface:
```bash
streamlit run deployment/app.py
```
**Important:** The FastAPI server must be running (Step 1) for the frontend to make successful predictions. If the API is not running, we will see a "Connection refused" error.

