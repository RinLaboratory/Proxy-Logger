# Proxy-Logger

## Project Info

This project uses Python `v3.11.3`, MongoDB, Tkinter, hashlib, os, threading, re and datetime.

Until now `17-05-2024` all this packages are integrated within python.

## Install dependencies

Run `pip install pymongo httpx httpcore`

Make sure that u have `pymongo`, `httpx` and `httpcore` updated. otherwise it will throw a weird error saying they're incompatible with each other.

## How to run

As stated above, you need [python `v3.11.3`](https://www.python.org/downloads/release/python-3113/) installed.

Use `python logger.py` to run the app.

## What it does

### At this time this app doesnt support Bungeecord so don't try to import Bungeecord log files
This app is intented to create a simple activity viewer to Minecraft Velocity based proxys

You can get player activity by timestamp within a IP address and a username.
- If you search by IP address it will show all players binded to that IP, and the times they changed IP.
- If you search by username it will show all IP's binded to that player.

At the time this app only accepts `*.log` files and excludes `latest.log` as currently doesnt have a way to process an unfinished log file.

If you use [nLogin](https://en.docs.nickuc.com/) this will append the player activity related to that plugin, such as:

- Login events
- Register events

This is important within the logs as it marks when the actual player session starts

All the information thats returned its ordered by timestamp (date and hour) so no need to worry about importing order between outdated logs and most recent ones.