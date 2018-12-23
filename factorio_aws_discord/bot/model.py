import pickle
from dataclasses import dataclass
from typing import Optional, Callable, Union


@dataclass
class Chat:
    chat_id: int
    chat_name: str
    guild_id: int


@dataclass
class World:
    wid: str
    ec2_instance_id: str
    bucket_url: str
    aws_region: str
    chat: Chat


# Doing in-memory database because we expect data to rarely change
class WorldsTable:
    def __init__(self, writer: Callable[[bytes], None], initial: Union[bytes, dict]):
        self._worlds = pickle.loads(initial) if isinstance(initial, bytes) else (initial or {})
        self._flush = writer

    def flush(self):
        payload = pickle.dumps(self._worlds, pickle.HIGHEST_PROTOCOL)
        self._flush(payload)

    def upsert(self, world: World) -> bool:
        exists = world.wid in self._worlds
        self._worlds[world.wid] = world
        self.flush()
        return not exists

    def delete(self, wid: str) -> bool:
        try:
            del self._worlds[wid]
        except KeyError:
            return False
        self.flush()
        return True

    def find_one_by(self, wid=None, ec2_instance_id=None, chat_id=None) -> Optional[World]:
        if wid is None:
            if ec2_instance_id is None and chat_id is None:
                raise ValueError
            else:
                iterable = self._worlds.values()
        else:
            world = self._worlds.get(wid)
            if ec2_instance_id is None and chat_id is None:
                return world
            elif world is None:
                return None
            else:
                iterable = (world,)

        for world in iterable:
            data = ((world.ec2_instance_id, ec2_instance_id),
                    (world.chat.chat_id, chat_id))
            if all(search is None or search == item for item, search in data):
                return world
