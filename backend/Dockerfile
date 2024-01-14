# Use the official Python base image
FROM python:3.9.18-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Set the PYTHONPATH environment variable to execute FLEE
ENV PYTHONPATH /app/flee:${PYTHONPATH}

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Install the necessary system dependencies
# (otherwise installing FLEE dependencies will fail due to mpi4py dependency)
RUN apt-get update && apt-get install -y \
    libopenmpi-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install FLEE dependencies
RUN pip install -r flee/requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 80

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
