import redis
from fastapi import APIRouter
from modules.RedisProxy import RedisProxy

router = APIRouter(
   prefix="/nestdaq",
   tags=["nestdaq"]
)

aProxy = RedisProxy();
#aProxy.connect("localhost",6379,0);
aProxy.connect("vmeserver1-gp",6379,0)
rcli = aProxy.instance()

@router.get('/')
async def root() : 
   pass

@router.get('/status/')
async def read_status():
   key_updated = rcli.keys("daq_service:*:updatedTime")
   val_updated = rcli.mget(key_updated)
   key_state = rcli.keys("daq_service:*:fair-mq-state")
   val_state = rcli.mget(key_state)
   key_state = [x.decode().split(':')[2] for x in key_state ]
   
   state = dict(zip(key_state,val_state))
   return state

@router.get("/set_path/{key}/{val:path}")
async def read_item(key: str, val:str) :
   rcli.set(key,val)
   return {"message": "set_path"}

@router.get('/run_number')
async def read_run_number():
   val_run_number = rcli.get("run_info:run_number")
   return {"message" : val_run_number}

@router.get('/run_comment')
async def read_run_comment():
   val_run_comment = rcli.get("run_info:run_comment")
   return {"message" : val_run_comment}
