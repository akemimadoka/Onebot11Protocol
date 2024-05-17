from typing import Annotated, Literal, Optional, Union
from .base import Event, EventBase, QuickOperation
from pydantic import Field, BaseModel


@Event("request", "request_type")
class RequestEventBase(EventBase):
    pass


class FriendRequestEvent(RequestEventBase):
    request_type: Literal["friend"]
    user_id: int
    comment: str
    flag: str


@QuickOperation(FriendRequestEvent)
class FriendRequestEventQuickOperation(BaseModel):
    approve: Optional[bool] = None
    remark: Optional[str] = None


class GroupRequestEvent(RequestEventBase):
    request_type: Literal["group"]
    sub_type: Literal["add", "invite"]
    group_id: int
    user_id: int
    comment: str
    flag: str


@QuickOperation(GroupRequestEvent)
class GroupRequestEventQuickOperation(BaseModel):
    approve: Optional[bool] = None
    reason: Optional[str] = None


RequestEvent = Annotated[Union[FriendRequestEvent,
                               GroupRequestEvent], Field(..., discriminator="request_type")]
