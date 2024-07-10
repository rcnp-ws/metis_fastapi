import json


class BaseScaler:

    def __init__(self) -> None:
        self._data = {

        }
        self._lastData = {}
        self._info = {
        }
        self._lastUpdated = 0

    def getInfoJason(self):
        return json.dumps(self._info, ensure_ascii=False, indent=2)

    def getDataJson(self):
        return json.dumps(self._data, ensure_ascii=False, indent=2)
