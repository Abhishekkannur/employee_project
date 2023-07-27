FROM python:3.11-slim

WORKDIR /code

COPY ./requirement.txt /code/requirement.txt

RUN pip install -r requirement.txt
RUN apt-get update && apt-get install -y libpq-dev

COPY /app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
