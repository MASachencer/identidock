FROM python:3

WORKDIR /app
COPY app /app
COPY requirement.txt /
COPY shell.sh /
RUN pip install -U -r /requirement.txt
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

USER uwsgi
EXPOSE 9090 9191

CMD ["/shell.sh"]