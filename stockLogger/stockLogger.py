from alpha_vantage.timeseries import TimeSeries
import time
import os
from datetime import datetime
import pytz
from influxdb import InfluxDBClient


STOCKS_TO_LOG="MSFT,GOOG"
APIKEY=os.environ["ALPHAVANTAGE_APIKEY"]
INFLUX_URL=os.environ["INFLUX_URL"]
INFLUX_USER=os.environ["INFLUX_USER"]
INFLUX_PASSWORD=os.environ["INFLUX_PASSWORD"]
INFLUX_DB=os.environ["INFLUX_DB"]

def vantageTimestampToUtc(timestamp, meta_data):
    parsedTimestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    tz = pytz.timezone(meta_data["6. Time Zone"])
    parsedTimestamp = tz.localize(parsedTimestamp)

    result = parsedTimestamp.astimezone(pytz.utc)
    return result

def savePointsToInflux(symbol, data, meta_data):
    points = []

    refresh_timestamp = vantageTimestampToUtc(meta_data["3. Last Refreshed"], meta_data)
    print("Last refreshed ({}): {}".format(symbol, refresh_timestamp), flush=True)

    for timekey, datapoint in data.items():
        utc_datatime = vantageTimestampToUtc(timekey, meta_data)
        point = {
            "measurement": "stocks",
            "tags": {
                "symbol": symbol,
            },
            "time": utc_datatime.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "open": float(datapoint["1. open"]),
                "high": float(datapoint["2. high"]),
                "low": float(datapoint["3. low"]),
                "close": float(datapoint["4. close"]),
                "volume": float(datapoint["5. volume"])
            }
        }
        points.append(point)
    
    influxClient = InfluxDBClient(INFLUX_URL, 8086, INFLUX_USER, INFLUX_USER, INFLUX_DB)
    influxClient.write_points(points)

if __name__ == "__main__":
    while True:
        ts = TimeSeries(key=APIKEY)
        for stock in STOCKS_TO_LOG.split(","):
            print("Getting data for {}".format(stock), flush=True)
            data, meta_data = ts.get_intraday(symbol=stock, interval="1min")

            savePointsToInflux(stock, data, meta_data)
            print("Data got for {}".format(stock), flush=True)

        time.sleep(20)
