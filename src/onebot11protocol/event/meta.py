from typing import Annotated, Literal, Union
from .base import Event, EventBase
from pydantic import Field
from ..api.shared import Status


@Event("meta_event", "meta_event_type")
class MetaEventBase(EventBase):
    pass


class LifecycleEvent(MetaEventBase):
    meta_event_type: Literal["lifecycle"]
    sub_type: Literal["enable", "disable", "connect"]


class HeartbeatEvent(MetaEventBase):
    meta_event_type: Literal["heartbeat"]
    status: Status
    interval: int


MetaEvent = Annotated[Union[LifecycleEvent, HeartbeatEvent],
                      Field(..., discriminator="meta_event_type")]
