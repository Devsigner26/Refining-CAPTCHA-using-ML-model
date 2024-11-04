# Stage 1: Build Stage
# Use the official Python image as the base for building dependencies
FROM python:3.9-slim AS builder

# Set environment variables to prevent prompts during installation
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy only the requirements file for dependency caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime Stage
# Start with a fresh Python image for a minimal runtime
FROM python:3.9-slim

# Set environment variables again for the final image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy dependencies from the builder stage
COPY --from=builder D:/SIH PS1/venv

# Set the PATH environment variable to include the installed packages
ENV PATH=D:/

# Set the working directory
WORKDIR /app

# Copy the application code from the local machine to the container
COPY . .

# Expose the port on which the FastAPI app will run
EXPOSE 8000

# Define the entrypoint for running the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
