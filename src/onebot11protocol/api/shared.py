APIArgsMap: dict[str, type] = {}

def API(name: str):
    def decorator(argsType: type):
        APIArgsMap[name] = argsType
        return argsType
    return decorator

APIRespMap: dict[str, type] = {}

def APIResp(name: str):
    def decorator(respType: type):
        APIRespMap[name] = respType
        return respType
    return decorator
