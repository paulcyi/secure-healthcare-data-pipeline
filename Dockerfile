# Step 1: Build stage
FROM python:3.11-slim AS build-stage

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Step 2: Production stage
FROM python:3.11-slim AS production-stage

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies installed in the build stage
COPY --from=build-stage /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build-stage /app /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Explicitly use the path to uvicorn in the CMD
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
