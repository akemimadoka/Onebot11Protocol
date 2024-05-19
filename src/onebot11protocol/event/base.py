from typing import ChainMap, Literal
from pydantic import BaseModel


class EventBase(BaseModel):
    time: int
    self_id: int


EventDiscriminatorMap: dict[str, str] = {}
"""post_type -> EventDiscriminator"""

EventQuickOperationMap: dict[type, type] = {}
"""Event -> QuickOperation"""

MessageTypeQuickOperationMap: dict[str, dict[str, type]] = {}
"""post_type -> DiscriminatorValue -> QuickOperation"""


def Event(postType: str, discriminatorName: str):
    def decorator(event: type):
        EventDiscriminatorMap[postType] = discriminatorName
        event.__annotations__["post_type"] = Literal[postType]
        event.post_type = postType
        return event
    return decorator


def QuickOperation(event: type):
    def decorator(quickOperation: type):
        EventQuickOperationMap[event] = quickOperation
        allAnnotations = ChainMap(
            *(c.__annotations__ for c in event.__mro__ if "__annotations__" in c.__dict__))
        postType = allAnnotations["post_type"].__args__[0]
        discriminator = EventDiscriminatorMap[postType]
        messageType: str = allAnnotations[discriminator].__args__[0]
        if postType not in MessageTypeQuickOperationMap:
            discriminatorQuickOperationMap = MessageTypeQuickOperationMap[postType] = {
            }
        else:
            discriminatorQuickOperationMap = MessageTypeQuickOperationMap[postType]
        discriminatorQuickOperationMap[messageType] = quickOperation

        return quickOperation
    return decorator
