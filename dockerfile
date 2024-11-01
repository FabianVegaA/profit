FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app
WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

ENTRYPOINT ["uv", "run"]
