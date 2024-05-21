# Proxy-Logger

## Project Info

This project uses Python `v3.11.3`, MongoDB, Tkinter, hashlib, os, threading, multiprocessing, re and datetime.

Until now `17-05-2024` all this packages are integrated within python.

## What it does

This app is intented to create a simple activity viewer to Minecraft based proxys

Currently supporting Velocity and Bungeecord based proxys.

You can get player activity by timestamp within a IP address and a username.
- If you search by IP address it will show all players binded to that IP, and the times they changed IP.
- If you search by username it will show all IP's binded to that player.

At the time this app only accepts `*.log` files and excludes `latest.log` as currently doesnt have a way to process an unfinished log file.

If you use [nLogin](https://en.docs.nickuc.com/) this will append the player activity related to that plugin, such as:

- Login events
- Register events

This is important within the logs as it marks when the actual player session starts

All the information thats returned its ordered by timestamp (date and hour) so no need to worry about importing order between outdated logs and most recent ones.

## Install dependencies

Run `pip install pymongo httpx httpcore`

Make sure that u have `pymongo`, `httpx` and `httpcore` updated. otherwise it will throw a weird error saying they're incompatible with each other.

## How to run

As stated above, you need [python `v3.11.3`](https://www.python.org/downloads/release/python-3113/) installed.

### I suggest closing very demanding apps when importing logs as it will use almost ALL of your computer resources.
(your total available threads in your core - 1)

Use `python logger.py` to run the app.

## How to identify a log
### From velocity:

Velocity logs look like this:
```
[18:21:38] [Netty epoll Worker #18/INFO] [com.velocitypowered.proxy.connection.client.AuthSessionHandler]: [connected player] TheCreeperZenior (/127.0.0.1:69420) has connected
[18:22:05] [Netty epoll Worker #18/INFO] [com.velocitypowered.proxy.connection.MinecraftConnection]: [server connection] TheCreeperZenior -> lobby has connected
[18:24:50] [Netty epoll Worker #18/INFO] [com.velocitypowered.proxy.connection.MinecraftConnection]: [connected player] TheCreeperZenior (127.0.0.1/127.0.0.1:69420) has disconnected
[18:24:50] [Netty epoll Worker #18/INFO] [com.velocitypowered.proxy.connection.MinecraftConnection]: [server connection] TheCreeperZenior -> lobby has disconnected
```

### From Bungeecord:

Bungeecord logs look like this:
```
[18:21:38] [Netty Worker IO Thread #2/INFO]: [TheCreeperZenior|/127.0.0.1:69420] <-> ServerConnector [auth] has connected
[18:22:05] [Netty Worker IO Thread #2/INFO]: [/127.0.0.1:69420|TheCreeperZenior] <-> DownstreamBridge <-> [auth] has disconnected
[18:24:50] [Netty Worker IO Thread #1/INFO]: [/127.0.0.1:69420|TheCreeperZenior] <-> DownstreamBridge <-> [lobby] has disconnected
[18:24:50] [Netty Worker IO Thread #10/INFO]: [/127.0.0.1:69420|TheCreeperZenior] -> UpstreamBridge has disconnected
```