FROM python:3.14-slim
RUN apt-get update && apt-get install -y --no-install-recommends cron && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir openpyxl==3.1.5
WORKDIR /app
CMD ["cron", "-f"]
