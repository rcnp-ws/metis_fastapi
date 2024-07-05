from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from modules.RedisProxy import RedisProxy
from routers import ControlNestDAQ

app = FastAPI()
app.include_router(ControlNestDAQ.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

aProxy = RedisProxy();
aProxy.connect("localhost",6379,0);

@app.get("/")
async def root():
    return {"message": aProxy.isConnected()}
@app.get("/set/{key}/{val}")
async def read_item(key: str, val: str) :
    r = aProxy.instance()
    r.set(key,val)
    return {"message": "hoge"}

@app.get("/get/{key}")
async def read_item(key: str) :
    r = aProxy.instance()
    val = r.get(key);
    if val == None :
        val = ""
    return {"message": val}

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return JSONResponse(content={"skip":skip, "limit":limit})

#    return {"skip":skip, "limit":limit}
