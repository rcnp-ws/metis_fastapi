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
   key_updated = rcli.keys("daq_service:*:updatedTime")
   val_updated = rcli.mget(key_updated)
   key_state = rcli.keys("daq_service:*:fair-mq-state")
   val_state = rcli.mget(key_state)
   key_state = [x.decode().split(':')[2] for x in key_state ]
   
   state = dict(zip(key_state,val_state))
   return state