# Use an official Python runtime as a parent image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .
COPY consumer.py .
ADD gbt_model .

# ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/

# Install any needed packages specified in requirements.txt
RUN apt-get update
RUN apt-get install default-jdk -y
RUN pip install --no-cache-dir -r requirements.txt

# Run consumer.py when the container launches
CMD ["python", "consumer.py"]
