# SITCH Feed Data Container Builder for FCC License Database

## Builds a data container for FCC License Database feed.

### Building:

```
python ./get_fcc_feed.py
docker build -t fcc_feed .
Inside the container, the feed can be found at
`/var/lib/sitch/feed/fcc/fcc.csv.gz`
```
