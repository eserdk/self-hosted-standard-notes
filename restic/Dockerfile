FROM restic/restic:0.12.1

RUN mkdir -p /mnt/restic /var/spool/cron/crontabs /var/log; \
    touch /var/log/cron.log

COPY backup.sh /bin/backup
COPY entry.sh /entry.sh

WORKDIR /

ENTRYPOINT ["/entry.sh"]
CMD ["tail","-fn0","/var/log/cron.log"]