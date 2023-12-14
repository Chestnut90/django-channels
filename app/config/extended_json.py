import json
from typing import Any


class ExtendedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, set):
            return {"__set__": True, "values": tuple(o)}
        return super().default(o)


class ExtendedJSONDecoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        kwargs.setdefault("object_hook", self._object_hook)
        super().__init__(**kwargs)

    @staticmethod
    def _object_hook(dct: dict):
        if "__set__" in dct:
            return set(dct["values"])
        return dct
