# ---- build stage: uv installs the locked dependencies ----
FROM python:3.14-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.13 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

# ---- runtime stage: only the venv and the code, no root ----
FROM python:3.14-slim
RUN useradd --create-home app
WORKDIR /app
COPY --from=build /app/.venv /app/.venv
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini gunicorn.conf.py ./
ARG APP_VERSION=dev
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 \
    APP_VERSION=$APP_VERSION
USER app
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s --start-period=10s --retries=5 \
  CMD ["python", "-c", "import urllib.request as u; u.urlopen('http://localhost:8000/health/ready', timeout=2)"]
CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
