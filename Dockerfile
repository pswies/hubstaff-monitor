FROM python:3.8 AS base
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app

FROM base
ENV PYTHONPATH /app
ENV check_date ""
CMD ["python3", "monitor/run.py"]
