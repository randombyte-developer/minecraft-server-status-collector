import os
import time
from datetime import datetime

from mcstatus import MinecraftServer

from models import Query
from uuid import UUID

with open("config.txt", "r") as config_file:
    config_string = config_file.read()
config_strings = config_string.split("\n")
data_folder = config_strings[0]
server_address = config_strings[1]
empty_server_interval = int(config_strings[2])
non_empty_server_interval = int(config_strings[3])

while True:

    server = MinecraftServer.lookup(server_address)
    status = server.status()

    query = Query(
        timestamp=datetime.now(),
        address=server_address,
        latency=status.latency,
        description=str(status.description),
        players_count=status.players.online,
        players_max=status.players.max,
        players=[UUID(player.id) for player in status.players.sample],
        version=status.version.name,
        mods=[mod["modId"] for mod in status.raw["forgeData"]["mods"]],
    )

    filename = os.path.expanduser(data_folder + query.timestamp_to_str() + ".json")
    with open(filename, "w+") as file:
        file.write(query.to_json())

    print("Written to file " + filename)

    if status.players.online > 0:
        time.sleep(non_empty_server_interval)
    else:
        time.sleep(empty_server_interval)
