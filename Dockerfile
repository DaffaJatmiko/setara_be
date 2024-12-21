# Dockerfile
FROM python:3.10-slim

# Set working directory di container
WORKDIR /app

# Install gcc untuk kompilasi beberapa package Python
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt dulu
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy seluruh code aplikasi ke container
COPY . .

# Command untuk menjalankan aplikasi
CMD ["python", "main.py"]