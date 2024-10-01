# Use an official Python runtime as a parent image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .
COPY consumer.py .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run consumer.py when the container launches
CMD ["python", "consumer.py"]
