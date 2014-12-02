import gevent
import struct

class ConnPool:

    int_size = struct.calcsize('i')
    def __init__(self, q_cls, sock_mod, sock_path, n, max_len, min_size=None):
        q = q_cls()
        count = 0
        for i in range(n):
            sock = sock_mod.socket(sock_mod.AF_UNIX)
            sock.connect(sock_path)
            allowed, = struct.unpack('i', sock.recv(self.int_size))
            if allowed:
                q.put(sock)
                count += 1
            else:
                sock.close()
                break
        if min_size and count < min_size:
            raise Exception("not enough connections")
        self.q = q
        self.max_len = max_len

    def send_recv(self, message):
        leng = len(message)
        if leng > self.max_len:
            raise Exception("content too long")
        proto = "{}{}".format(struct.pack("I", leng), message)
        sock = self.q.get()
        sock.send(proto)
        res_len, = struct.unpack('i', sock.recv(self.int_size))
        res = sock.recv(res_len)
        self.q.put(sock)
        return res
    
    def shutdown(self):
        while self.q.qsize():
            self.q.get().close()




if __name__ == "__main__":
    #make_q(8, gevent.queue.Queue, gevent.socket)
    global pool
    global s
    pool = ConnPool(gevent.queue.Queue, gevent.socket, "/var/run/bays.socket", 50)
    jobs = [gevent.spawn(repeat, 5) for x in range(8)]
    gevent.joinall(jobs)
    print([job.value for job in jobs])
    pool.shutdown()
    s = "movies about young vampires and werewolves"
    pool = ConnPool(gevent.queue.Queue, gevent.socket, "/var/run/bays.socket", 50)
    jobs = [gevent.spawn(repeat, 5) for x in range(8)]
    gevent.joinall(jobs)
    print([job.value for job in jobs])



