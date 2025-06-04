
# Use the official Python 3.13.3-slim base image
FROM python:3.13.3-slim

# Set environment variables
ENV ACCEPT_EULA=Y
ENV SERVER_DOMAIN = http://4.247.151.9

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl apt-transport-https gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    apt-get install -y msodbcsql17 unixodbc-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a directory for the app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code
COPY . .

# # Expose the port FastAPI will run on
# EXPOSE 8000

# # Command to run the FastAPI server
# CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]

EXPOSE 3100

CMD ["gunicorn", "--bind", "0.0.0.0:3100", "app:app", "--worker-class", "uvicorn.workers.UvicornWorker"]