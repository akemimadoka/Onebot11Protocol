from typing import Annotated, Literal, Optional, Union
from pydantic import BaseModel, Field
from ..message import Message
from .base import EventBase, QuickOperation, Event


@Event("message", "message_type")
class MessageEventBase(EventBase):
    pass


class PrivateSenderInfo(BaseModel):
    user_id: Optional[int] = None
    nickname: Optional[str] = None
    sex: Optional[Literal["male", "female", "unknown"]] = None
    age: Optional[int] = None


class PrivateMessageEvent(MessageEventBase):
    message_type: Literal["private"]
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
    user_id: Optional[int] = None
    nickname: Optional[str] = None
    card: Optional[str] = None
    sex: Optional[Literal["male", "female", "unknown"]] = None
    age: Optional[int] = None
    area: Optional[str] = None
    level: Optional[str] = None
    role: Optional[Literal["owner", "admin", "member"]] = None
    title: Optional[str] = None


class GroupMessageEvent(MessageEventBase):
    message_type: Literal["group"]
    sub_type: Literal["normal", "anonymous", "notice"]
    message_id: int
    group_id: int
    user_id: int
    anonymous: Optional[AnonymousInfo] = None
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
