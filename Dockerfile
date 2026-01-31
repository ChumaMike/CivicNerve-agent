# 🐍 Base Image: Python 3.10 Slim
FROM python:3.10-slim

# 🛠️ System Dependencies
# FIX: Replaced 'libgl1-mesa-glx' with 'libgl1' for newer Debian versions
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 📂 Working Directory
WORKDIR /app

# 📦 Install Python Dependencies
# (Copy requirements first to cache layers)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🚀 Copy the Codebase
COPY . .

# 🔌 Expose Ports
EXPOSE 8000 8501 8502

# Default command
CMD ["python", "-m", "src.system.api"]