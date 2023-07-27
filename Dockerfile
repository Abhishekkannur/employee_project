FROM python:3.11-slim

WORKDIR /code

COPY ./requirement.txt /code/requirement.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirement.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
