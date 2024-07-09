import json

class BaseScaler:

   def __init__(self) -> None:
      self._numCh = 0
      self._numBit = 0
      self._data = []
      self._type = "scalerType"
      self._id = "id_or_ip"
      self._version = "version"
      self._id = "id"
#      self._isValid = False

   def getJson(self):
         if self._numCh != len(self._data):
             return json.dumps({
                 self._id : {
                     "isValid": False
                 }
             })
         return json.dumps({
                 self._id : {
                     'isValid': True,
                     'numCh' : self._numCh,
                     'numBit': self._numBit,
                     'data'  : self._data,
                     'type'  : self._type
                 }
         })