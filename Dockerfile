# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file from Challenge1
COPY Challenge1/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory structure
COPY . .

# Expose Jupyter Lab port
EXPOSE 8895

# Set environment variables for Jupyter Lab
ENV JUPYTER_ENABLE_LAB=yes

# Run Jupyter Lab (accessible from root directory containing all challenges)
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8895", "--no-browser", "--allow-root", "--notebook-dir=/app"]

