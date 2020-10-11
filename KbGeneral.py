import datetime
import urllib.request
from urllib.error import URLError, HTTPError
#import socket
import re
import sys

class Counter:
    def __init__(self, interval, limit=None, skip=0):
        self.__interval = interval
        self.__limit = limit
        self.__skip  = skip
        self.reset()
    def reset(self):
        self.__count = 0
    def is_interval(self):
        return ((self.__count - self.__skip) % self.__interval)==0
    def is_over(self):
        return (self.__limit and self.__count > (self.__limit + self.__skip))
    def is_skip(self):
        return self.__count <= self.__skip
    def up(self):
        self.__count += 1
    def count(self):
        return self.__count
    def say(self, *prms):
        dt = datetime.datetime.now()
        print(dt.strftime('%Y/%m/%d(%a) %X'), ':', *prms)
    def say_c(self, *prms, **kwargs):
        fmt = kwargs['fmt'] if 'fmt' in kwargs else '> {}:'
        self.say(fmt.format(self.__count),  *prms)

# Tab Separated File (Read)
class TSVFile:
    def __init__(self, fname, enc=''):
        if enc == '':
            self.fp = open(fname, 'r')
        else:
            self.fp = open(fname, 'r', encoding=enc)
   
    def __iter__(self):
        return self
    def __next__(self): 
        row = self.fp.readline()
        if not row:
            raise StopIteration()
        else:
            return list(row.strip("\n").split("\t"))
    def __del__(self):
        self.fp.close()

def mkd(path):
    if not (os.path.exists(path)):
        os.mkdir(path)

ptnChrst = re.compile('charset=(\S+)')
def getUrl(url):
    retry = 0
    tmlst = [20, 40, 80]
    while retry < len(tmlst):
        try:
            with urllib.request.urlopen(url, timeout=tmlst[retry]) as res:
                cont = res.read()
                mtch = ptnChrst.search( res.headers['Content-Type'])
                chrst = mtch[1] if mtch else ''
                if mtch:
                    if retry <= 0:
                        if chrst == 'shift_jis' or chrst == 'Windows-31J':
                            chrst = 'cp932'
                        return(cont.decode(chrst))
                    else:
                        return(cont.decode('latin1'))
                else:
                    return(cont.decode())
        except HTTPError as e:
            print('Error HTTP code: ', e.code, url, file=sys.stderr)
            return None
        except URLError as e:
            print('Error URL Reason: ', e.reason, url, file=sys.stderr)
            return None
        except Exception as errMsg:
            retry += 1
            print("getUrl:", 'WARNING:' + str(errMsg), '('+ str(retry) + ')',   url, file=sys.stderr)
    print('ERROR: timeout retry error', file=sys.stderr)
    return None
