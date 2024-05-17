from typing import Annotated, Union

from .base import MessageTypeQuickOperationMap, EventDiscriminatorMap
from .message import MessageEvent
from .notice import NoticeEvent
from .request import RequestEvent
from .meta import MetaEvent

from pydantic import Field, Tag

Event = Annotated[Union[MessageEvent, NoticeEvent, RequestEvent,
                        MetaEvent], Field(..., discriminator="post_type")]

QuickOperationsUnion = Union[tuple(
    quickOperation for discriminatorQuickOperationMap in MessageTypeQuickOperationMap.values() for quickOperation in discriminatorQuickOperationMap.values())]

QuickOperationsAnnotatedUnion = Union[tuple(Annotated[quickOperation, Tag(
    f"{postType}.{discriminatorValue}")] for postType, discriminatorQuickOperationMap in MessageTypeQuickOperationMap.items() for discriminatorValue, quickOperation in discriminatorQuickOperationMap.items())]
