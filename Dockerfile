FROM python:3.10.12

WORKDIR /app

COPY requirements.txt requirements.txt

COPY ./app/ .

RUN pip install -r requirements.txt

CMD ["python3", "-u", "main.py"]
