from modules.HulScalerTask import HulScalerTask
from modules.HulScaler import HulScaler


class ScalerFactory:
    def __init__(self):
        self._info = {}
        self._data = {}
        self._keys = {}
        self._scalers = {}

    def message(self, status: int, message: str, payload: dict = {}):
        ret = {'header': {'status': status, 'message':  message}}
        if len(payload):
            ret['payload'] = payload
        return ret

    def addHulScaler(self, id: str, series: str = ""):
        if id in self._scalers:
            return self.message(0, "already exists {}".format(id))
        aTask = HulScalerTask(id)
        print("addHulScaler")
        if not aTask.isValid():
            return self.message(-1, "scaler does not exists {}".format(id))
        self._keys[id] = []
        for infoKey in aTask.getInfo():
            self._info[infoKey] = aTask.getInfo()[infoKey]
            self._keys[id].append(infoKey)
        self._scalers[id] = aTask
        self._scalers[id].start()
        return self.message(0, "successfully added {}".format(id))

    def suspend(self):
        for id in self._scalers :
            self._scalers[id].suspend()

    def resume(self):
        for id in self._scalers :
            self._scalers[id].resume()
            

    def removeScaler(self, id: str):
        self._scalers[id].stop()
        for infoKey in self._keys[id]:
            self._info.pop(infoKey)
            self._data.pop(infoKey)
        self._keys.pop(id)
        self._scalers.pop(id)

    def get_info(self, id: str = ""):
        if len(id):
            if id in self._scalers:
                return self.message(0, "success", self._scalers[id].getInfo())
            else:
                return self.message(-1, "no such id {}".format(id))

        return self.message(0, "success", self._info)

    def get_data(self, id: str = ""):
        if len(id):
            if id in self._scalers:
                return self.message(0, "success for {}".format(id), self._scalers[id].getData())
            else:
                return self.message(-1, "no such id {}".format(id))
        for scaler in self._scalers.values():
            for id, data in self._scaler.getData().items():
                self._data[id] = data
        return self.message(0, "success", self._data)


def main():
    HulScaler.CommandPath = "ssh ata03 "

    factory = ScalerFactory()
    factory.addScaler("192.168.2.169")


if __name__ == "__main__":
    main()
