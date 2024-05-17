from typing import Annotated, Literal, Optional, Union
from .shared import API, APIResp
from pydantic import BaseModel, ConfigDict, Field, RootModel, model_validator
from ..message import Message
from ..event.message import PrivateSenderInfo, GroupSenderInfo, AnonymousInfo


@API("send_private_msg")
class SendPrivateMsgArgs(BaseModel):
    user_id: int
    message: Message
    auto_escape: Optional[bool] = None
    """
    默认值为 false

    消息内容是否作为纯文本发送（即不解析 CQ 码），只在 message 字段是字符串时有效
    """


@APIResp("send_private_msg")
class SendPrivateMsgResp(BaseModel):
    message_id: int


@API("send_group_msg")
class SendGroupMsgArgs(BaseModel):
    group_id: int
    message: Message
    auto_escape: Optional[bool] = None
    """
    默认值为 false

    消息内容是否作为纯文本发送（即不解析 CQ 码），只在 message 字段是字符串时有效
    """


@APIResp("send_group_msg")
class SendGroupMsgResp(BaseModel):
    message_id: int


@API("send_msg")
class SendMsgPrivateArgs(BaseModel):
    message_type: Optional[Literal["private", "group"]]
    user_id: Optional[int]
    group_id: Optional[int]
    message: Message
    auto_escape: Optional[bool] = None
    """
    默认值为 false

    消息内容是否作为纯文本发送（即不解析 CQ 码），只在 message 字段是字符串时有效
    """


class SendMsgPrivateArgs(BaseModel):
    message_type: Literal["private"]
    user_id: int
    message: Message
    auto_escape: Optional[bool] = None
    """
    默认值为 false

    消息内容是否作为纯文本发送（即不解析 CQ 码），只在 message 字段是字符串时有效
    """


class SendMsgGroupArgs(BaseModel):
    message_type: Literal["group"]
    group_id: int
    message: Message
    auto_escape: Optional[bool] = None
    """
    默认值为 false

    消息内容是否作为纯文本发送（即不解析 CQ 码），只在 message 字段是字符串时有效
    """


@API("send_msg")
class SendMsgArgs(RootModel):
    root: Annotated[Union[SendMsgPrivateArgs, SendMsgGroupArgs],
                    Field(..., discriminator="message_type")]


@APIResp("send_msg")
class SendMsgResp(BaseModel):
    message_id: int


@API("delete_msg")
class DeleteMsgArgs(BaseModel):
    message_id: int


@API("get_msg")
class GetMsgArgs(BaseModel):
    message_id: int


class GetMsgPrivateResp(BaseModel):
    time: int
    message_type: Literal["private"]
    message_id: int
    real_id: int
    sender: PrivateSenderInfo


class GetMsgGroupResp(BaseModel):
    time: int
    message_type: Literal["group"]
    message_id: int
    real_id: int
    sender: GroupSenderInfo


@APIResp("get_msg")
class GetMsgResp(RootModel):
    root: Annotated[Union[GetMsgPrivateResp, GetMsgGroupResp],
                    Field(..., discriminator="message_type")]


@API("get_forward_msg")
class GetForwardMsgArgs(BaseModel):
    id: str


@APIResp("get_forward_msg")
class GetForwardMsgResp(BaseModel):
    message: Message


@API("send_like")
class SendLikeArgs(BaseModel):
    user_id: int
    times: Optional[int] = None
    """
    默认值为 1

    赞的次数，每个好友每天最多 10 次
    """


@API("set_group_kick")
class SetGroupKickArgs(BaseModel):
    group_id: int
    user_id: int
    reject_add_request: Optional[bool] = None
    """
    默认值为 false

    拒绝此人的加群请求
    """


@API("set_group_ban")
class SetGroupBanArgs(BaseModel):
    group_id: int
    user_id: int
    duration: Optional[int] = None
    """
    默认值为 30 * 60

    禁言时长，单位秒，0 表示取消禁言
    """


@API("set_group_anonymous_ban")
class SetGroupAnonymousBanArgs(BaseModel):
    group_id: int
    anonymous: Optional[AnonymousInfo] = None
    anonymous_flag: Optional[str] = None
    duration: Optional[int] = None
    """
    默认值为 30 * 60

    禁言时长，单位秒，无法取消匿名用户禁言
    """

    @model_validator(mode="after")
    def checkFields(self):
        if self.anonymous is None and self.anonymous_flag is None:
            raise ValueError(
                "At least one field between anonymous and anonymous_flag should be set")
        return self


@API("set_group_whole_ban")
class SetGroupWholeBanArgs(BaseModel):
    group_id: int
    enable: Optional[bool] = None
    """
    默认值为 true

    是否禁言
    """


@API("set_group_admin")
class SetGroupAdminArgs(BaseModel):
    group_id: int
    user_id: int
    enable: Optional[bool] = None
    """
    默认值为 true

    true 为设置，false 为取消
    """


@API("set_group_anonymous")
class SetGroupAnonymousArgs(BaseModel):
    group_id: int
    enable: Optional[bool] = None
    """
    默认值为 true

    是否允许匿名聊天
    """


@API("set_group_card")
class SetGroupCardArgs(BaseModel):
    group_id: int
    user_id: str
    card: Optional[str] = None
    """
    默认值为空

    群名片内容，不填或空字符串表示删除群名片
    """


@API("set_group_name")
class SetGroupNameArgs(BaseModel):
    group_id: int
    group_name: str


@API("set_group_leave")
class SetGroupLeave(BaseModel):
    group_id: int
    is_dismiss: Optional[bool] = None
    """
    默认值为 false

    是否解散，如果登录号是群主，则仅在此项为 true 时能够解散
    """


@API("set_group_special_title")
class SetGroupSpecialTitleArgs(BaseModel):
    group_id: int
    user_id: int
    special_title: Optional[str] = None
    """
    默认值为空

    专属头衔，不填或空字符串表示删除专属头衔
    """
    duration: Optional[int] = None
    """
    默认值为 -1

    专属头衔有效期，单位秒，-1 表示永久，不过此项似乎没有效果，可能是只有某些特殊的时间长度有效，有待测试
    """


@API("set_friend_add_request")
class SetFriendAddRequestArgs(BaseModel):
    flag: str
    approve: Optional[bool] = None
    """
    默认值为 true

    是否同意请求
    """
    remark: Optional[str] = None
    """
    默认值为空

    添加后的好友备注（仅在同意时有效）
    """


@API("set_group_add_request")
class SetGroupAddRequestArgs(BaseModel):
    flag: str
    sub_type: Literal["add", "invite"]
    approve: Optional[bool] = None
    """
    默认值为 true

    是否同意请求／邀请
    """
    reason: Optional[str] = None
    """
    默认值为空

    拒绝理由（仅在拒绝时有效）
    """


@APIResp("get_login_info")
class GetLoginInfoResp(BaseModel):
    user_id: int
    nickname: str


@API("get_stranger_info")
class GetStrangerInfoArgs(BaseModel):
    user_id: int
    no_cache: Optional[bool] = None
    """
    默认值为 false

    是否不使用缓存（使用缓存可能更新不及时，但响应更快）
    """


@APIResp("get_stranger_info")
class GetStrangerInfoResp(BaseModel):
    user_id: int
    nickname: str
    sex: Literal["male", "female", "unknown"]
    age: int


class FriendInfo(BaseModel):
    user_id: int
    nickname: str
    remark: str


@APIResp("get_friend_list")
class GetFriendListResp(RootModel):
    root: list[FriendInfo]


@API("get_group_info")
class GetGroupInfoArgs(BaseModel):
    group_id: int
    no_cache: Optional[bool] = None
    """
    默认值为 false

    是否不使用缓存（使用缓存可能更新不及时，但响应更快）
    """


class GroupInfo(BaseModel):
    group_id: int
    group_number: str
    member_count: int
    max_member_count: int


@APIResp("get_group_info")
class GetGroupInfoResp(GroupInfo):
    pass


@APIResp("get_group_list")
class GetGroupListResp(RootModel):
    root: list[GroupInfo]


@API("get_group_member_info")
class GetGroupMemberInfoArgs(BaseModel):
    group_id: int
    user_id: int
    no_cache: Optional[bool] = None
    """
    默认值为 false

    是否不使用缓存（使用缓存可能更新不及时，但响应更快）
    """


class GroupMemberInfo(BaseModel):
    group_id: int
    user_id: int
    nickname: str
    card: str
    sex: Literal["male", "female", "unknown"]
    age: int
    area: str
    join_time: int
    last_sent_time: int
    level: str
    role: Literal["owner", "admin", "member"]
    unfriendly: bool
    title: str
    title_expire_time: int
    card_changable: bool


@APIResp("get_group_member_info")
class GetGroupMemberInfoResp(GroupMemberInfo):
    pass


@API("get_group_member_list")
class GetGroupMemberListArgs(BaseModel):
    group_id: int


@APIResp("get_group_member_list")
class GetGroupMemberListResp(RootModel):
    root: list[GroupMemberInfo]


@API("get_group_honor_info")
class GetGroupHonorInfoArgs(BaseModel):
    group_id: int
    type: Literal["talkative", "performer",
                  "legend", "strong_newbie", "emotion", "all"]


class CurrentTalkativeInfo(BaseModel):
    user_id: int
    nickname: str
    avatar: str
    day_count: int


class HonorUserInfo(BaseModel):
    user_id: int
    nickname: str
    avatar: str
    description: str


@APIResp("get_group_honor_info")
class GetGroupHonorInfoResp(BaseModel):
    group_id: int
    current_talkative: Optional[CurrentTalkativeInfo]
    talkative_list: Optional[list[HonorUserInfo]]
    performer_list: Optional[list[HonorUserInfo]]
    legend_list: Optional[list[HonorUserInfo]]
    strong_newbie_list: Optional[list[HonorUserInfo]]
    emotion_list: Optional[list[HonorUserInfo]]


@API("get_cookies")
class GetCookiesArgs(BaseModel):
    domain: Optional[str] = None
    """
    默认值为空

    需要获取 cookies 的域名
    """


@APIResp("get_cookies")
class GetCookiesResp(BaseModel):
    cookies: str


@APIResp("get_csrf_token")
class GetCSRFTokenResp(BaseModel):
    token: int


@API("get_credentials")
class GetCredentialsArgs(BaseModel):
    domain: Optional[str] = None
    """
    默认值为空

    需要获取 cookies 的域名
    """


@APIResp("get_credentials")
class GetCredentialsResp(BaseModel):
    cookies: str
    token: int


@API("get_record")
class GetRecordArgs(BaseModel):
    file: str
    out_format: Literal["mp3", "amr", "wma",
                        "m4a", "spx", "ogg", "wav", "flac"]


@APIResp("get_record")
class GetRecordResp(BaseModel):
    file: str


@API("get_image")
class GetImageArgs(BaseModel):
    file: str


@APIResp("get_image")
class GetImageResp(BaseModel):
    file: str


@APIResp("can_send_image")
class CanSendImageResp(BaseModel):
    yes: bool


@APIResp("can_send_record")
class CanSendRecordResp(BaseModel):
    yes: bool


class Status(BaseModel):
    model_config = ConfigDict(extra="allow")

    online: bool
    good: bool


@APIResp("get_status")
class GetStatusResp(Status):
    pass


@APIResp("get_version_info")
class GetVersionInfoResp(BaseModel):
    model_config = ConfigDict(extra="allow")

    app_name: str
    app_version: str
    protocol_version: str


@API("set_restart")
class SetRestartArgs(BaseModel):
    delay: Optional[int] = None
    """
    默认值为 0

    要延迟的毫秒数，如果默认情况下无法重启，可以尝试设置延迟为 2000 左右
    """

# clean_cache 无参无响应数据
