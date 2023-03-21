FROM python:3.9.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/matchbot

COPY ./req.txt /usr/src/req.txt
RUN pip install -r /usr/src/req.txt


COPY . /usr/src/matchbot
CMD ["python", "bot.py"]
