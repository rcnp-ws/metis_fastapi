import redis
from fastapi import APIRouter, Path
import datetime
router = APIRouter(
    prefix="/scaler",
    tags=["scaler"]
)

@router.get('/')
async def root() : 
    pass


@router.get('/read/{ip}/')
async def read_scaler(
    ip: str):
    if (ip == "10.32.2.169") : 
        # HR-TDC
        
    if (ip == "192.168.10.1") :
        scr = []
        for i in range(64):
            scr.append({"ch" : i, "val" : 0})
        ts = int(datetime.datetime.timestamp(datetime.datetime.now()))
        scr[63]['val'] = ts
        return {"scr": scr, "timestamp": ts, "ip": ip}
    else : 
        scr = []
        for i in range(32):
            scr.append({"ch" : i, "val" : 0})
        ts = int(datetime.datetime.timestamp(datetime.datetime.now()))
        scr[31]['val'] = ts
        return {"scr": scr, "timestamp": ts, "ip": ip}


