import psycopg2
from threading import get_ident


class DBConnector:
    def __init__(self, conf):
        self.host = conf.get("host")
        self.port = conf.get("port")
        self.user = conf.get("user")
        self.password = conf.get("password")
        self.database = conf.get("database")

        self.connDict = {}
        self.curDict = {}

        self.makeConn()

    def getCursor(self):
        thread_id = get_ident().__int__()

        if thread_id not in self.connDict.keys() or self.connDict[thread_id].closed:
            self.connDict[thread_id] = self.makeConn()

        if thread_id not in self.curDict.keys() or self.connDict[thread_id].closed:
            self.curDict[thread_id] = self.connDict[thread_id].cursor()

        return self.curDict[thread_id]

    def makeConn(self):
        self.connDict[get_ident().__int__()] = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )

        return self.connDict[get_ident().__int__()]

    def write_log(self, data):
        qstr = """INSERT INTO "APIInfo" ("""
        qstr += '"' + '", "'.join([str(x) for x in data.keys()]) + '") VALUES ('
        qstr += "'" + "', '".join([str(x) for x in data.values()]) + "');"

        cur = self.getCursor()
        cur.execute(qstr)

    def fetch_column(self, column: str):
        cur = self.getCursor()
        try:
            cur.execute(f"""SELECT "timestamp", "{column}" FROM "APIInfo" ORDER BY "timestamp";""")
        except psycopg2.ProgrammingError:
            return True, None

        return False, cur.fetchall()


