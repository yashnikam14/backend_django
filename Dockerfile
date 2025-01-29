# Use the official Python image
FROM python:3.10-slim

# Install system dependencies for mysqlclient and build tools
RUN apt-get update \
    && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /django_backend/base_app

# Copy the current directory contents into the container
COPY . /django_backend/base_app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (optional, depending on your application setup)
EXPOSE 8000

# Command to run your app (adjust based on your app's entry point)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
