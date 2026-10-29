FROM m20l03-api:base
USER root
COPY --from=ghcr.io/astral-sh/uv:0.13 /uv /bin/uv
RUN uv pip install --python /app/.venv/bin/python py-spy
USER app
