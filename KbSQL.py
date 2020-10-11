class KbTable:
    def __init__(self, tbl, keys):
        self.tbl = tbl
        lenKey = 0
        txtKey = ''
        for key in keys:
            if lenKey > 0:
                txtKey += ", "
            keyType = type(key)
            if keyType is list:
                txtKey += key[0] + ' ' + key[1]
            else:
                txtKey += str(key) + ' text'
            lenKey += 1
        self.creSQL = "CREATE TABLE " + tbl + ' ( ' + txtKey + ')'
        self.drpSQL = "DROP TABLE " + tbl
        self.insSQL = 'INSERT INTO ' + tbl + ' VALUES (' + ",".join(list('?' * lenKey)) + ')'
    def create(self, cursor, force=True):
        if force:
            try:
                self.drop(cursor)
            except Exception as errMsg:
                pass
        cursor.execute(self.creSQL)
    def drop(self, cursor):
        cursor.execute(self.drpSQL)
    def insert(self, cursor, lstVal):
        cursor.execute(self.insSQL, lstVal)
