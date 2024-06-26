# This Dockerfile is configured for general deployment.

#------- [Base] -------#

# Use the lightweight Python 3.8-slim base image
FROM python:3.8-slim

# Install system dependencies and clean up in a single RUN command
RUN apt-get update && \
    #TODO: add postgresql libpq-dev later if needed
    apt-get install -y  gcc postgresql libpq-dev && \ 
    rm -rf /var/lib/apt/lists/* && \
    # Set up the Python virtual environment
    python -m venv /opt/venv && \
    chmod +x /opt/venv/bin/activate

ENV PATH="/opt/venv/bin:$PATH"


# Copy the requirements.txt file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Run collect static
RUN python manage.py collectstatic --noinput


# ------- [Non-Railway Specific] -------

# Expose the default Gunicorn port
EXPOSE 8000

# Copy the entrypoint script
COPY entrypoint.sh .

# Give the execution permissions to the entrypoint script
RUN chmod +x ./entrypoint.sh

# Run the entrypoint script when the container starts
CMD ["./entrypoint.sh"]