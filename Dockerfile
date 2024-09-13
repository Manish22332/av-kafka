# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY src/ ./src
COPY config/ ./config

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the main script
CMD ["python", "src/main.py"]
