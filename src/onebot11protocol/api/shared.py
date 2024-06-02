from typing import ClassVar, TypeVar
from pydantic import BaseModel, ConfigDict


class Status(BaseModel):
    model_config = ConfigDict(extra="allow")

    online: bool
    good: bool


# snake_case 太丑了，必须换成 CamelCase
def _name_prettier(name: str):
    return "".join(part.title() for part in name.split("_"))


class APIRequest[Name, RespType]:
    def __class_getitem__(cls, typeParameters):
        assert isinstance(typeParameters, tuple) and len(
            typeParameters) == 2, "Invalid type parameters"

        if isinstance(typeParameters[0], TypeVar):
            # 未绑定的 class
            return cls
        name = typeParameters[0].__args__[0]
        prettyName = _name_prettier(name)
        return type(f"{prettyName}ReqBase", (BaseModel,), {
            "typeParameters": typeParameters,
            "__annotations__": {
                "typeParameters": ClassVar[tuple]
            }
        })


class EmptyResp(BaseModel):
    pass
