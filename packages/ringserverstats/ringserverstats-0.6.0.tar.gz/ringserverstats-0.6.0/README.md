# ringserverstats

Parse ringserver reports, compute statistics and store in influxdb.

![ringserver activity](https://github.com/resif/ringserver-stats/raw/master/images/2019-02-25_09-30.png)

![ringserver statistics by day](https://github.com/resif/ringserver-stats/raw/master/images/2019-02-25_09-30_1.png)

![ringserver statistics by month](https://github.com/resif/ringserver-stats/raw/master/images/2019-02-25_09-31.png)

## Installation

ringserverstats is distributed on PyPI https://pypi.org as a universal wheel.

``` bash
    $ pip install ringserverstats
```

## Influxdb configuration

This program will fill 2 measurements. You should configure a database for these, and configure a user with write priviledges.

### Prepare database

First, create a database, a user, and retention policie.

``` sql
create database ringserverdb
create user ringserver with password 'ringserverer'
grant write on ringserverdb to ringserver
grant read on ringserverdb to ringserver
create retention policy rp_ringserverevents on ringserver duration 1w replication 1
create retention policy rp_ringserverstats on ringserver duration 520w replication 1
```

## Usage

To work properly, this program needs the following environment variables set :

  * `INFLUXDB_HOST` : The host name or adress of influxdb server
  * `INFLUXDB_PORT` : The port number of influxdb server
  * `INFLUXDB_USER` : The influxdb user to authenticate to
  * `INFLUXDB_PASS` : The password to authenticate with
  * `INFLUXDB_DB`   : The database name containing the metric
  * `INFLUXDB_VERIFY_SSL` : Set to `yes` or `no` to verify SSL connection
  * `INFLUXDB_SSL`  : Should the connection go to https ?

``` bash
$ ringserstats txlogs.log
```

## Explanations

The TX logs from ringserver are metrics suitable for a timeserie database. The idea is to parse the logs, as in the exemple below, and to generate values to insert into an influxdb timeseries database.

The file `grafana-dashboard.json` can be imported into grafana to visualize this timeserie.

Used tags in influxdb :

``` sql
show tag keys from ringserverevents
show tag keys from ringserverstats
```

### Events

The ringserverevents measure has several tags :

  * network, station, location, channel : which data was requested
  * geohash : location of the client in geohash format
  * hosthash : a hash of the client ip (usefull to correlate the clients requests)
  * city : an english city name

### Grouping and downsampling
Because storing events in the longterm is not very relevant, the `ringserverstats` measurement groups all events by day, by host, by network, station, location and channel.
The retention policies discribed above will manage the time your data get stored in influxdb.

To achieve downsampling, we use influxdb's continuous query. This is an exemple of creating the continuous query :

``` sql
create continuous query "cq_ringserverstats_by_day" on resif
  resample for 3d
  begin
    select sum("bytes") as bytes into "rp_ringserverstats"."ringserverstats" from "rp_ringserverevents"."ringserverevents" group by
      time(1d),network,station,location,channel,city,hosthash,geohash
  end
```

This query is executed every day (from the `group by time(1d)` instruction) and will resample 3 days in the past (instruction `resample for 3 d`), genrating 3 entries (one per day). Existing entries are overwritten.

Documentation of influxdb's continuous queries is here : https://docs.influxdata.com/influxdb/v1.7/query_language/continuous_queries/

## License

`ringserverstats` is distributed under the terms of the GPL v3 or later. See LICENSE file.

## Build

``` shell
python3 setup.py sdist bdist_wheel
```

## Test

``` shell
tox
```
