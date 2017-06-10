# pytsdb

> Featureless Python adapter for OpenTSDB
## Requirements
Requires Python version 3.3 or greater

## Installation
```bash
pip3 install git+ssh://git@github.com/WhoopInc/pytsdb@v0.2.2
```

## Usage
```python
import datetime
import pytsdb

con = pytsdb.connect("hostname.example.com")
con.fetch_metric(metric="host0.cpu",
    start=datetime.datetime(2014, 1, 27),
    tags={ 'user_id': 44 },
    end=datetime.datetime(2014, 1, 29))
>>> { '1390955680': 66.0, '1390955681': 63.0 }
```

## Handling errors
```python

try:
    con.fetch_metric(...)
except pytsdb.TimeoutError:
    print("Is TSDB running?!")
```

## Release
Skip this section unless you're hacking on pytsdb!

To cut a new release, bump the version number in `setup.py` and in the
README installation instructions. Then:

```bash
git add -A
git commit
git tag -a "vx.x.x"
git push --follow-tags
```
