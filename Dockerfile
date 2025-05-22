FROM python:3.11-slim

WORKDIR /app

# Copy script and cron file into container
COPY sync.py .
COPY crontab /etc/cron.d/rd-sync-cron

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron ffmpeg && \
    pip install --no-cache-dir requests && \
    chmod +x /app/sync.py && \
    chmod 0644 /etc/cron.d/rd-sync-cron && \
    crontab /etc/cron.d/rd-sync-cron && \
    rm -rf /var/lib/apt/lists/*

# Declare volume for downloads folder (optional)
VOLUME ["/downloads"]

# Run cron and forward logs
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]
