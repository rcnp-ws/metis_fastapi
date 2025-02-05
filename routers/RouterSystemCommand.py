import subprocess
from fastapi import APIRouter

router = APIRouter(
   prefix="/syscmd",
   tags=["syscmd"]
)

@router.get('/')
async def root() : 
   pass

@router.get('/exec/{cmd:path}')
async def exec(cmd: str):
   try:
#      ret = subprocess.Popen(cmd, shell=True, text=True)
#      p.wait()
      p = subprocess.Popen(cmd, shell=True, text=True, stdout=subprocess.PIPE)
      ret = p.stdout
#      p.wait()
#      ret = subprocess.Popen(cmd, shell=True, capture_output=True, text=True).stdout
#      ret = subprocess.check_output(cmd, shell=True, text=True)
#      ret = subprocess.run(cmd, shell=True, text=True)
   except Exception as e:
      ret = "Error in subprocess.Popen(" + cmd + ") : " + str(e)
   return {"message": ret}

@router.get('/exec/')
async def exec():
   return {"message": "No command"}
