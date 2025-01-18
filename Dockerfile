# Use Python 3.12.4 slim image
#FROM python:3.12.4-slim
FROM python:3.10-slim


# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies required by the Python libraries
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libgl1 \
    libgtk-3-0 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --upgrade setuptools wheel pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Expose the port the app will run on
EXPOSE 8080

# Command to run the app
CMD ["python", "bank_details_Api_dir.py"]
