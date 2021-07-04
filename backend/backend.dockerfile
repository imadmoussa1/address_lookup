ARG image=address:latest
FROM $image

WORKDIR /app/

COPY ./start.sh /start.sh
RUN chmod +x /start.sh
COPY ./gunicorn_conf.py /gunicorn_conf.py
ARG env=prod
ADD ./app /app
ENV PYTHONPATH=/app
EXPOSE 80
CMD ["/start.sh"]
