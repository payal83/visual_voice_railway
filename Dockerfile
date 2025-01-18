# Use an official Python image as the base
FROM python:3.9-slim

# Install necessary libraries and tools
RUN apt-get update && apt-get install -y \
    libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev curl build-essential && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Set environment variables
ENV PATH="/root/.cargo/bin:$PATH"

# Set the default port (optional, Railway will override this)
ENV PORT 5000  # You can set a default port, but Railway will override it.

# Copy project files
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn app:app --workers=3 --threads=2 --bind 0.0.0.0:$PORT

