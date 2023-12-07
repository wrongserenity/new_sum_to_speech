FROM python:3.10

WORKDIR /usr/app/src

COPY . .
COPY requirements.txt .

RUN pip install -r requirements.txt

RUN crontab crontab

CMD ["crond", "-f"]