from typing import Annotated, Literal, Optional, Union
from pydantic import Field, BaseModel

DataSegmentMap: dict[type, type] = {}


# 一个 Segment 可能对应多个 DataType，但是一个 DataType 只能对应一个 Segment
class SegmentBase[Name, DataType](BaseModel):
    def __class_getitem__(cls, typeParameters):
        assert isinstance(typeParameters, tuple) and len(
            typeParameters) == 2, "Invalid type parameters"
        nameLiteral, dataType = typeParameters
        name = nameLiteral.__args__[0]

        return type(f"{name.title()}SegmentBase", (SegmentBase,), {
            "type": name,
            "__annotations__": {
                "type": nameLiteral,
                "data": dataType,
            },
        })

    def __init_subclass__(cls, **kwargs):
        if cls.__name__.endswith("Base"):
            # 生成的类
            return

        dataType = cls.__mro__[1].__annotations__["data"]
        if hasattr(dataType, "__args__"):
            if dataType.__name__ == "Annotated":
                dataType = dataType.__args__[0]
            assert dataType.__name__ == "Union"
            # 是 Union
            DataSegmentMap.update((singleDataType, cls)
                                  for singleDataType in dataType.__args__)
        else:
            # 是单个类型
            DataSegmentMap[dataType] = cls


class TextData(BaseModel):
    text: str


class TextSegment(SegmentBase[Literal["text"], TextData]):
    pass


class FaceData(BaseModel):
    id: str


class FaceSegment(SegmentBase[Literal["face"], FaceData]):
    pass


class ImageDataBase(BaseModel):
    file: str
    type: Optional[Literal["flash"]] = None


class ReceivedImageData(ImageDataBase):
    url: str


class SendingImageData(ImageDataBase):
    cache: Literal[0, 1]
    proxy: Literal[0, 1]
    timeout: int


class ImageSegment(SegmentBase[Literal["image"], Union[ReceivedImageData, SendingImageData]]):
    pass


class RecordDataBase(BaseModel):
    file: str


class ReceivedRecordData(RecordDataBase):
    magic: Literal[0, 1]
    url: str


class SendingRecordData(RecordDataBase):
    magic: Optional[Literal[0, 1]] = None
    cache: Literal[0, 1]
    proxy: Literal[0, 1]
    timeout: int


class RecordSegment(SegmentBase[Literal["record"], Union[ReceivedRecordData, SendingRecordData]]):
    pass


class VideoDataBase(BaseModel):
    file: str


class ReceivedVideoData(VideoDataBase):
    url: str


class SendingVideoData(VideoDataBase):
    cache: Literal[0, 1]
    proxy: Literal[0, 1]
    timeout: int


class VideoSegment(SegmentBase[Literal["video"], Union[ReceivedVideoData, SendingVideoData]]):
    pass


class AtData(BaseModel):
    qq: str


class AtSegment(SegmentBase[Literal["at"], AtData]):
    pass


class EmptyData(BaseModel):
    pass


class RpsSegment(SegmentBase[Literal["rps"], EmptyData]):
    pass


class DiceSegment(SegmentBase[Literal["dice"], EmptyData]):
    pass


class ShakeSegment(SegmentBase[Literal["shake"], EmptyData]):
    pass


class PokeDataBase(BaseModel):
    type: str
    id: str


class ReceivedPokeData(PokeDataBase):
    name: str


class SendingPokeData(PokeDataBase):
    pass


class PokeSegment(SegmentBase[Literal["poke"], Union[ReceivedPokeData, SendingPokeData]]):
    pass


class ReceivedAnonymousData(BaseModel):
    pass


class SendingAnonymousData(BaseModel):
    ignore: Literal[0, 1]


class AnonymousSegment(SegmentBase[Literal["anonymous"], Union[ReceivedAnonymousData, SendingAnonymousData]]):
    pass


class ShareDataBase(BaseModel):
    url: str
    title: str


class ReceivedShareData(ShareDataBase):
    content: str
    image: str


class SendingShareData(ShareDataBase):
    content: Optional[str] = None
    image: Optional[str] = None


class ShareSegment(SegmentBase[Literal["share"], Union[ReceivedShareData, SendingShareData]]):
    pass


class QQContactInfo(BaseModel):
    type: Literal["qq"] = "qq"
    id: str


class GroupContactInfo(BaseModel):
    type: Literal["group"] = "group"
    id: str


class ContactSegment(SegmentBase[Literal["contact"], Annotated[Union[QQContactInfo, GroupContactInfo], Field(..., discriminator="type")]]):
    pass


class LocationDataBase(BaseModel):
    lat: float
    lon: float


class ReceivedLocationData(LocationDataBase):
    title: str
    content: str


class SendingLocationData(LocationDataBase):
    title: Optional[str] = None
    content: Optional[str] = None


class LocationSegment(SegmentBase[Literal["location"], Union[ReceivedLocationData, SendingLocationData]]):
    pass


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
    content: Optional[str] = None
    image: Optional[str] = None


MusicData = Annotated[Union[QQMusicData, NeteaseMusicData, XMMusicData,
                            CustomMusicData], Field(..., discriminator="type")]


class MusicSegment(SegmentBase[Literal["music"], MusicData]):
    pass


class ReplyData(BaseModel):
    id: str


class ReplySegment(SegmentBase[Literal["reply"], ReplyData]):
    pass


class ForwardData(BaseModel):
    id: str


class ForwardSegment(SegmentBase[Literal["forward"], ForwardData]):
    pass


class NodeData(BaseModel):
    id: str


class NodeCustomData(BaseModel):
    user_id: str
    nickname: str
    content: "Message"


class NodeSegment(SegmentBase[Literal["node"], Union[NodeData, NodeCustomData]]):
    pass


class XMLData(BaseModel):
    data: str


class XMLSegment(SegmentBase[Literal["xml"], XMLData]):
    pass


class JSONData(BaseModel):
    data: str


class JSONSegment(SegmentBase[Literal["json"], JSONData]):
    pass


Segment = Annotated[Union[TextSegment, FaceSegment, ImageSegment, RecordSegment, VideoSegment, AtSegment, RpsSegment, DiceSegment, ShakeSegment, PokeSegment, AnonymousSegment,
                          ShareSegment, ContactSegment, LocationSegment, MusicSegment, ReplySegment, ForwardSegment, NodeSegment, XMLSegment, JSONSegment], Field(..., discriminator="type")]

Message = list[Segment]


class MessageBuilder:
    content = Message()

    def add(self, data):
        segmentType = DataSegmentMap[type(data)]
        self.content.append(segmentType(data=data))
        return self

    def finish(self):
        return self.content
