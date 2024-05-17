from pydantic import BaseModel, model_validator
from ..event import Event, QuickOperationsUnion, EventDiscriminatorMap, MessageTypeQuickOperationMap
from .shared import API

@API(".handle_quick_operation")
class HandleQuickOperationArgs(BaseModel):
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
