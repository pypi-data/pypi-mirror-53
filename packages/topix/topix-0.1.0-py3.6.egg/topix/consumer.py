"""Consumer class for working on streams."""


import uuid
from typing import Union, List, Generator
from functools import wraps

from topix.topic import Topic
from topix.event import Event


def requires_setup(func):
    """Wraps methods that require setup."""

    @wraps(func)
    def wrapped(self, *args, **kwargs):
        if not self.is_setup:
            self.setup()
        return func(self, *args, **kwargs)

    return wrapped


class Consumer:
    """A consumer is a registered consumer of a stream, belonging to a group."""

    def __init__(
        self,
        stream: str,
        group: str,
        guid: str = None,
        topic: Union[Topic, None] = None,
    ):
        self.stream_name = stream
        self.group_name = group
        self.guid = guid if guid else str(uuid.uuid4())

        self.topic = topic if topic else Topic(self.stream_name)
        self.is_setup = False

    def setup(self):
        """Run setup methods for the consumer."""
        self.topic.create_group(self.group_name)
        self.is_setup = True

    @requires_setup
    def ack(self, event: Event):
        """Ack an event."""
        self.topic.ack(event, self.guid)

    @requires_setup
    def read(
        self, timeout: int = 0, seen: Union[str, int] = ">"
    ) -> Union[List[Event], None]:
        """Listen for new entries in the stream"""
        return self.topic.read(self.group_name, self.guid, timeout=timeout, seen=seen)

    @requires_setup
    def yield_from_stream(
        self, many=True
    ) -> Generator[Union[List[Event], Event], None, None]:
        """Yield groups of events (or single events) from the stream.

        Keyword Arguments:
            many: Whether to yield lists of events or single events. (default True)
        """
        events = self.read()
        if many:
            yield events
        else:
            for event in events:
                yield event
