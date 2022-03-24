FROM alpine:3.15
MAINTAINER @Lordslair

RUN adduser -h /code -u 1000 -D -H redsub

ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ARG LOGURU_DATE="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
ARG LOGURU_LEVEL="<level>level={level: <8}</level> | "
ARG LOGURU_MSG="<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
ENV LOGURU_FORMAT=$LOGURU_DATE$LOGURU_LEVEL$LOGURU_MSG
ENV LOGURU_COLORIZE='true'
ENV LOGURU_DEBUG_COLOR='<cyan><bold>'

ENV PYTHONUNBUFFERED='True'
ENV PYTHONIOENCODING='UTF-8'

COPY                       requirements.txt /requirements.txt
COPY --chown=redsub:redsub subscriber.py     /code/subscriber.py

RUN apk update --no-cache \
    && apk add --no-cache python3 \
    && apk add --no-cache --virtual .build-deps \
                                    tzdata \
    && cp /usr/share/zoneinfo/Europe/Paris /etc/localtime \
    && cd /code \
    && su redsub -c "python3 -m ensurepip --upgrade \
                     && /code/.local/bin/pip3 install --user -U -r /requirements.txt" \
    && apk del .build-deps \
    && rm /requirements.txt

USER redsub
WORKDIR /code
ENV PATH="/code/.local/bin:${PATH}"

ENTRYPOINT ["/code/subscriber.py"]
