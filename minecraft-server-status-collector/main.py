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
error_wait = int(config_strings[2])
empty_server_interval = int(config_strings[3])
non_empty_server_interval = int(config_strings[4])

while True:
    try:

        while True:

            while True:
                try:
                    server = MinecraftServer.lookup(server_address)
                    status = server.status()
                    break
                except:
                    print("Error while getting status!")
                    time.sleep(error_wait)

            player_uuids = []
            if status.players.sample is not None:
                player_uuids = [UUID(player.id) for player in status.players.sample]


            query = Query(
                timestamp=datetime.now(),
                address=server_address,
                latency=status.latency,
                description=str(status.description),
                players_count=status.players.online,
                players_max=status.players.max,
                players=player_uuids,
                version=status.version.name,
            )

            filename = os.path.expanduser(data_folder + query.timestamp_to_str() + ".json")
            with open(filename, "w+") as file:
                file.write(query.to_json())

            print("Written to file " + filename)

            if status.players.online > 0:
                time.sleep(non_empty_server_interval)
            else:
                time.sleep(empty_server_interval)

    except:
        print("Error!")
        time.sleep(error_wait)
