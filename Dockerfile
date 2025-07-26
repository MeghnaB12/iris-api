FROM python:3.10.13-slim-bullseye

# Set working directory
WORKDIR /code

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for numpy, pandas, scikit-learn
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gfortran \
    libatlas-base-dev \
    liblapack-dev \
    libgfortran5 \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools for modern builds
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements file
COPY ./requirements.txt /code/requirements.txt

# Install Python dependencies (prefer binary wheels to avoid source build issues)
RUN pip install --no-cache-dir --prefer-binary -r /code/requirements.txt

# Copy app source code
COPY . /code/

# Expose port (optional, for documentation purposes)
EXPOSE 80

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
