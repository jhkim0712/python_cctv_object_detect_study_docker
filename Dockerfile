# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements (if you want to use requirements.txt, otherwise install inline)
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# Install Python dependencies

# Install Python dependencies
RUN pip install --no-cache-dir opencv-python ultralytics flask

# Copy the rest of the application code
COPY . .

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Create output directory
RUN mkdir -p /output

# Start both the detection script and the web server using a process manager
CMD ["sh", "-c", "python python_opencv.py --output_dir /output & python web_stream.py"]
