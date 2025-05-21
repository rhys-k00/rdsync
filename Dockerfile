FROM python:3.11-slim

WORKDIR /app

COPY sync.py .

# Install required packages
RUN apt-get update && \
    apt-get install -y cron ffmpeg && \
    pip install requests && \
    rm -rf /var/lib/apt/lists/*

# Make sure the script is executable
RUN chmod +x /app/sync.py

# Add cron job file inside container
COPY crontab /etc/cron.d/rd-sync-cron

# Set correct permissions for cron job
RUN chmod 0644 /etc/cron.d/rd-sync-cron && \
    crontab /etc/cron.d/rd-sync-cron

# Declare volume for downloads folder (optional)
VOLUME /downloads

# Run cron and forward its logs to Docker logs
CMD ["sh", "-c", "cron && tail -f /proc/1/fd/1"]
