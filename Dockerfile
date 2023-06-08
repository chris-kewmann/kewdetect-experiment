FROM python:3.8.16-slim-bullseye

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY .env /code

EXPOSE 8000

# CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]
CMD ["uvicorn", "app.main:app", "--port", "8000", "--reload"]
