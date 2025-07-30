FROM python:3.12-slim

RUN pip install pipenv

WORKDIR /code 

COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --system --deploy

COPY .env ./
COPY ./src ./src

CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]