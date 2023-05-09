# kewdetect-experiment

gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --reload

uvicorn app.main:app --host 0.0.0.0 --port 80 --reload