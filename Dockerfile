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

# <approach 1>
# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# </approach 1>

# <approach 2>
# RUN pip install --no-cache-dir flask
# RUN pip install --no-cache-dir vanna[chromadb,openai]
# RUN pip install --no-cache-dir databricks-sql-connector
# </approach 2>

COPY . .

FROM base AS final

EXPOSE 8084

CMD ["python", "app.py"]