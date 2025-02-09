from fastapi import APIRouter, FastAPI, Depends
from fastapi.responses import JSONResponse
import threading
import time
import json
from multiprocessing import Value
from modules.json_dbstore import json_dbstore
from modules.wrap_babicmdjson import runinfo
from modules.RedisProxy import RedisProxy

router = APIRouter(
   prefix="/babirl",
   tags=["babirl"]
)
dbpath = "test.db"



async def babinfo(host : str) : 
   return runinfo(host)
#   with runinfo(host) as info :
#      yield info

#@router.get("/")
#async def root():
#      return {"message": "API for babirl daq control. Please specify the server to control and path for the data base.."}
#   
#@router.get("/config/{key}/{val:path}")
#async def set_path(key: str, val: str):
#    rcli.set(key, val)
#    return JSONResponse(content={"message": "set_path"}, headers={"Access-Control-Allow-Origin": "*"})   

def makeMessage(status: int, message: str, payload: dict = {}) : 
   ret = {'header': {'status': status, 'message': message} };
   if len(payload) > 0 :
      ret['payload'] = json.loads(payload)
   return ret

@router.get("/")
async def root():
   return JSONResponse(content={"message": "API for babirl daq control. Please specify the server to control and path for the data base.."}, headers={"Access-Control-Allow-Origin": "*"})

@router.get("/host/{host}")
async def set_host(host: str):
      ret = makeMessage(0, "set host {}".format(host))
      return JSONResponse(content=ret, headers={"Access-Control-Allow-Origin": "*"})   

@router.get("/{host}/monitor/")
async def monitor(info : runinfo = Depends(babinfo)):
   ret = info.getconfig()
   return JSONResponse(content=ret, headers={"Access-Control-Allow-Origin": "*"})

@router.get("/{host}/control/stop/ender={ender}")
async def stop(ender: str, info : runinfo = Depends(babinfo)):
    ret = info.getconfig()
    if 'error' in ret:
        return JSONResponse(content=ret, headers={"Access-Control-Allow-Origin": "*"})
    state = "START"
    if "runinfo" not in ret or "runstatus" not in ret["runinfo"]:
        return JSONResponse(content={"error": "Invalid runinfo", "runinfo": ret["runinfo"]}, headers={"Access-Control-Allow-Origin": "*"})
    if ret["runinfo"]["runstatus"] == "NSSTA":
        state = "NSSTA"
    resp_text = json.dumps(info.getinfo("stop", ender))
    info.getconfig()
    info.getevtnumber()
    if 'error' in resp_text:
        return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    if state == "NSSTA":
        return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    count = 0
    ret = info.getconfig()
    if 'error' in ret:
        return JSONResponse(content=ret, headers={"Access-Control-Allow-Origin": "*"})
    while count < 3 and ret["runinfo"]["runstatus"] == state:
        time.sleep(1)
        ret = info.getconfig()
        count += 1
    ret = info.getconfig()
    type = ret["runinfo"]["runname"] + str(ret["runinfo"]["runnumber"]).zfill(4)
    # ret.update(info.getevtnumber())
    return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    
@router.get("/{host}/control/start/header={header}")
async def start(header: str, info : runinfo = Depends(babinfo)):
    info.getinfo("wth", header)
    resp_text = json.dumps(info.getinfo("start", ""))
    if 'error' in resp_text:
        return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    count = 0
    ret = info.getconfig()
    if "runinfo" not in ret or "runstatus" not in ret["runinfo"]:
        return JSONResponse(content={"error": "Invalid runinfo", "runinfo": ret["runinfo"]}, headers={"Access-Control-Allow-Origin": "*"})
    while count < 3 and ret["runinfo"]["runstatus"] == "IDLE":
        time.sleep(1)
        ret = info.getconfig()
        count += 1
    ret = info.getconfig()
    type = ret["runinfo"]["runname"] + str(ret["runinfo"]["runnumber"]).zfill(4)
    return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    
@router.get("/{host}/control/nssta")
async def nssta(info : runinfo = Depends(babinfo)):
    resp_text = json.dumps(info.getinfo("nssta", ""))
    return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})

@router.get("/{host}/control/setrunnumber/{runnumber}")
async def setrunnumber(runnumber: int, info : runinfo = Depends(babinfo)):
    resp_text = json.dumps(info.getinfo("setrunnumber", str(runnumber)))
    return JSONResponse(content=json.loads(resp_text), headers={"Access-Control-Allow-Origin": "*"})
    
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    t1 = threading.Thread(target=monitorWorker)
    t1.start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5042)
    doMonitor.value = 0
