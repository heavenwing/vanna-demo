FROM python:3.13-slim AS base

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM base AS final

# Expose the port FastAPI will run on
EXPOSE 8084

CMD ["python", "api.py"]