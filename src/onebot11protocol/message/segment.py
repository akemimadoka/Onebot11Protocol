from typing import Annotated, Any, Literal, Optional, Union
from ..event.base import EventBase
from pydantic import BeforeValidator, Field, BaseModel, ValidationInfo


class TextData(BaseModel):
    text: str


class TextSegment(BaseModel):
    type: Literal["text"] = "text"
    data: TextData


class FaceData(BaseModel):
    id: str


class FaceSegment(BaseModel):
    type: Literal["face"] = "face"
    data: FaceData


class ImageDataBase(BaseModel):
    file: str
    type: Optional[Literal["flash"]]


class ReceivedImageData(ImageDataBase):
    url: str


class SendingImageData(ImageDataBase):
    cache: Literal[0, 1]
    proxy: Literal[0, 1]
    timeout: int


class ImageSegment(BaseModel):
    type: Literal["image"] = "image"
    data: Union[ReceivedImageData, SendingImageData]


class RecordDataBase(BaseModel):
    file: str


class ReceivedRecordData(RecordDataBase):
    magic: Literal[0, 1]
    url: str


class SendingRecordData(RecordDataBase):
    magic: Optional[Literal[0, 1]]
    cache: Literal[0, 1]
    proxy: Literal[0, 1]
    timeout: int


class RecordSegment(BaseModel):
    type: Literal["record"] = "record"
    data: Union[ReceivedRecordData, SendingRecordData]


class VideoDataBase(BaseModel):
    file: str


class ReceivedVideoData(VideoDataBase):
    url: str


class SendingVideoData(VideoDataBase):
    cache: Literal[0, 1]
    proxy: Literal[0, 1]
    timeout: int


class VideoSegment(BaseModel):
    type: Literal["video"] = "video"
    data: Union[ReceivedVideoData, SendingVideoData]


class AtData(BaseModel):
    qq: str


class AtSegment(BaseModel):
    type: Literal["at"] = "at"
    data: AtData


class EmptyData(BaseModel):
    pass


class RpsSegment(BaseModel):
    type: Literal["rps"] = "rps"
    data: EmptyData


class DiceSegment(BaseModel):
    type: Literal["dice"] = "dice"
    data: EmptyData


class ShakeSegment(BaseModel):
    type: Literal["shake"] = "shake"
    data: EmptyData


class PokeDataBase(BaseModel):
    type: str
    id: str


class ReceivedPokeData(PokeDataBase):
    name: str


class SendingPokeData(PokeDataBase):
    pass


class PokeSegment(BaseModel):
    type: Literal["poke"] = "poke"
    data: Union[ReceivedPokeData, SendingPokeData]


class ReceivedAnonymousData(BaseModel):
    pass


class SendingAnonymousData(BaseModel):
    ignore: Literal[0, 1]


class AnonymousSegment(BaseModel):
    type: Literal["anonymous"] = "anonymous"
    data: Union[ReceivedAnonymousData, SendingAnonymousData]


class ShareDataBase(BaseModel):
    url: str
    title: str


class ReceivedShareData(ShareDataBase):
    content: str
    image: str


class SendingShareData(ShareDataBase):
    content: Optional[str]
    image: Optional[str]


class ShareSegment(BaseModel):
    type: Literal["share"] = "share"
    data: Union[ReceivedShareData, SendingShareData]


class QQContactInfo(BaseModel):
    type: Literal["qq"] = "qq"
    id: str


class GroupContactInfo(BaseModel):
    type: Literal["group"] = "group"
    id: str


class ContactSegment(BaseModel):
    type: Literal["contact"] = "contact"
    data: Annotated[Union[QQContactInfo, GroupContactInfo],
                    Field(..., discriminator="type")]


class LocationDataBase(BaseModel):
    lat: float
    lon: float


class ReceivedLocationData(LocationDataBase):
    title: str
    content: str


class SendingLocationData(LocationDataBase):
    title: Optional[str]
    content: Optional[str]


class LocationSegment(BaseModel):
    type: Literal["location"] = "location"
    data: Union[ReceivedLocationData, SendingLocationData]


class SimpleMusicDataBase(BaseModel):
    id: str


class QQMusicData(SimpleMusicDataBase):
    type: Literal["qq"] = "qq"


class NeteaseMusicData(SimpleMusicDataBase):
    type: Literal["163"] = "163"


class XMMusicData(SimpleMusicDataBase):
    type: Literal["xm"] = "xm"


class CustomMusicData(BaseModel):
    type: Literal["custom"] = "custom"
    url: str
    audio: str
    title: str
    content: Optional[str]
    image: Optional[str]


MusicData = Annotated[Union[QQMusicData, NeteaseMusicData, XMMusicData,
                            CustomMusicData], Field(..., discriminator="type")]


class MusicSegment(BaseModel):
    type: Literal["music"] = "music"
    data: MusicData


class ReplyData(BaseModel):
    id: str


class ReplySegment(BaseModel):
    type: Literal["reply"] = "reply"
    data: ReplyData


class ForwardData(BaseModel):
    id: str


class ForwardSegment(BaseModel):
    type: Literal["forward"] = "forward"
    data: ForwardData


class NodeData(BaseModel):
    id: str


class NodeCustomData(BaseModel):
    user_id: str
    nickname: str
    content: "Message"


class NodeSegment(BaseModel):
    type: Literal["node"] = "node"
    data: Union[NodeData, NodeCustomData]


class XMLData(BaseModel):
    data: str


class XMLSegment(BaseModel):
    type: Literal["xml"] = "xml"
    data: XMLData


class JSONData(BaseModel):
    data: str


class JSONSegment(BaseModel):
    type: Literal["json"] = "json"
    data: JSONData


Segment = Annotated[Union[TextSegment, FaceSegment, ImageSegment, RecordSegment, VideoSegment, AtSegment, RpsSegment, DiceSegment, ShakeSegment, PokeSegment, AnonymousSegment,
                          ShareSegment, ContactSegment, LocationSegment, MusicSegment, ReplySegment, ForwardSegment, NodeSegment, XMLSegment, JSONSegment], Field(..., discriminator="type")]

Message = list[Segment]
