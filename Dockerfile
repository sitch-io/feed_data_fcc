FROM sitch/feed_builder:latest
COPY fcc.csv.gz /var/lib/sitch/feed/fcc/

VOLUME /var/lib/sitch/feed/fcc/

CMD ["true"]
