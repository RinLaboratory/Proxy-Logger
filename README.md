# Proxy-Logger

## Project Info

This project uses Python `v3.11.3`, MongoDB, Tkinter, hashlib, os, threading, multiprocessing, re and datetime.

Until now `17-05-2024` all this packages are integrated within python.

Proxy-Logger uses the IP2Location LITE database for <a href="https://lite.ip2location.com">IP geolocation</a>.

## What it does

This app is intented to create a simple activity viewer to Minecraft based proxys

Currently supporting Velocity and Bungeecord based proxys.

You can get player activity by timestamp within a IP address and a username.
- If you search by IP address it will show all players binded to that IP, and the times they changed IP.
- If you search by username it will show all IP's binded to that player.

At the time this app only accepts `*.log` files.

If you use [nLogin](https://en.docs.nickuc.com/) this will append the player activity related to that plugin, such as:

- Login events
- Register events

This is important within the logs as it marks when the actual player session starts

All the information thats returned its ordered by timestamp (date and hour) so no need to worry about importing order between outdated logs and most recent ones. `latest.log` activity related will always show at the bottom.

## Install dependencies

Run `pip install pymongo httpx httpcore`

Make sure that u have `pymongo`, `httpx` and `httpcore` updated. otherwise it will throw a weird error saying they're incompatible with each other.

## Populate Country DB

from [ip2location website](https://lite.ip2location.com) download CSV database and put it inside the `./country_processing` folder and rename it as `IP2LOCATION-LITE-DB3.CSV`.
Run `python ./country_processing/populate_country_database.py` to populate the database with country data for fetching purposes within the app.
The app will fetch all ip addresses countries from that database.
All ip addresses that have `-` in the country variable means it doesnt currently exist in the ip2location db.

## Country names to iso2

### This option is only available when importing from Velocity proxies.
from [brenes github](https://gist.github.com/brenes/1095110#file-paises-csv) download `paises.csv` and put it inside the `./country_processing` folder and rename it as `spanish-countries.csv`.
if you have a Anti-VPN provider like [v4Guard](https://v4guard.io/) and in the disconnect message shows the country name this part will be useful. this function currently supports spanish and english country names.

## How to run

As stated above, you need [python `v3.11.3`](https://www.python.org/downloads/release/python-3113/) installed.

### I suggest closing very demanding apps when importing logs as it will use almost ALL of your computer resources.
(your total available threads in your core - 1)

Use `python logger.py` to run the app.

## How to identify a log
### From velocity:

Velocity logs look like this:
```
[18:21:38] [Netty epoll Worker #18/INFO] [com.velocitypowered.proxy.connection.client.AuthSessionHandler]: [connected player] RinLaboratory (/127.0.0.1:69420) has connected
[18:22:05] [Netty epoll Worker #18/INFO] [com.velocitypowered.proxy.connection.MinecraftConnection]: [server connection] RinLaboratory -> lobby has connected
[18:24:50] [Netty epoll Worker #18/INFO] [com.velocitypowered.proxy.connection.MinecraftConnection]: [connected player] RinLaboratory (127.0.0.1/127.0.0.1:69420) has disconnected
[18:24:50] [Netty epoll Worker #18/INFO] [com.velocitypowered.proxy.connection.MinecraftConnection]: [server connection] RinLaboratory -> lobby has disconnected
```

### From Bungeecord:

Bungeecord logs look like this:
```
[18:21:38] [Netty Worker IO Thread #2/INFO]: [RinLaboratory|/127.0.0.1:69420] <-> ServerConnector [auth] has connected
[18:22:05] [Netty Worker IO Thread #2/INFO]: [/127.0.0.1:69420|RinLaboratory] <-> DownstreamBridge <-> [auth] has disconnected
[18:24:50] [Netty Worker IO Thread #1/INFO]: [/127.0.0.1:69420|RinLaboratory] <-> DownstreamBridge <-> [lobby] has disconnected
[18:24:50] [Netty Worker IO Thread #10/INFO]: [/127.0.0.1:69420|RinLaboratory] -> UpstreamBridge has disconnected
```
