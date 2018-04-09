from alpha_vantage.timeseries import TimeSeries
import time
import os
from datetime import datetime
from pytz import timezone
from influxdb import InfluxDBClient


STOCKS_TO_LOG="MSFT,GOOG"
APIKEY=os.environ["ALPHAVANTAGE_APIKEY"]
INFLUX_URL=os.environ["INFLUX_URL"]
INFLUX_USER=os.environ["INFLUX_USER"]
INFLUX_PASSWORD=os.environ["INFLUX_PASSWORD"]
INFLUX_DB=os.environ["INFLUX_DB"]


def savePointsToInflux(symbol, data, meta_data):
    points = []

    for timekey, datapoint in data.items():
        datatime = datetime.strptime(timekey, "%Y-%m-%d %H:%M:%S") 
        datatime = datatime.replace(tzinfo=timezone(meta_data["6. Time Zone"]))
        print(datatime, flush=True)
        point = {
            "measurement": "stocks",
            "tags": {
                "symbol": symbol,
            },
            "time": datatime.strftime('%Y-%m-%dT%H:%M:%SZ'),
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
            print("Getting data for {}".format(stock))
            data, meta_data = ts.get_intraday(symbol=stock, interval="1min")

            print(meta_data)
            print(data)

            savePointsToInflux(stock, data, meta_data)

            time.sleep(20)
