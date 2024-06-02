from abc import ABC, abstractmethod
import asyncio
from types import TracebackType
from typing import Optional, Type

from ..api.shared import APIRequest
from ..event import Event


class CommunicationSessionBase(ABC):
    @abstractmethod
    async def send[Name, RespType](self, request: APIRequest[Name, RespType]) -> RespType:
        pass

    @abstractmethod
    async def listen(self) -> Event:
        pass

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_val: Optional[BaseException],
                        exc_tb: Optional[TracebackType]):
        await self.disconnect()


class CommunicationBase[TEndpoint, TSession](ABC):
    @abstractmethod
    async def connect(self, endpoint: TEndpoint) -> TSession:
        pass
