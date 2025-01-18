# Use an official Python image
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev curl build-essential

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy pre-downloaded model into the container
COPY pretrained_model ./pretrained_model

# Expose the port
ENV PORT 5000

# Start the app
# Start the app using gunicorn, use the environment variable for port
CMD gunicorn --workers=2 app:app --bind 0.0.0.0:$PORT
