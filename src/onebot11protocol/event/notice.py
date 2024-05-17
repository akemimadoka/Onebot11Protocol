from typing import Annotated, Literal, Union
from .base import EventBase, Event
from pydantic import Field, BaseModel

@Event("notice", "notice_type")
class NoticeEventBase(EventBase):
    pass


class FileInfo(BaseModel):
    id: str
    name: str
    size: int
    busid: int


class GroupUploadNoticeEvent(NoticeEventBase):
    notice_type: Literal["group_upload"]
    group_id: int
    user_id: int
    file: FileInfo


class GroupAdminNoticeEvent(NoticeEventBase):
    notice_type: Literal["group_admin"]
    sub_type: Literal["set", "unset"]
    group_id: int
    user_id: int


class GroupDecreaseNoticeEvent(NoticeEventBase):
    notice_type: Literal["group_decrease"]
    sub_type: Literal["leave", "kick", "kick_me"]
    group_id: int
    operator_id: int
    user_id: int


class GroupIncreaseNoticeEvent(NoticeEventBase):
    notice_type: Literal["group_increase"]
    sub_type: Literal["approve", "invite"]
    group_id: int
    operator_id: int
    user_id: int


class GroupBanNoticeEvent(NoticeEventBase):
    notice_type: Literal["group_ban"]
    sub_type: Literal["ban", "lift_ban"]
    group_id: int
    operator_id: int
    user_id: int
    duration: int


class FriendAddNoticeEvent(NoticeEventBase):
    notice_type: Literal["friend_add"]
    user_id: int


class GroupRecallNoticeEvent(NoticeEventBase):
    notice_type: Literal["group_recall"]
    group_id: int
    user_id: int
    operator_id: int
    message_id: int


class FriendRecallNoticeEvent(NoticeEventBase):
    notice_type: Literal["friend_recall"]
    user_id: int
    message_id: int


class NotifyNoticeEventBase(NoticeEventBase):
    notice_type: Literal["notify"]


class PokeNotifyNoticeEvent(NotifyNoticeEventBase):
    sub_type: Literal["poke"]
    group_id: int
    user_id: int
    target_id: int


class LuckyKingNotifyNoticeEvent(NotifyNoticeEventBase):
    sub_type: Literal["lucky_king"]
    group_id: int
    user_id: int
    target_id: int


class HonorNotifyNoticeEvent(NotifyNoticeEventBase):
    sub_type: Literal["honor"]
    group_id: int
    honor_type: Literal["talkative", "performer", "emotion"]
    user_id: int


NotifyNoticeEvent = Annotated[Union[PokeNotifyNoticeEvent, LuckyKingNotifyNoticeEvent,
                                    HonorNotifyNoticeEvent], Field(..., discriminator="sub_type")]

NoticeEvent = Annotated[Union[GroupUploadNoticeEvent, GroupAdminNoticeEvent, GroupDecreaseNoticeEvent, GroupIncreaseNoticeEvent, GroupBanNoticeEvent,
                              FriendAddNoticeEvent, GroupRecallNoticeEvent, FriendRecallNoticeEvent, NotifyNoticeEvent], Field(..., discriminator="notice_type")]
