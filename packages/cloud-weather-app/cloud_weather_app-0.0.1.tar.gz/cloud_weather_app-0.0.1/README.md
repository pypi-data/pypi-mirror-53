# Weather Application 

A python package to get quick info of weather
For more info visit : https://gitlab.com/0xdebug/cloud-weather

## Get Started

### How to Install

Use the python package manager [pip](https://pip.pypa.io/en/stable/) to install cloud_weather_app.

```
pip install cloud_weather_app
```

### Requirements

- python >= 3.6
- requests
- beautifulsoup4

### Usage

```
from cloud_weather_app import cloud_weather

# Enter the valid Place Name
mumbai = cloud_weather('mumbai')

# Choose relevant forecast type and print variable to view outputs
daily = mumbai.daily()
monthly = mumbai.monthly()
hourly = mumbai.hourly()

```

### Sample Output
The Ouputs are just indicative and may subject to enhance in future versions

- Daily
```
Observed at : 2019-10-14 03:03:49
Temperature : 22°, Feels like : 22°, Desc : Thunder
```

- Monthly
```
--------------------------------------------------------------------------------

Date           Temp Day                      Temp Night
--------------------------------------------------------------------------------

2019-10-15     28°  PM T-Storms              21°  Scattered T-Storms
2019-10-16     27°  T-Storms                 20°  T-Storms
2019-10-17     28°  T-Storms                 20°  T-Storms
2019-10-18     28°  PM T-Storms              20°  Scattered T-Storms
2019-10-19     28°  PM T-Storms              20°  Scattered T-Storms
2019-10-20     28°  PM T-Storms              20°  T-Storms
2019-10-21     27°  PM T-Storms              20°  T-Storms
2019-10-22     27°  PM T-Storms              20°  T-Storms
2019-10-23     27°  T-Storms                 20°  T-Storms
2019-10-24     27°  T-Storms                 20°  T-Storms
2019-10-25     26°  T-Storms                 19°  Scattered T-Storms
2019-10-26     27°  PM T-Storms              19°  Scattered T-Storms
2019-10-27     27°  PM T-Storms              19°  T-Storms
2019-10-28     27°  Scattered T-Storms       19°  Scattered T-Storms
```

- Weekly
```
--------------------------------------------------------------------------------

Time           Description              Temp           Feels like
--------------------------------------------------------------------------------

04:00          Cloudy                   22°            22°
05:00          Scattered T-Storms       22°            22°
06:00          Cloudy                   22°            22°
07:00          Mostly Cloudy            21°            21°
08:00          Mostly Cloudy            22°            22°
09:00          Partly Cloudy            23°            23°
10:00          Partly Cloudy            25°            25°
11:30          Partly Cloudy            27°            30°
12:30          Partly Cloudy            28°            30°
13:30          Partly Cloudy            29°            30°
14:30          Partly Cloudy            29°            31°
15:30          Partly Cloudy            29°            31°
16:30          Partly Cloudy            28°            30°
17:30          Partly Cloudy            27°            29°
18:30          Partly Cloudy            26°            28°
```

### Author
Deepak Natanmai [gitlab.com/0xdebug](https://gitlab.com/0xdebug)