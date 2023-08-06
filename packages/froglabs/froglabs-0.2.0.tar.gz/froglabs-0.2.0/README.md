# Froglabs Client Library

[![CircleCI](https://circleci.com/gh/froglabs/froglabs.svg?style=svg&circle-token=30c7634c62f6c9ef50db3329c87b07b600267e6b)](https://circleci.com/gh/froglabs/froglabs)

This package provides the froglabs cli and python library for requestion weather data and training weather data based models.

### Installing

Clone the repository if you do not have it already:

```bash
$ pip install froglabs
```

Froglabs supports Python 3.4 and newer.

## Weather Service

Request Black Sea Mean Wave Direction for 2018-01-01 to 2018-01-02:

```bash
$ froglabs query result.nc "Black Sea" mean_wave_direction 2018-01-01 2018-01-02
```

Dates are in UTC with no timezone, following ISO 8601. The timezone used is the local to the server.
Only certain variables are available at certain dates. For instance "sst" is currently only available for prediction (future dates).
For more information on variables availability please run:

```bash
$ froglabs get_variables
```

To see which variables are available for analysis and forecast, just take a look to the sanity preserver:

http://api.froglabs.ai/sanity_preserver

Request Black Sea surface temperature and salinity between tomorrow and the day after tomorrow:

```bash
$ froglabs query result.nc "Black Sea" sst,sss 
```

Now plot the result:

```bash
$ froglabs plot result.nc output.png sst
```

You can also plot on a map (install `cartopy` with `pip install cartopy` or `sudo apt-get install python3-cartopy`):

```bash
$ froglabs plot result.nc output.png mwd --projection=PlateCarree
$ froglabs plot result.nc output.png mwd --draw-gridlines=true --central-latitude=45 --projection=Orthographic
```
