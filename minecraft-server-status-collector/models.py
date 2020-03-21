import json
from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

datetime_format = "%Y-%m-%d-%H-%M-%S"


@dataclass
class Query:
    timestamp: datetime
    address: str
    latency: float
    version: str
    description: str
    players_count: int
    players_max: int
    players: List[UUID]

    def timestamp_to_str(self) -> str:
        return self.timestamp.strftime(datetime_format)

    def to_json(self) -> str:
        return json.dumps({
            "t": self.timestamp_to_str(),
            "a": self.address,
            "l": self.latency,
            "v": self.version,
            "d": self.description,
            "pc": self.players_count,
            "pm": self.players_max,
            "p": [str(uuid) for uuid in self.players],
        })
