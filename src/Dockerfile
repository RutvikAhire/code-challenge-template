FROM python:3.10.10-alpine3.17

WORKDIR /app-docker

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 run.py