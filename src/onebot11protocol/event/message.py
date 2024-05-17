from typing import Annotated, Literal, Optional, Union
from pydantic import BaseModel, Field
from ..message import Message
from .base import EventBase, QuickOperation, Event


@Event("message", "message_type")
class MessageEventBase(EventBase):
    pass


class PrivateSenderInfo(BaseModel):
    user_id: Optional[int]
    nickname: Optional[str]
    sex: Optional[Literal["male", "female", "unknown"]]
    age: Optional[int]


class PrivateMessageEvent(MessageEventBase):
    message_type: Literal["private"] = "private"
    sub_type: Literal["friend", "group", "other"]
    message_id: int
    user_id: int
    message: Message
    raw_message: str
    font: int
    sender: PrivateSenderInfo


@QuickOperation(PrivateMessageEvent)
class PrivateMessageEventQuickOperation(BaseModel):
    reply: Optional[Message] = None
    auto_escape: Optional[bool] = None


class AnonymousInfo(BaseModel):
    id: int
    name: str
    flag: str


class GroupSenderInfo(BaseModel):
    user_id: Optional[int]
    nickname: Optional[str]
    card: Optional[str]
    sex: Optional[Literal["male", "female", "unknown"]]
    age: Optional[int]
    area: Optional[str]
    level: Optional[str]
    role: Optional[Literal["owner", "admin", "member"]]
    title: Optional[str]


class GroupMessageEvent(MessageEventBase):
    message_type: Literal["group"]
    sub_type: Literal["normal", "anonymous", "notice"]
    message_id: int
    group_id: int
    user_id: int
    anonymous: Optional[AnonymousInfo]
    message: Message
    raw_message: str
    font: int
    sender: GroupSenderInfo


@QuickOperation(GroupMessageEvent)
class GroupMessageEventQuickOperation(BaseModel):
    reply: Optional[Message] = None
    auto_escape: Optional[bool] = None
    at_sender: Optional[bool] = None
    delete: Optional[bool] = None
    kick: Optional[bool] = None
    ban: Optional[bool] = None
    ban_duration: Optional[int] = None


MessageEvent = Annotated[Union[PrivateMessageEvent,
                               GroupMessageEvent], Field(..., discriminator="message_type")]
