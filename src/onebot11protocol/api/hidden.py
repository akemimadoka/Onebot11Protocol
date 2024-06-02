from typing import Literal
from pydantic import model_validator
from ..event import Event, QuickOperationsUnion, EventDiscriminatorMap, MessageTypeQuickOperationMap
from .shared import APIRequest, EmptyResp


class HandleQuickOperationReq(APIRequest[Literal[".handle_quick_operation"], EmptyResp]):
    context: Event
    operation: QuickOperationsUnion

    @model_validator(mode="after")
    def checkQuickOperation(self):
        postType = self.context.post_type
        discriminator = EventDiscriminatorMap[postType]
        discriminatorValue = getattr(self.context, discriminator)
        discriminatorQuickOperationMap = MessageTypeQuickOperationMap[postType]
        expectQuickOperation = discriminatorQuickOperationMap[discriminatorValue]
        if not isinstance(self.operation, expectQuickOperation):
            raise ValueError("Unmatched event and operation")
        return self
