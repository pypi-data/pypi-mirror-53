"""Mixins for Redis connectivity."""


from typing import Dict
from redis import Redis


class RedisMixin:
    """Mixin for giving Redis connectivity to an object."""

    _borg_url: Dict[str, str] = {"url": ""}
    _borg_connections: Dict[str, Redis] = {}

    def connect(self, url: str):
        """Set the redis URL for the borg."""
        self._borg_url["url"] = url

    @property
    def redis(self) -> Redis:
        """Get the Redis instance from the borg."""
        url = self._borg_url["url"]
        assert (
            url
        ), "Please call `.connect` on any instance to initialize the connection."
        client = self._borg_connections.get(url)

        if client is None:
            created = Redis.from_url(url)
            self._borg_connections[url] = created
            return created

        return client
