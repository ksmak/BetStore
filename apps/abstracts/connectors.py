from typing import Optional, Any
from abc import ABC
import pickle

from redis import Redis


class AbstractConnector(ABC):
    "AbstractConnector."
    def __str__(self) -> str:
        return super().__str__()


class RedisConnector(AbstractConnector):
    """RedisConnector."""

    PICKLE_DEFAULT_PROTOCOL: int = 4
    DEFAULT_DB_VER: int = 0

    def __init__(
        self,
        db_ver: int = DEFAULT_DB_VER,
        protocol: int = PICKLE_DEFAULT_PROTOCOL
    ) -> None:
        self.db = Redis(db=db_ver)
        self.protocol = protocol

    def get(self, key: str) -> Optional[dict[str, Any]]:
        data: Any = self.db.get(key)
        if not data:
            return None
        return pickle.loads(data)

    def set(
        self,
        key: str,
        data: dict[str, Any],
        expire_time: int = 1 * 60 * 24
    ) -> None:
        pickled_obj: Any = pickle.dumps(
            data,
            protocol=self.protocol
        )
        # v1
        self.db.set(
            key,
            pickled_obj,
            expire_time
        )
        # v2
        # self.db.set(
        #     key,
        #     pickled_obj
        # )
        # self.db.expire(
        #     key,
        #     expire_time
        # )

    def delete(self, key: str):
        self.db.delete(key)
