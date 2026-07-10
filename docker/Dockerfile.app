FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /code

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/code/.venv/bin:$PATH"

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen --no-dev

COPY .env ./
COPY ./src ./src

CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
