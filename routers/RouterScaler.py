import datetime

import redis
from fastapi import APIRouter, Path
from modules.ScalerFactory import ScalerFactory

router = APIRouter(prefix="/scaler", tags=["scaler"])

factory = ScalerFactory


@router.get("/")
async def root():
    pass


@router.get("/add/{id}/{series}")
async def scaler_add(id: str, series: str):
    factory.add(id, series)
    return factory.get_info(id)


@router.get("/read/info/all/")
async def scaler_read_info_all():
    return factory.get_info()


@router.get("/read/data/all")
async def scaler_read_data_all():
    return factory.get_data()


@router.get("/read/{ip}/")
async def read_scaler(ip: str):
    #    if (ip == "10.32.2.169"):
    #        # HR-TDC

    if ip == "192.168.10.1":
        scr = []
        for i in range(64):
            scr.append({"ch": i, "val": 0})
        ts = int(datetime.datetime.timestamp(datetime.datetime.now()))
        scr[63]["val"] = ts
        return {"scr": scr, "timestamp": ts, "ip": ip}
    else:
        scr = []
        for i in range(32):
            scr.append({"ch": i, "val": 0})
        ts = int(datetime.datetime.timestamp(datetime.datetime.now()))
        scr[31]["val"] = ts
        return {"scr": scr, "timestamp": ts, "ip": ip}
