from onebot11protocol.api.public import SendGroupMsgReq, SendPrivateMsgReq
import pytest

from onebot11protocol.communication.ws import WebSocketCommunication, WebSocketEndpoint
from onebot11protocol.event import *
from onebot11protocol.event.message import *

from onebot11protocol.api.hidden import HandleQuickOperationReq
from onebot11protocol.message.segment import DataSegmentMap, FaceData, MessageBuilder, TextData, TextSegment


def test_models():
    args = HandleQuickOperationReq(context=PrivateMessageEvent(message_type="private", time=0, sub_type="friend", self_id=0, message_id=0, user_id=0, message=[TextSegment(
        data=TextData(text="a"))], raw_message="", font=1, sender=PrivateSenderInfo(user_id=0, nickname="", sex="female", age=1)), operation=PrivateMessageEventQuickOperation())

    HandleQuickOperationReq.model_validate(args)
    str = args.model_dump_json()
    print(str)
    obj = HandleQuickOperationReq.model_validate_json(str)
    assert args == obj

    SendPrivateMsgReq(user_id=1, message=[
        TextSegment(data=TextData(text=""))])
    # SendPrivateMsgResp.model_validate_json("")
    GroupMessageEvent.model_validate({'self_id': 1, 'user_id': 2, 'time': 3, 'message_id': 4, 'message_seq': 5, 'real_id': 6, 'message_type': 'group', 'sender': {'user_id': 2, 'nickname': '测试', 'card': '', 'role': 'owner'},
                                     'raw_message': '[CQ:image,file=xxx.gif,url=xxx]', 'font': 14, 'sub_type': 'normal', 'message': [], 'message_format': 'array', 'post_type': 'message', 'group_id': 114514})

    print(TextSegment(data=TextData(text="abc")).model_dump())
    print(MessageBuilder().add(TextData(text="Hello")).add(FaceData(id="123")).finish())

    # async with WebSocketCommunication().connect(WebSocketEndpoint(url="ws://127.0.0.1:3001")) as session:
    #     def send():
    #         async def work():
    #             # IDE 应当能识别到返回类型为 SendGroupMsgResp
    #             resp = await session.send(SendGroupMsgReq(group_id=114514, message=[TextSegment(data=TextData(text="Hello"))]))
    #             print(resp)
    #         session.loop.create_task(work())
    #     session.loop.call_later(5, send)
    #     while True:
    #         event = await session.listen()
    #         if isinstance(event, GroupMessageEvent):
    #             print(event.message)
