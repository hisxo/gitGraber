# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 to allow communication to the container
EXPOSE 80

# Define environment variable
ENV ENV_VAR_NAME="value"

# Run app.py when the container launches
CMD ["python", "gitGraber.py"]
