import re
import subprocess

from BaseScaler import BaseScaler


class HulScaler(BaseScaler):
    CommandPath = ""
    VersionCommand = "get_version"

    def __init__(self, ip: str):
        super(HulScaler, self).__init__()
        self._types = {
            "0xc480": {"name": "StrHrTdc Base", "numCh": 32, "numBit": [32] * 32},
            "0x60c4": {"name": "StrLrTdc", "numCh": 129, "numBit": [32] * 129},
            "0xf000": {"name": "Mikumari", "numCh": 40, "numBit": [32] * 40},
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
            "0x60c4": [],
            "0xf000": [],
        }
        self._info["address"] = ip
        self.getVersion(ip)

    def getData(self):
        print(self._info["fwid"])
        print(self._dataCmd[self._info["fwid"]])
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
            timestamp = values.pop(-1)
            self._data[sid] = {"data": values, "ts": timestamp}
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
        print(lines)
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
    scaler.getData()


if __name__ == "__main__":
    main()
