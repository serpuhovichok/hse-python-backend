FROM python:3.12

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml /app/
COPY poetry.lock /app/
RUN poetry install

COPY . /app

CMD ["poetry", "run", "uvicorn", "lecture_2.hw.shop_api.main:app", "--host", "0.0.0.0", "--port", "80"]