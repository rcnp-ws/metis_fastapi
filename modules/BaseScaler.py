import json


class BaseScaler:

    def __init__(self) -> None:
        self._data = {}
        self._info = {
            "numCh": 0,
            "numBit": 0,
            "address": "",
            "fwver": "",
            "fwid": "",
            "type": "",
            "isValid": False,
        }
        self._lastUpdated = 0

    def getInfoJason(self):
        return json.dumps(self._info, ensure_ascii=False, indent=2)

    def getDataJson(self):
        if self._numCh != len(self._data):
            return json.dumps({self._id: {"isValid": False}})
        return json.dumps(
            {
                self._id: {
                    "isValid": True,
                    "data": self._data,
                }
            }
        )
