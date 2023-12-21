FROM python:3.10

WORKDIR /usr/app/src

ADD . .

RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y libportaudio2
RUN python -m spacy download ru_core_news_sm
RUN pip install lxml
RUN chmod a+x run.sh

CMD ["./run.sh"]
