FROM python:3.6

ENV FLASK_APP hyperOSPF.py

COPY hyperOSPF.py gunicorn_config.py requirements.txt ./
COPY app app

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["gunicorn", "--config", "gunicorn.py", "hyperOSPF:app"]