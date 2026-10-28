FROM python:3.12-slim

# uv binary from its official image, pinned to an exact version.
COPY --from=ghcr.io/astral-sh/uv:0.12.24 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Dependencies first, so this layer is cached while only the code changes.
COPY pyproject.toml uv.lock .python-version ./
# The uv cache is mounted only during the build, so it does not end up in the image.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-default-groups --no-install-project

# The rules documents ship with the image: on start the server ingests them (see infra/).
COPY app ./app
COPY data ./data

RUN useradd --create-home appuser
USER appuser

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
