import datetime
import requests

class ConnectionError(Exception):
    pass

class QueryError(Exception):
    pass

class TimeoutError(Exception):
    pass

class Connection(object):
    def __init__(self, host="localhost", port=4242, timeout=1):
        self.url = "http://{0}:{1}/api".format(host, port)
        self.timeout = timeout
        if not self.__valid():
            raise ConnectionError()

    def fetch_metric(self, metric, start, end, tags={}, aggregator="sum",
        downsample=None, ms_resolution=True):
        """Fetch time series data from OpenTSDB

        Parameters:
            metric:
                A string representing a valid OpenTSDB metric.

            tags:
                A dict mapping tag names to tag values. Tag names and values are
                always strings.

                { 'user_id': '44' }

            start:
                A datetime.datetime-like object representing the start of the
                range to query over.

            end:
                A datetime.datetime-like object representing the end of the
                range to query over.

            aggregator:
                The function for merging multiple time series together. For
                example, if the "user_id" tag is not specified, this aggregator
                function is used to combine all heart rate time series into one
                time series. (Yes, this isn't very useful.)

                For queries that return only one time series, this parameter is
                not relevant.

                Valid values: "sum", "min", "max", "avg", "dev"

                See: http://opentsdb.net/docs/build/html/user_guide/query/aggregators.html

            downsampling:
                A relative time interval to "downsample". This isn't true
                downsampling; rather, if you specify a downsampling of "5m"
                (five minutes), OpenTSDB will split data into five minute
                intervals, and return one data point in the middle of each
                interval whose value is the average of all data points within
                that interval.

                Valid relative time values are strings of the following format:

                    "<amount><time_unit>"

                Valid time units: "ms", "s", "m", "h", "d", "w", "n", "y"

                Date and time format: http://opentsdb.net/docs/build/html/user_guide/query/dates.html

            ms_resolution:
                Whether or not to output data point timestamps in milliseconds
                or seconds. If this flag is false and there are multiple
                data points within a second, those data points will be down
                sampled using the query's aggregation function.

        Returns:
            A dict mapping timestamps to data points
        """
        query = "{aggregator}:{downsample}{metric}{{{tags}}}".format(
            aggregator=aggregator,
            downsample=downsample + "-avg:" if downsample else "",
            metric=metric,
            tags=','.join("%s=%s" % (k, v) for k, v in tags.items())
        )
        params = {
            'ms': ms_resolution,
            'start': '{0:.3f}'.format(start.timestamp()),
            'end': '{0:.3f}'.format(end.timestamp()),
            'm': query
        }
        response = self.__request("/query", params)

        if response.status_code == 200:
            try:
                return response.json()[0]['dps']
            except IndexError:
                # empty data set
                return {}

        raise QueryError(response.json())

    def fetch_sorted_metric(self, *args, **kwargs):
        """Fetch and sort time series data from OpenTSDB

        Takes the same parameters as `fetch_metric`, but returns a list of
        (timestamp, value) tuples sorted by timestamp.
        """
        return sorted(self.fetch_metric(*args, **kwargs).items(),
            key=lambda x: float(x[0]))

    def __valid(self):
       return self.__request("/version").status_code == 200

    def __request(self, path, params=None):
        try:
            return requests.get(self.url + path, params=params, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise TimeoutError()

def connect(*args, **kwargs):
    return Connection(*args, **kwargs)
