#!/usr/bin/python3

import envirophat
import json
import os
import time
from influxdb import InfluxDBClient

INFLUX_URL=os.environ["INFLUX_URL"]
INFLUX_USER=os.environ["INFLUX_USER"]
INFLUX_PASSWORD=os.environ["INFLUX_PASSWORD"]
INFLUX_DB=os.environ["INFLUX_DB"]


def saveTemperatureToInflux(temp):
    points = []

    point = {
        "measurement": "temperature",
        "tags": {
            "raspberry": "myRaspBerry",
        },
        "fields": {
            "temperature": float(temp),
        }
    }
    points.append(point)

    influxClient = InfluxDBClient(INFLUX_URL, 8086, INFLUX_USER, INFLUX_USER, INFLUX_DB)
    influxClient.write_points(points)

if __name__ == "__main__":
    while True:
        temp = envirophat.weather.temperature()
        saveTemperatureToInflux(temp)

        time.sleep(1)
        print("Wrote to influx: {}".format(temp))
