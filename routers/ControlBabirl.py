from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
import threading
import time
import json
from multiprocessing import Value
from json_dbstore import json_dbstore
from wrap_babicmdjson import runinfo

router = APIRouter(
   prefix="/babirl",
   tags=["babirl"]
)

doMonitor = Value('i', 1)
lock = threading.Lock()
info = runinfo("sels-fs01")
dbpath = "/home/exp/db/h445_3_runinfo.db"

def monitorWorker():
    while doMonitor.value == 1:
        lock.acquire()
        info.getconfig(doUpdate=True)
        time.sleep(0.01)
        info.getevtnumber(doUpdate=True)
        lock.release()
        time.sleep(1)

@router.get("/monitor/runinfo.json")
async def monitor():
    ret = info.getconfig()
    ret.update(info.getevtnumber())
    return JSONResponse(content=ret, headers={"Access-Control-Allow-Origin": "*"})

@router.get("/control/stop/ender={ender}")
async def stop(ender: str):
    lock.acquire()
    ret = info.getconfig(doUpdate=True)
    if 'error' in ret:
        lock.release()
        return JSONResponse(content=ret, headers={"Access-Control-Allow-Origin": "*"})
    state = "START"
    if "runinfo" not in ret or "runstatus" not in ret["runinfo"]:
        lock.release()
        return JSONResponse(content={"error": "Invalid runinfo"}, headers={"Access-Control-Allow-Origin": "*"})
    if ret["runinfo"]["runstatus"] == "NSSTA":
        state = "NSSTA"
    resp_text = json.dumps(info.getinfo("stop", ender, doUpdate=True))
    info.getconfig(doUpdate=True)
    info.getevtnumber(doUpdate=True)
    if 'error' in resp_text:
        lock.release()
        return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    if state == "NSSTA":
        lock.release()
        return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    db = json_dbstore(dbpath)
    db.createTableIfNot()
    db.commit()
    count = 0
    ret = info.getconfig(doUpdate=True)
    if 'error' in ret:
        lock.release()
        return JSONResponse(content=ret, headers={"Access-Control-Allow-Origin": "*"})
    while count < 3 and ret["runinfo"]["runstatus"] == "START":
        time.sleep(1)
        ret = info.getconfig(doUpdate=True)
        count += 1
    ret = info.getconfig(doUpdate=True)
    type = ret["runinfo"]["runname"] + str(ret["runinfo"]["runnumber"]).zfill(4)
    ret.update(info.getevtnumber())
    db.updateOrInsert(type, json.dumps(ret))
    db.commit()
    db.close()
    lock.release()
    return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    
@router.get("/control/start/header={header}")
async def start(header: str):
    lock.acquire()
    info.getinfo("wth", header, doUpdate=True)
    resp_text = json.dumps(info.getinfo("start", "", doUpdate=True))
    if 'error' in resp_text:
        lock.release()
        return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    db = json_dbstore(dbpath)
    db.createTableIfNot()
    db.commit()
    count = 0
    ret = info.getconfig(doUpdate=True)
    if "runinfo" not in ret or "runstatus" not in ret["runinfo"]:
        lock.release()
        return JSONResponse(content={"error": "Invalid runinfo"}, headers={"Access-Control-Allow-Origin": "*"})
    while count < 3 and ret["runinfo"]["runstatus"] == "IDLE":
        time.sleep(1)
        ret = info.getconfig(doUpdate=True)
        count += 1
    ret = info.getconfig()
    type = ret["runinfo"]["runname"] + str(ret["runinfo"]["runnumber"]).zfill(4)
    db.updateOrInsert(type, json.dumps(ret))
    db.commit()
    db.close()
    lock.release()
    return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    
@router.get("/control/nssta")
async def nssta():
    lock.acquire()
    resp_text = json.dumps(info.getinfo("nssta", "", doUpdate=True))
    lock.release()
    return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    t1 = threading.Thread(target=monitorWorker)
    t1.start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5042)
    doMonitor.value = 0
