# Use a specific Python version
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /code

# Install build dependencies and update pip/setuptools
# This is crucial for compiling packages like numpy and scikit-learn
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy the requirements file first to leverage Docker cache
COPY ./requirements.txt /code/requirements.txt

# Install application dependencies
# This step will now have the necessary build tools
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy all your application files from the root of your project to the /code directory
COPY . /code/

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
