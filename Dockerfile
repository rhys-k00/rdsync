FROM python:3.11-slim

WORKDIR /app

COPY sync.py .

RUN pip install requests

# Install cron
RUN apt-get update && apt-get install -y cron

# Make sure the script is executable (optional)
RUN chmod +x /app/sync.py

# Add cron job file inside container
COPY crontab /etc/cron.d/rd-sync-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/rd-sync-cron

# Apply the cron job
RUN crontab /etc/cron.d/rd-sync-cron

# Create the log file so cron can write logs
RUN touch /var/log/cron.log

# Declare volume for downloads folder (optional)
VOLUME /downloads

# Run cron in foreground and tail the log file so container stays alive and you see logs
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]
