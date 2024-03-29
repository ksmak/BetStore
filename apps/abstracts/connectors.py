import os
from typing import Optional, Any
from abc import ABC, abstractmethod
import pickle
import json

from django.conf import settings

from redis import Redis


class BaseConnector(ABC):
    "BaseConnector."

    @abstractmethod
    def get(self, key: str) -> Optional[dict[str, Any]]:
        pass

    @abstractmethod
    def set(self, key: str, value: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass


class RedisConnector(BaseConnector):
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
        value: Optional[dict[str, Any]] = self.db.get(key)
        if not value:
            return None
        return pickle.loads(value)

    def set(
        self,
        key: str,
        value: dict[str, Any]
    ) -> None:
        pickled_obj: Any = pickle.dumps(
            value,
            protocol=self.protocol
        )
        self.db.set(
            key,
            pickled_obj
        )

    def set_ex(
        self,
        key: str,
        value: dict[str, Any],
        expire_time: int = 1 * 60 * 24
    ) -> None:
        pickled_obj: Any = pickle.dumps(
            value,
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

    def delete(self, key: str) -> None:
        self.db.delete(key)


class FileConnector(BaseConnector):
    """FileConnector."""

    def __init__(
        self,
        path: str = settings.BASE_DIR,
    ) -> None:
        self.path = path

    def get(self, key: str) -> Optional[dict[str, Any]]:
        value: Optional[dict[str, Any]] = None
        file_name: str = os.path.join(self.path, key + '.pickle')
        try:
            if os.path.exists(file_name):
                with open(file_name, 'rb') as f:
                    value = pickle.load(f)
        except Exception as e:
            print(e)
            return None

        return value

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        file_name: str = os.path.join(self.path, key + '.pickle')
        try:
            with open(file_name, 'wb') as f:
                pickle.dump(value, f)
        except Exception as e:
            print(e)
            return

    def delete(self, key: str) -> None:
        file_name: str = os.path.join(self.path, key + '.pickle')
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
        except Exception as e:
            print(e)
            return


class TextConnector(BaseConnector):
    """TextConnector."""

    def __init__(
        self,
        path: str = settings.BASE_DIR,
    ) -> None:
        self.path = path

    def get(self, key: str) -> Any:
        file_name: str = os.path.join(self.path, key + '.txt')
        value: Any = None
        try:
            if os.path.exists(file_name):
                with open(file_name, 'r') as f:
                    value: dict[str, Any] = json.loads(f.read())
        except Exception as e:
            print(e)
            return None

        return value

    def set(
        self,
        key: str,
        value: dict[str, Any],
    ) -> None:
        file_name: str = os.path.join(self.path, key + '.txt')
        try:
            with open(file_name, 'w') as f:
                f.write(json.dumps(value))
        except Exception as e:
            print(e)
            return

    def delete(self, key: str) -> None:
        file_name: str = os.path.join(self.path, key + '.txt')
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
        except Exception as e:
            print(e)
            return
