# Dockerfile
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=core/server.py

# Command to run the Flask app
CMD ["bash", "run.sh"]
