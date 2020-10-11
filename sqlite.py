import sys
import sqlite3
import os

db = sys.argv[1]
if not (os.path.exists(db)):
    if input(db + ' not exists. do you really want to create? (Y/n): ') != 'Y':
        sys.exit()
conn = sqlite3.connect(db)
c = conn.cursor()
INTERVAL = 20
OUTFILE='sqliteout.txt'
fpO = False
preSQL = ''
while 1:
    sql = input(('SQL: ' if preSQL == '' else '   : '))
    if sql == '':
        break
    elif sql[0:2] == '>>':
        if not fpO:
            fpO = open(OUTFILE, 'w', encoding='utf-8')
        else:
            print("Alread Spooing", file=sys.stderr)
    elif sql[0:1] == '>':
        if not fpO:
            fpO = open(OUTFILE, 'a', encoding='utf-8')
        else:
            print("Alread Spooing", file=sys.stderr)
    elif sql[0:1] == '<':
        print('END:', sql)
        if fpO:
          fpO.close()
          fpO = False 
    elif sql[-1] == '\\':
        preSQL += sql[0:-1]
    else:
        try:
            execSQL = preSQL + sql
            preSQL = ''
            if fpO:
                print("SQL: ", execSQL, file=fpO)
            res = c.execute(execSQL)
            if res:
                cnt = 0
                for row in res:
                    cnt += 1
                    if fpO:
                        print("\t".join(list(map(lambda x: str(x), row))), file=fpO)
                    else:
                        if (cnt % INTERVAL) == 0:
                            res = input('> Continue? (y/N): ')
                            res = 'N' if not res else res
                            if res == 'N':
                                break
                        print(row)
                print("lines: " + str(cnt))
            else:
                if fpO:
                    print("NO RES", file=fpO)
                print("NO RES")
        except Exception as inst:
            if fpO:
                print("ERROR:", str(inst), file=fpO)
            print("ERROR:", inst)
if fpO:
    fpO.close()
