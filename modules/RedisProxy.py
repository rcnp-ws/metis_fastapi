import redis

class RedisProxy  :
    def __init__ (self) :
        self.__ip  = "localhost"
        self.__port = 6379
        self.__db = 0
        self.__redis = None
        self.__connected = False
        self.__cache = {}

    def isConnected(self) :
        try: 
            self.__redis.ping()
            self.__connected = True
        except Exception as e:
            # do nothing
            self.__redis = None
            self.__connected = False
        return self.__connected
        
    def connect(self,ip,port=6379,db=0) :
        if self.isConnected() :
            return True
        self.__redis = redis.Redis(ip,port,db)
        return self.isConnected();

    def instance(self) :
        return self.__redis
