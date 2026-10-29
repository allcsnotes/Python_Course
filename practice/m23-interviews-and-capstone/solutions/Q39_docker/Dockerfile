FROM python:3.14-slim
RUN useradd --create-home --uid 10001 app
WORKDIR /home/app
RUN pip install --no-cache-dir pydantic-settings
COPY settings.py .
USER app
CMD ["python", "settings.py"]
