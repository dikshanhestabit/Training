
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if needed 
# RUN apt-get update && apt-get install -y gcc

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port
EXPOSE 8000

# Set python path
ENV PYTHONPATH=/app

# Run Command
CMD ["uvicorn", "deployment.api:app", "--host", "0.0.0.0", "--port", "8000"]
