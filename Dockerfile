FROM sitch/feed_builder:latest

RUN mkdir -p /var/lib/sitch/feed/fcc/

COPY get_fcc_feed.py /

RUN apk add -U expect tcl

RUN unbuffer /usr/local/bin/pypy /get_fcc_feed.py

VOLUME /var/lib/sitch/feed/fcc/

CMD ["true"]
