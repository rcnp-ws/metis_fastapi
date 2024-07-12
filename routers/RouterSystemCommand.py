import subprocess
from fastapi import APIRouter

router = APIRouter(
   prefix="/syscmd",
   tags=["syscmd"]
)

@router.get('/')
async def root() : 
   pass

@router.get('/exe/{cmd}')
async def exe(cmd: str):
   try:
      ret = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
   except:
      ret = "Error in subprocess.check_call(" + cmd + ")"
   return ret
