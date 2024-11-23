FROM python:3.12

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY ./api api/
COPY ./general general/
COPY ./src src/
COPY main.py .

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install --no-root

CMD ["poetry", "run", "python", "main.py"]
