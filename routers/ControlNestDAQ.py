import redis
from fastapi import APIRouter

router = APIRouter(
   prefix="/nestdaq",
   tags=["nestdaq"]
)

@router.get('/')
async def root() : 
   pass

@router.get('/status/')
async def read_status():
   rcli = redis.Redis("vmeserver1-gp")
   #rcli = redis.Redis("localhost")
   key_updated = rcli.keys("daq_service:*:updatedTime")
   val_updated = rcli.mget(key_updated)
   key_state = rcli.keys("daq_service:*:fair-mq-state")
   val_state = rcli.mget(key_state)
   key_state = [x.decode().split(':')[2] for x in key_state ]
   
   state = dict(zip(key_state,val_state))
   return state

@router.get('/run_number/')
async def read_run_number():
   rcli = redis.Redis("vmeserver1-gp")
   #rcli = redis.Redis("localhost")
   val_run_number = rcli.get("run_info:run_number")
   return val_run_number

@router.get('/run_comment/')
async def read_run_comment():
   rcli = redis.Redis("vmeserver1-gp")
   #rcli = redis.Redis("localhost")
   val_run_comment = rcli.get("run_info:run_comment")
   return val_run_comment
