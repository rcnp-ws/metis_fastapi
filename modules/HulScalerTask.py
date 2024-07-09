import threading
import time
import json
import subprocess
import re
import BaseScaler
from BaseEventTask import BaseEventTask

isDone = False
sendBuffer = {}
scalerList = {}

cmd_get_version = "get_version"
cmd_hul_scr = "read_scr"
cmd_amq_scr = "read_mzn_scr"

path="ssh ata03 "

cmdfmt = "{0} '{1} {2} .scaler.{1}.txt && od -j40 -An -v -t u4 -w4 .scaler.{1}.txt && od -j4 -N4 -An -v -t u4 -w4 .scaler.{1}.txt'"

class HulScalerTask (BaseEventTask):
   def __init__ (self) :
      super(HulScalerTask,self).__init__()
      self._isDone = False
      self._scalers = []
      

#   def addScaler (self, ip: str):


   def task(self):
      # ret = subprocess.Popen(path+cmd_get_version+" 192.168.2.169")
#      lines = (subprocess.Popen(path + cmd_get_version + " 192.168.2.169",stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8').split('\n')
      # print(lines)
#      for line in lines :
#         if (not len(line)) or line[0] == "*" or line[0] == "#" :
#            continue
#         result = re.match(r'FW ID +: (\S+)',line)
#         if result : 
#            self._id = result.group(1)
#            continue
#         result = re.match(r'FW version +: (\S+)',line)
#         if result :
#            self._version = result.group(1)
#            continue
      if self._id == "0xc480" : # hrtdc scr
         lastData = self._data
         self._data = []
         lines = (subprocess.Popen(cmdfmt.format(path+cmd_amq_scr,"192.168.2.169","up"),stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8').split('\n')
         print(lines)
         print(len(lines))
         for line in lines :
            if (not len(line)) or line[0] == "*" or line[0] == "#":
               continue
            self._data[]
         lines = (subprocess.Popen(cmdfmt.format(path+cmd_amq_scr,"192.168.2.169","low"),stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8').split('\n')
         print(lines)
         print(len(lines))         
      return {}



def main() :
   task = HulScalerTask()
   task.start()


if __name__ == "__main__" :
   HulScaler.VersionCommand = "ssh ata03 get_version"

   main()