import psycopg2


class DBConnector:
    def __init__(self, conf):
        self.host = conf.get("host")
        self.port = conf.get("port")
        self.user = conf.get("user")
        self.password = conf.get("password")
        self.database = conf.get("database")

        self.makeConn()

    def makeConn(self):
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def makeCursor(self):
        if self.conn.closed:
            self.makeConn()

        return self.conn.cursor()

    def write_log(self, data):
        qstr = """INSERT INTO "APIInfo" ("""
        qstr += '"' + '", "'.join([str(x) for x in data.keys()]) + '") VALUES ('
        qstr += "'" + "', '".join([str(x) for x in data.values()]) + "');"

        self.makeCursor().execute(qstr)
        self.conn.commit()