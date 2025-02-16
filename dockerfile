FROM python:3.11.9-slim
ARG AIPROXY_TOKEN
ENV AIPROXY_TOKEN=${AIPROXY_TOKEN}
#COPY . /app
WORKDIR /app
COPY requirements.txt .

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
RUN pip install --no-cache-dir -r requirements.txt
# # Use slim image to reduce size and build time
# # Use slim image for smaller size and faster builds
# FROM python:3.11-slim AS base

# # Set working directory
# WORKDIR /app

# # Install system dependencies required for packages
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends build-essential libpq-dev curl && \
#     rm -rf /var/lib/apt/lists/*

# # Leverage Docker cache: copy requirements separately
# COPY requirements.txt .

# # Install pip packages with retry mechanism and timeout adjustments
# ENV PIP_DEFAULT_TIMEOUT=100 \
#     PIP_NO_CACHE_DIR=off \
#     PIP_DISABLE_PIP_VERSION_CHECK=on

# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir wheel && \
#     pip install --no-cache-dir -r requirements.txt --timeout=100 --retries=5

# # Copy the entire project after installing dependencies
# COPY . .

# # Expose port for FastAPI
# EXPOSE 8000

# # Start FastAPI server
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]