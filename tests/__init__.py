import pytest

from onebot11protocol.event import *
from onebot11protocol.event.message import *

from onebot11protocol.api.hidden import HandleQuickOperationArgs
from onebot11protocol.message.segment import Segment, TextData, TextSegment

def test_models():
    args = HandleQuickOperationArgs(context=PrivateMessageEvent(time=0, sub_type="friend", self_id=0, message_id=0, user_id=0, message=[TextSegment(
        data=TextData(text="a"))], raw_message="", font=1, sender=PrivateSenderInfo(user_id=0, nickname="", sex="female", age=1)), operation=PrivateMessageEventQuickOperation())

    HandleQuickOperationArgs.model_validate(args)
    str = args.model_dump_json()
    print(str)
    obj = HandleQuickOperationArgs.model_validate_json(str)
    assert args == obj
