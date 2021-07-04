ARG image=address:latest
FROM $image

WORKDIR /app

ARG env=prod

ENV C_FORCE_ROOT=1

ADD ./app /app

ENV PYTHONPATH=/app

COPY ./app/worker-start.sh /worker-start.sh

RUN chmod +x /worker-start.sh

CMD ["bash", "/worker-start.sh"]
