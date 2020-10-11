import threading, queue

class KbThreadD:
    def __init__(self, fncW, fncE, MAX=5, ENDKEY='>>END<<'):
        self.cnt_t = 0
        self.MAX_T = MAX
        self.END_KEY = ENDKEY
        self.start_queue = queue.Queue(self.MAX_T)
        self.end_queue = queue.Queue(self.MAX_T*2)
        self.funcW = fncW
        self.funcE = fncE
        for i in range(self.MAX_T):
            threading.Thread(target=self.worker, daemon=True).start()
    def worker(self):
        while 1:
            try:
                prm = self.start_queue.get()
                if prm == self.END_KEY:
                    break
                bStart = True
                res = self.funcW(*prm)
                self.end_queue.put([True, res])
            except Exception as errMsg:
                self.end_queue.put([False, str(errMsg)])
    def waitT(self):
        rtn = self.end_queue.get()
        if rtn != self.END_KEY:
            self.funcE(rtn[0], rtn[1])
    def start(self, *prm):
        while (not self.end_queue.empty()):
            self.waitT()
        self.start_queue.put(prm)
    def end(self):
        print("END Start")
        for i in range(self.MAX_T):
            while (not self.end_queue.empty()):
                self.waitT()
            print("END_KEY:" + str(i))
            self.start_queue.put(self.END_KEY)
        print("COUNT:" + str(threading.active_count()))
        while not self.end_queue.empty() or threading.active_count() > 1:
            self.waitT()
