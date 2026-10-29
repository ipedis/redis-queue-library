FROM python:3.12.16-slim-trixie@sha256:aa943ce411423c7582288f18707ff66eddcbaeb510502d747a72aeb34f30d159

COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /bin/uv

# Keep the virtualenv outside /app: docker-compose bind-mounts the project over /app.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONPATH=/app

WORKDIR /app

# Install the locked dependencies first to benefit from layer caching
COPY pyproject.toml uv.lock README.md LICENSE /app/
RUN uv sync --locked --no-install-project

COPY . /app
RUN uv sync --locked

RUN useradd --create-home --uid 1000 app && chown -R app:app /app /opt/venv
USER app

ENTRYPOINT ["/opt/venv/bin/python", "demo/demo_script.py"]
