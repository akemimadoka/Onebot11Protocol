from typing import Annotated, Literal, Optional, Union
from .shared import APIRequest, EmptyResp, Status
from pydantic import BaseModel, ConfigDict, Field, RootModel, model_validator
from ..message import Message
from ..event.message import PrivateSenderInfo, GroupSenderInfo, AnonymousInfo


class SendPrivateMsgResp(BaseModel):
    message_id: int


class SendPrivateMsgReq(APIRequest[Literal["send_private_msg"], SendPrivateMsgResp]):
    user_id: int
    message: Message
    auto_escape: Optional[bool] = None
    """
    默认值为 false

    消息内容是否作为纯文本发送（即不解析 CQ 码），只在 message 字段是字符串时有效
    """


class SendGroupMsgResp(BaseModel):
    message_id: int


class SendGroupMsgReq(APIRequest[Literal["send_group_msg"], SendGroupMsgResp]):
    group_id: int
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


class SendMsgResp(BaseModel):
    message_id: int


class SendMsgArgs(APIRequest[Literal["send_msg"], SendMsgResp], RootModel):
    root: Annotated[Union[SendMsgPrivateArgs, SendMsgGroupArgs],
                    Field(..., discriminator="message_type")]


class DeleteMsgReq(APIRequest[Literal["delete_msg"], EmptyResp]):
    message_id: int


class GetMsgPrivateResp(BaseModel):
    time: int
    message_type: Literal["private"]
    message_id: int
    real_id: int
    sender: PrivateSenderInfo
    message: Message


class GetMsgGroupResp(BaseModel):
    time: int
    message_type: Literal["group"]
    message_id: int
    real_id: int
    sender: GroupSenderInfo
    message: Message


class GetMsgResp(RootModel):
    root: Annotated[Union[GetMsgPrivateResp, GetMsgGroupResp],
                    Field(..., discriminator="message_type")]


class GetMsgReq(APIRequest[Literal["get_msg"], GetMsgResp]):
    message_id: int


class GetForwardMsgResp(BaseModel):
    message: Message


class GetForwardMsgReq(APIRequest[Literal["get_forward_msg"], GetForwardMsgResp]):
    id: str


class SendLikeReq(APIRequest[Literal["send_like"], EmptyResp]):
    user_id: int
    times: Optional[int] = None
    """
    默认值为 1

    赞的次数，每个好友每天最多 10 次
    """


class SetGroupKickReq(APIRequest[Literal["set_group_kick"], EmptyResp]):
    group_id: int
    user_id: int
    reject_add_request: Optional[bool] = None
    """
    默认值为 false

    拒绝此人的加群请求
    """


class SetGroupBanReq(APIRequest[Literal["set_group_ban"], EmptyResp]):
    group_id: int
    user_id: int
    duration: Optional[int] = None
    """
    默认值为 30 * 60

    禁言时长，单位秒，0 表示取消禁言
    """


class SetGroupAnonymousBanReq(APIRequest[Literal["set_group_anonymous_ban"], EmptyResp]):
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


class SetGroupWholeBanReq(APIRequest[Literal["set_group_whole_ban"], EmptyResp]):
    group_id: int
    enable: Optional[bool] = None
    """
    默认值为 true

    是否禁言
    """


class SetGroupAdminReq(APIRequest[Literal["set_group_admin"], EmptyResp]):
    group_id: int
    user_id: int
    enable: Optional[bool] = None
    """
    默认值为 true

    true 为设置，false 为取消
    """


class SetGroupAnonymousReq(APIRequest[Literal["set_group_anonymous"], EmptyResp]):
    group_id: int
    enable: Optional[bool] = None
    """
    默认值为 true

    是否允许匿名聊天
    """


class SetGroupCardReq(APIRequest[Literal["set_group_card"], EmptyResp]):
    group_id: int
    user_id: str
    card: Optional[str] = None
    """
    默认值为空

    群名片内容，不填或空字符串表示删除群名片
    """


class SetGroupNameReq(APIRequest[Literal["set_group_name"], EmptyResp]):
    group_id: int
    group_name: str


class SetGroupLeaveReq(APIRequest[Literal["set_group_leave"], EmptyResp]):
    group_id: int
    is_dismiss: Optional[bool] = None
    """
    默认值为 false

    是否解散，如果登录号是群主，则仅在此项为 true 时能够解散
    """


class SetGroupSpecialTitleReq(APIRequest[Literal["set_group_special_title"], EmptyResp]):
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


class SetFriendAddRequestReq(APIRequest[Literal["set_friend_add_request"], EmptyResp]):
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


class SetGroupAddRequestReq(APIRequest[Literal["set_group_add_request"], EmptyResp]):
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


class GetLoginInfoResp(BaseModel):
    user_id: int
    nickname: str


class GetLoginInfoReq(APIRequest[Literal["get_login_info"], GetLoginInfoResp]):
    pass


class GetStrangerInfoResp(BaseModel):
    user_id: int
    nickname: str
    sex: Literal["male", "female", "unknown"]
    age: int


class GetStrangerInfoReq(APIRequest[Literal["get_stranger_info"], GetStrangerInfoResp]):
    user_id: int
    no_cache: Optional[bool] = None
    """
    默认值为 false

    是否不使用缓存（使用缓存可能更新不及时，但响应更快）
    """


class FriendInfo(BaseModel):
    user_id: int
    nickname: str
    remark: str


class GetFriendListResp(RootModel):
    root: list[FriendInfo]


class GetFriendListReq(APIRequest[Literal["get_friend_list"], GetFriendListResp]):
    pass


class GroupInfo(BaseModel):
    group_id: int
    group_number: str
    member_count: int
    max_member_count: int


class GetGroupInfoResp(GroupInfo):
    pass


class GetGroupInfoReq(APIRequest[Literal["get_group_info"], GetGroupInfoResp]):
    group_id: int
    no_cache: Optional[bool] = None
    """
    默认值为 false

    是否不使用缓存（使用缓存可能更新不及时，但响应更快）
    """


class GetGroupListResp(RootModel):
    root: list[GroupInfo]


class GetGroupListReq(APIRequest[Literal["get_group_list"], GetGroupListResp]):
    pass


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


class GetGroupMemberInfoResp(GroupMemberInfo):
    pass


class GetGroupMemberInfoReq(APIRequest[Literal["get_group_member_info"], GetGroupMemberInfoResp]):
    group_id: int
    user_id: int
    no_cache: Optional[bool] = None
    """
    默认值为 false

    是否不使用缓存（使用缓存可能更新不及时，但响应更快）
    """


class GetGroupMemberListResp(RootModel):
    root: list[GroupMemberInfo]


class GetGroupMemberListReq(APIRequest[Literal["get_group_member_list"], GetGroupMemberListResp]):
    group_id: int


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


class GetGroupHonorInfoResp(BaseModel):
    group_id: int
    current_talkative: Optional[CurrentTalkativeInfo]
    talkative_list: Optional[list[HonorUserInfo]]
    performer_list: Optional[list[HonorUserInfo]]
    legend_list: Optional[list[HonorUserInfo]]
    strong_newbie_list: Optional[list[HonorUserInfo]]
    emotion_list: Optional[list[HonorUserInfo]]


class GetGroupHonorInfoReq(APIRequest[Literal["get_group_honor_info"], GetGroupHonorInfoResp]):
    group_id: int
    type: Literal["talkative", "performer",
                  "legend", "strong_newbie", "emotion", "all"]


class GetCookiesResp(BaseModel):
    cookies: str


class GetCookiesReq(APIRequest[Literal["get_cookies"], GetCookiesResp]):
    domain: Optional[str] = None
    """
    默认值为空

    需要获取 cookies 的域名
    """


class GetCSRFTokenResp(BaseModel):
    token: int


class GetCSRFTokenReq(APIRequest[Literal["get_csrf_token"], GetCSRFTokenResp]):
    pass


class GetCredentialsResp(BaseModel):
    cookies: str
    token: int


class GetCredentialsReq(APIRequest[Literal["get_credentials"], GetCredentialsResp]):
    domain: Optional[str] = None
    """
    默认值为空

    需要获取 cookies 的域名
    """


class GetRecordResp(BaseModel):
    file: str


class GetRecordReq(APIRequest[Literal["get_record"], GetRecordResp]):
    file: str
    out_format: Literal["mp3", "amr", "wma",
                        "m4a", "spx", "ogg", "wav", "flac"]


class GetImageResp(BaseModel):
    file: str


class GetImageReq(APIRequest[Literal["get_image"], GetImageResp]):
    file: str


class CanSendImageResp(BaseModel):
    yes: bool


class CanSendImageReq(APIRequest[Literal["can_send_image"], CanSendImageResp]):
    pass


class CanSendRecordResp(BaseModel):
    yes: bool


class CanSendRecordReq(APIRequest[Literal["can_send_record"], CanSendRecordResp]):
    pass


class GetStatusResp(Status):
    pass


class GetStatusReq(APIRequest[Literal["get_status"], GetStatusResp]):
    pass


class GetVersionInfoResp(BaseModel):
    model_config = ConfigDict(extra="allow")

    app_name: str
    app_version: str
    protocol_version: str


class GetVersionInfoReq(APIRequest[Literal["get_version_info"], GetVersionInfoResp]):
    pass


class SetRestartReq(APIRequest[Literal["set_restart"], EmptyResp]):
    delay: Optional[int] = None
    """
    默认值为 0

    要延迟的毫秒数，如果默认情况下无法重启，可以尝试设置延迟为 2000 左右
    """


class CleanCacheReq(APIRequest[Literal["clean_cache"], EmptyResp]):
    pass
