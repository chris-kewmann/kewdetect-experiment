FROM python:3.8.16-slim-bullseye

WORKDIR /mlflow

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 5000

CMD ["mlflow", "ui", "--host", "127.0.0.1"]
