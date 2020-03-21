import time
from datetime import datetime

from mcstatus import MinecraftServer
from mongoengine import *

from models import Query
from uuid import UUID


with open("config.txt", "r") as config_file:
    config_string = config_file.read()
config_strings = config_string.split("\n")
mongo_db_name = config_strings[0]
server_address = config_strings[1]
empty_server_interval = int(config_strings[2])
non_empty_server_interval = int(config_strings[3])

connect(mongo_db_name)

while True:

    server = MinecraftServer.lookup(server_address)
    status = server.status()

    query = Query()
    query.timestamp = datetime.now()
    query.address = server_address
    query.latency = status.latency
    query.description = str(status.description)
    query.players_count = status.players.online
    query.players_max = status.players.max
    query.players = [UUID(player.id) for player in status.players.sample]
    query.version = status.version.name
    query.mods = [mod["modId"] for mod in status.raw["forgeData"]["mods"]]

    query.save()

    if status.players.online > 0:
        print("Non-empty")
        time.sleep(non_empty_server_interval)
    else:
        print("Empty")
        time.sleep(empty_server_interval)
