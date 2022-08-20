FROM python:slim

RUN useradd to_do_restful_api

WORKDIR /home/to_do_restful_api

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY to_do_restful_api.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP to_do_restful_api.py

RUN chown -R to_do_restful_api:to_do_restful_api ./
USER to_do_restful_api

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]