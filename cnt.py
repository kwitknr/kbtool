import os
import sys
import datetime
import glob

tcnt = 0
args = sys.argv
for ff in (args[1:]):
    print(ff, end="\r")
    for f in glob.glob(ff):
        cnt = 0
        with open(f, 'r', encoding='utf-8') as fp:
            for row in fp:
               cnt += 1
        print(f, ':', str(cnt))
        tcnt += cnt
print('TOTAL:', str(tcnt), ' (', datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' )' )
