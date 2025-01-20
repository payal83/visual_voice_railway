# Use the Python 3.9-slim base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port that Flask will run on
EXPOSE 5000
# Use an official Python image as the base

CMD gunicorn app:app --timeout 120 --workers=3 --threads=2 --bind 0.0.0.0:5000

