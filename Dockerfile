# Use a specific Python version (using bullseye for better system libs)
FROM python:3.10.13-slim-bullseye # Or python:3.10-slim if you prefer

# Set the working directory inside the container
WORKDIR /code

# Install system dependencies needed for compiling scientific Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgfortran5 \
    pkg-config \
    # Add any other build deps if needed
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy the requirements file first to leverage Docker cache
COPY ./requirements.txt /code/requirements.txt

# Install application dependencies, preferring pre-built binary wheels
RUN pip install --no-cache-dir --prefer-binary -r /code/requirements.txt

# Copy all your application files from the root of your project to the /code directory
COPY . /code/

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
