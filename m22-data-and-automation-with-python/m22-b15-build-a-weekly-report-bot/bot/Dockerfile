FROM python:3.14-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.13 /uv /bin/uv
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
COPY src ./src
RUN uv sync --locked --no-dev

FROM python:3.14-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends cron tzdata \
 && rm -rf /var/lib/apt/lists/*
ENV TZ=Asia/Kolkata
RUN useradd --create-home --shell /bin/sh app \
 && mkdir /data && chown app /data
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime
COPY --from=build /app /app
COPY crontab /etc/cron.d/weekly-report
COPY run.sh entrypoint.sh /app/
RUN chmod 0644 /etc/cron.d/weekly-report \
 && chmod +x /app/run.sh /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
