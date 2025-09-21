# Start from a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file first
COPY requirements.txt ./

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# The command to run when the container starts
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
