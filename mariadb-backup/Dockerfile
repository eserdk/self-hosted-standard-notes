FROM alpine

RUN apk update && \
    apk upgrade && \
    apk add --no-cache mariadb-client openssl

COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
