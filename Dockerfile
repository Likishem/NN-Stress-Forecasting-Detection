# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for faster builds)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files
COPY ACC.csv .
COPY BVP.csv .
COPY EDA.csv .
COPY HR.csv .
COPY IBI.csv .
COPY TEMP.csv .
COPY stress_classifier.py .
COPY app.py .

# Expose Flask’s default port
EXPOSE 5000

# Default command when the container runs
CMD ["python", "app.py"]

