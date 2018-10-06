import psycopg2
from threading import get_ident


class DBConnector:
    def __init__(self, conf, initial_connect=True):
        self.host = conf.get("host", "localhost")
        self.port = conf.get("port", 5432)
        self.user = conf.get("user", "postgres")
        self.pw = conf.get("password", "")
        self.db = conf.get("database", "postgres")

        self.conn = None
        self.cursor = None

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

        if self.conn.closed:
            for x in self.curDict:
                self.curDict[x].close()

            self.getConn()

        if thread_id not in self.curDict or self.curDict[thread_id].closed:
            self.curDict[thread_id] = self.conn.cursor()

        return self.curDict[thread_id]

    def write_log(self, data):
        qstr = """INSERT INTO "APIInfo" ("""
        qstr += '"' + '", "'.join([str(x) for x in data.keys()]) + '") VALUES ('
        qstr += "'" + "', '".join([str(x) for x in data.values()]) + "');"

        try:
            self.getCursor().execute(qstr)
        except psycopg2.ProgrammingError:
            return True, None
        except psycopg2.OperationalError:
            return self.write_log(data)
