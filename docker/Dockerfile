FROM python:3.6-alpine

LABEL maintainer="Zachary Romer <romerzs14@gmail.com>"

ENV PGBADGER_DATA=/data
ENV PGBADGER_VERSION=11.0
ENV PGBADGER_PREFIX=/opt/pgbadger-${PGBADGER_VERSION}
ENV PATH=${PGBADGER_PREFIX}:$PATH

RUN apk --no-cache add coreutils \
    openssl \
    perl \
  && mkdir -p /data /opt \
  && wget -O - https://github.com/darold/pgbadger/archive/v11.0.tar.gz | tar -zxvf - -C /opt

COPY get_log_files.py /entrypoint.py

VOLUME $PGBADGER_DATA

ENTRYPOINT ["/entrypoint.py"]

CMD ["python3"]