import asyncio
from dataclasses import dataclass
import json
from types import TracebackType
from typing import Any, Optional, TypedDict
from pydantic import TypeAdapter
import websockets
import websockets.connection

from ..event import Event

from ..api.shared import APIRequest

from .base import CommunicationBase, CommunicationSessionBase


@dataclass
class WebSocketEndpoint:
    url: str
    access_token: Optional[str] = None


class RawAPIResponse(TypedDict):
    status: str
    retcode: int
    data: Any
    echo: str


def _is_bad_retcode(retcode: int):
    return retcode == 1400 or retcode == 1401 or retcode == 1403 or retcode == 1404


class BadAPIResponseException(Exception):
    def __init__(self, *args: object, response: RawAPIResponse) -> None:
        super().__init__(*args)
        self.response = response


class WebSocketSession(CommunicationSessionBase):
    def __init__(self, loop: asyncio.AbstractEventLoop, endpoint: WebSocketEndpoint) -> None:
        super().__init__()
        self.endpoint = endpoint
        self.loop = loop
        self.api_index = 0
        self.waiting_api_map: dict[int, asyncio.Future[RawAPIResponse]] = {}
        self.is_listening = False

    async def listen(self) -> Event:
        self.is_listening = True
        try:
            while True:
                data = await self.websocket.recv()
                jsonData = json.loads(data)
                if "self_id" in jsonData:
                    # 是 event
                    print(jsonData)
                    event: Event = TypeAdapter(Event).validate_python(jsonData)
                    return event
                else:
                    # 是 api 的响应
                    jsonData: RawAPIResponse
                    apiIndex = int(jsonData["echo"])
                    future = self.waiting_api_map[apiIndex]
                    future.set_result(jsonData)
                    del self.waiting_api_map[apiIndex]
        finally:
            self.is_listening = False

    async def send[Name, RespType](self, request: APIRequest[Name, RespType]) -> RespType:
        if not self.is_listening:
            raise Exception("Not listening, cannot fetch response")

        apiNameLiteral, respType = request.typeParameters
        apiName = apiNameLiteral.__args__[0]
        index = self.api_index
        self.api_index += 1
        content = {
            "action": apiName,
            "params": request.model_dump(),
            "echo": str(index)
        }
        future: asyncio.Future[RawAPIResponse] = self.loop.create_future()
        self.waiting_api_map[index] = future
        await self.websocket.send(json.dumps(content))
        response = await future
        retcode = response["retcode"]
        if _is_bad_retcode(retcode):
            raise BadAPIResponseException(
                f"Api \"{apiName}\"(#{index}) invocation failed with retcode: {retcode}", response=response)
        return respType.model_validate(response["data"])

    async def connect(self):
        self.websocket = await websockets.connect(self.endpoint.url, extra_headers={
            "Authorization": f"Bearer {self.endpoint.access_token}"} if self.endpoint.access_token else None, loop=self.loop)

    async def disconnect(self):
        await self.websocket.close()


class WebSocketCommunication(CommunicationBase[WebSocketEndpoint, WebSocketSession]):
    def connect(self, endpoint: WebSocketEndpoint) -> WebSocketSession:
        loop = asyncio.get_event_loop()
        return WebSocketSession(loop, endpoint)
