# kewdetect-experiment

## System Design

## Database Design

## Selected Algorithm
    - Local Outlier Factor (LOF)
    - Isolation Forest


## 1. Prerequisites
- create and activate virtualenv (preferably : Python 3.8)
- pip install -r ./requirements.txt

## 2. How to Run
- open new tab, execute following command:
```bash
mlflow ui
```
- open new tab, execute following command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
```

## 2. How to Run (using gunicorn)
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --reload
```

## Documentation 
```
Open 127.0.0.1/docs on your browser
```