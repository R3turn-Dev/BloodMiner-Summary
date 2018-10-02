import psycopg2
from threading import get_ident


class DBLogger:
    def __init__(self, conf, initial_connect=True):
        self.host = conf.get("host", "localhost")
        self.port = conf.get("port", 5432)
        self.user = conf.get("user", "postgres")
        self.pw = conf.get("password", "")
        self.db = conf.get("database", "postgres")

        self.conn = None
        self.cursor = None

        self.connDict = {}
        self.curDict = {}

        if initial_connect:
            self.getConn()
            self.getCursor()

    def getConn(self):
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.pw,
            database=self.db
        )

        self.conn.autocommit = True
        return self.conn

    def getCursor(self):
        thread_id = get_ident().__int__()

        if thread_id not in self.connDict.keys():
            self.connDict[thread_id] = self.getConn()

        if thread_id not in self.curDict.keys():
            self.curDict[thread_id] = self.connDict[thread_id].cursor()

        return self.curDict[thread_id]

    def write_log(self, data):
        qstr = """INSERT INTO "APIInfo" ("""
        qstr += '"' + '", "'.join([str(x) for x in data.keys()]) + '") VALUES ('
        qstr += "'" + "', '".join([str(x) for x in data.values()]) + "');"

        self.getCursor().execute(qstr)