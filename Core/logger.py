import psycopg2
import logging
import requests
import traceback
import psutil
import os
import time
from datetime import datetime, timedelta
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


class DiscordLogger(logging.Handler):
    def __init__(self, conf):
        super(DiscordLogger, self).__init__()
        self.hook = conf.get("uri")
        self.username = conf.get("username", "Python Logger")
        self.avatar_url = conf.get("avatar", "https://www.python.org/static/favicon.ico")
        self.mention = conf.get("mention", "")

    def _get_ip(self):
        try:
            return requests.get("http://ipinfo.io/ip").text.replace("\r", "").replace("\n", "")
        except:
            return "0.0.0.0"

    def _process_uptime(self):
        try:
            return timedelta(seconds=time.time() - psutil.Process(os.getpid()).create_time()).__str__()
        except:
            return "0:00:00.000000"

    def _system_uptime(self, *args, **kwargs):
        try:
            with open('/proc/uptime', 'r') as f:
                return str(timedelta(seconds=float(f.readline().split()[0])))
        except:
            return "0:00:00.000000"

    def emit(self, record):
        self.lastest_logging = requests.post(
            self.hook,
            json={
                "content": self.mention if self.mention else "",
                "username": self.username,
                "avatar_url": self.avatar_url,
                "embeds": [
                    {
                        "title": "Runtime Reporter",
                        "description": "Reporting from IP: " + self._get_ip(),
                        "fields": [
                            {
                                "name": "Reporter Info",
                                "inline": False,
                                "value": f"""Host: {self._get_ip()}
                                Process Uptime: {self._process_uptime()}
                                System Uptime: {self._system_uptime()}"""
                            },
                            {
                                "name": "TraceBack",
                                "inline": False,
                                "value": traceback.format_exc()
                            },
                            {
                                "name": "Log Body",
                                "inline": False,
                                "value": self.format(record)
                            }
                        ],
                        "footer": {
                            "text": "Python Logger | " + datetime.now().strftime("%Y%m%dT%H%M%S.%fZ")
                        }
                    }
                ]
            },
            headers={
                "Content-Type": "multipart/form-data"
            }
        )
        return self.lastest_logging
