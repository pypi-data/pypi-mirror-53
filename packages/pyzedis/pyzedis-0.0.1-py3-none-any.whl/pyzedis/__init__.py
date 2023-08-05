import zmq
import json


class ZedisClient:
    port = "5555"
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:%s" % port)

    def zset(self, key, value):
        self.socket.send_string(
            "SET {} {}".format(str(key), str(value)))
        return self.socket.recv()

    def zset_json(self, key, value):
        self.socket.send_string(
            "SET {} {}".format(str(key), json.dumps(value)))
        return self.socket.recv()

    def zget_json(self, key):
        self.socket.send_string("GET {}".format(str(key)))
        return json.loads(self.socket.recv())

    def zget(self, key):
        self.socket.send_string("GET {}".format(str(key)))
        return self.socket.recv()

    def zkeys(self):
        self.socket.send_string("KEYS")
        return json.loads(self.socket.recv())

    def zclear(self):
        self.socket.send_string("CLEAR")
        return json.loads(self.socket.recv())

    def zflush(self):
        self.socket.send_string("FLUSH")
        return json.loads(self.socket.recv())

    def zdel(self, key):
        self.socket.send_string("DEL {}".format(str(key)))
        return json.loads(self.socket.recv())

    def zpre(self, prefix):
        self.socket.send_string("PRE {}".format(str(prefix)))
        return json.loads(self.socket.recv())



# snake = ZedisClient()

# snake.zset_json("david", {"status": 200})

# snake.zget_json("david")
