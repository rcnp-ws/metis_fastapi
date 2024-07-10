import re
import subprocess
import time
import numpy as np
from BaseScaler import BaseScaler


class HulScaler(BaseScaler):
    CommandPath = ""
    VersionCommand = "get_version"

    def __init__(self, ip: str):
        super(HulScaler, self).__init__()
        self._types = {
            "0xc480": {"name": "StrHrTdc Base", "numCh": 32, "numBit": [32] * 32},
            "0x60c4": {"name": "StrLrTdc", "numCh": 129, "numBit": [32] * 129},
            "0xf000": {"name": "Mikumari", "numCh": 66, "numBit": [32] * 66},
        }
        self._dataCmd = {
            "0xc480": [
                [
                    "read_mzn_scr {1} up {0} ",
                    "od -An -j40 -v -t u4 -w4 {0}",
                    "od -An -j4 -N4 -v -t u4 -w4 {0}",
                ],
                [
                    "read_mzn_scr {1} down {0} ",
                    "od -An -j40 -v -t u4 -w4 {0}",
                    "od -An -j4 -N4 -v -t u4 -w4 {0}",
                ],
            ],
            "0x60c4": [
                [
                    "read_scr {1} {0} ",
                    "od -An -j40 -v -t u4 -w4 {0}",
                    "od -An -j4 -N4 -v -t u4 -w4 {0}",
                ],
            ],
            "0xf000": [
                [
                    "read_scr {1} {0} ",
                    "od -An -j40 -v -t u4 -w4 {0}",
                    "od -An -j4 -N4 -v -t u4 -w4 {0}",
                ]
            ],
        }
        self._info["address"] = ip
        self.getVersion(ip)

    def loopGetData(self, nLoop):
        iLoop = 0
        lastModified = 0
        period = 1  # second
        checkStep = 0.1
        while ((iLoop < nLoop) if nLoop > 0 else 1):
            if time.time() - lastModified < period:
                time.sleep(checkStep)
                continue
            iLoop += 1
            lastModified = time.time()
            self.getData()

    def getData(self):
        print(self._info["fwid"])
        print(self._dataCmd[self._info["fwid"]])
        print(self._data)
        self._lastData = self._data
        for idx, fmts in enumerate(self._dataCmd[self._info["fwid"]]):
            cmd = []
            sid = "{}-{}".format(self._info["address"], idx)
            for fmt in fmts:
                cmd.append(
                    fmt.format(
                        ".scaler.{}-{}.txt".format(self._info["address"], idx),
                        self._info["address"],
                    )
                )
            cmd = " && ".join(
                cmd,
            )
            cmd = HulScaler.CommandPath + "'" + cmd + "'"
            print(cmd)
            lines = (
                (subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True))
                .communicate()[0]
                .decode("utf-8")
                .split("\n")
            )
            values = []
            for line in lines:
                if (not len(line)) or line[0] == "*" or line[0] == "#":
                    continue
                values.append(line)
            hbfn = values.pop(-1)
            timestamp = time.time()
            if len(values) == self._info["numCh"]:
                print("good")
            else:
                print("bad")

            diffValues = [np.nan] * self._info["numCh"]
            diffHbfn = 0
            diffTs = 0
            if len(self._lastData) > 0 and sid in self._lastData:
                lastValues = self._lastData[sid]["data"]
                lastHbfn = self._lastData[sid]["hbfn"]
                lastUpdate = self._lastData[sid]["ts"]
                for i, val in enumerate(lastValues):
                    diffValues[i] = int(values[i]) - int(val)
                    diffValues[i] += 2**int(self._info["numBit"]
                                            ) if diffValues[i] < 0 else 0
                diffHbfn = int(hbfn) - int(lastHbfn)
                diffHbfn += (2**24) if diffHbfn < 0 else 0

                diffTs = float(timestamp) - float(lastUpdate)
            self._data[sid] = {"data": values, "hbfn": hbfn, "ts": timestamp,
                               "diff": diffValues, "diffHbfn": diffHbfn, "diffTs": diffTs}
        print(self._data)

    def getVersion(self, ip):
        cmd = HulScaler.CommandPath + HulScaler.VersionCommand
        lines = (
            (
                subprocess.Popen(
                    cmd + " " + ip, stdout=subprocess.PIPE, shell=True
                ).communicate()[0]
            )
            .decode("utf-8")
            .split("\n")
        )
#        print(lines)
        for line in lines:
            if (not len(line)) or line[0] == "*" or line[0] == "#":
                continue
            result = re.match(r"FW ID +: (\S+)", line)
            if result:
                self._info["fwid"] = result.group(1)
                if self._info["fwid"] in self._types:
                    self._info["type"] = self._types[self._info["fwid"]]["name"]
                    self._info["numCh"] = self._types[self._info["fwid"]]["numCh"]
                    self._info["numBit"] = self._types[self._info["fwid"]]["numBit"]
                    self._info["isValid"] = True
                else:
                    self._info["type"] = "unknown"
                    self._info["isValid"] = False
                continue
            result = re.match(r"FW version +: (\S+)", line)
            if result:
                self._info["fwver"] = result.group(1)
                continue


def main():
    import sys

    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        ip = "192.168.2.169"
    HulScaler.CommandPath = "ssh ata03 "
    scaler = HulScaler(ip)
    print(scaler._info)
    scaler.loopGetData(2)


if __name__ == "__main__":
    main()
