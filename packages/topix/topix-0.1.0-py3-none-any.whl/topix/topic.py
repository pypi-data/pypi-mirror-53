"""A Topic is a specific Redis Stream that holds Events."""


from typing import Union, Dict, List, Any
import logging

import redis

from topix.mixins import RedisMixin
from topix.event import Event


LOG = logging.getLogger(__name__)


class Topic(RedisMixin):
    """A Topic is analagous to a Redis `stream` with an easy to use Python interface.

    Usage:
    >>> topic = Topic("incoming_webhooks")
    >>> topic.add({"user": 18, "action": "create_order"})

    Often times, you'll want to use a Topic alongside a consumer class.
    """

    def __init__(self, name: str):
        self.name = name

    def add(self, event: Union[Dict[str, Any], List[Any], Event]) -> bytes:
        """Add an event to the event stream."""
        # Duck type check for event classes.
        try:
            data = event.serialize()  # type: ignore
        except AttributeError:
            data = Event(event).serialize()  # type: ignore
        return self.redis.xadd(self.name, data)

    def create_group(self, group: str):
        """Idempotently create a consumer group.

        If the group already exists, simply pass.
        """
        try:
            self.redis.xgroup_create(self.name, group, mkstream=True)
        except redis.exceptions.ResponseError:
            LOG.debug(f"Consumer group {group} for {self.name} already exists")

    def read(
        self, group: str, consumer: str, timeout=0, seen=">"
    ) -> Union[List[Event], None]:
        """Read latest events from the stream for a given consumer group.

        Arguments:
            group: The name of the group.
            consumer: Consumer ID as a string.
        Keyword Arguments:
            timeout: The timeout in milliseconds, or 0 for "block"
            seen: The last ID seen OR the string ">" for "latest".
        """
        LOG.debug(f"Reading latest messages from {self.name} for {group}.{consumer}")
        data = self.redis.xreadgroup(group, consumer, {self.name: seen}, block=timeout)
        # If it's blank or empty, let the caller wait again with a clear signal.
        if not data:
            return None

        # We already know the stream. Discard it.
        _, keyvals = data[0]
        return [Event.deserialize(event, ruid) for (ruid, event) in keyvals]

    def ack(self, event: Event, consumer: str):
        """Acknowledge the success of a given event.

        Arguments:
            event: An Event.
            consumer: ID of the acking consumer.
        """
        assert event.ruid, "Event has no .ruid, was it deserialized?"
        LOG.debug(f"Consumer {consumer} acks {event}")
        self.redis.xack(self.name, consumer, event.ruid)
