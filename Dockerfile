FROM python:3.7.0

WORKDIR /app
COPY app /app
COPY cmd.sh /
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install -U -r /app/requirement.txt

USER uwsgi
EXPOSE 9090 9191

CMD ["/cmd.sh"]