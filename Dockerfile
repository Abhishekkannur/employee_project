FROM  tiangolo/uvicorn-gunicorn-fastapi:python3.11
WORKDIR /app
COPY . /app
RUN pip install -r requirement.txt
EXPOSE 8000

ENTRYPOINT ["python","manage.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
