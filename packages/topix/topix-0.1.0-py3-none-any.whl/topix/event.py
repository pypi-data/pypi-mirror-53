"""The event class.

Events are JSON-compatible objects stored in Redis streams, to be consumed
by applications.

Any JSON object can be turned into an Event.
"""


from typing import Union, NamedTuple, Dict, List, Any
import json


class Event(NamedTuple):
    """An event sent through a Redis stream."""

    data: Union[Dict[str, Any], List[Any], None]
    ruid: Union[str, None] = None

    def __str__(self):
        return f"<Event ruid={str(self.ruid)}>"

    @classmethod
    def deserialize(
        cls, raw: Dict[bytes, bytes], ruid: Union[bytes, None] = None
    ) -> "Event":
        """Deserialize a raw dictionary to an event."""
        data = json.loads(raw[b"topix:event.data"].decode("utf-8"))
        if ruid:
            return cls(data, ruid=ruid.decode("utf-8"))
        return cls(data)

    def serialize(self) -> Dict[str, bytes]:
        """Serialize to a Redis Streams-compatible dictionary."""
        return {"topix:event.data": json.dumps(self.data).encode("utf-8")}
