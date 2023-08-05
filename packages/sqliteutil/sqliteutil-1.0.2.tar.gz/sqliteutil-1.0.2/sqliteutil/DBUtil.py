import sys
import sqlite3
import queue
import time
import threading
import logging
import logging.handlers
import traceback


def init_log(log_name='mysqlutil'):
    """
    init module log
    :param log_name:
    :return:
    """
    logger = logging.getLogger(name=log_name)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s')
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger


def escape_name(s):
    return f"`{s.replace('`', '``')}`"


class DB:

    def __init__(self, db_path=None, max_cached=5, idle_time=600, log=None):

        if not log:
            self.log = init_log()
        self._db_path = db_path
        if not self._db_path:
            self.log.error('need db_path')
            sys.exit(1)

        #
        self._max_cached = min(max_cached, 10)
        self._max_cached = max(self._max_cached, 1)
        self._idle_time = max(idle_time, 300)
        self._idle_time = min(self._idle_time, 1800)
        self.pool = queue.Queue(maxsize=self._max_cached)

        # check pool
        t = threading.Thread(target=self._check_pool)
        t.setDaemon(True)
        t.start()

    def _create_conn(self):
        return sqlite3.connect(self._db_path, check_same_thread=False)

    def get_conn(self):
        try:
            return self.pool.get_nowait()[0]
        except queue.Empty:
            return self._create_conn()

    def recycle(self, conn):
        """
        recycle connection
        :param conn:
        :return:
        """
        if not conn:
            return
        try:
            self.pool.put_nowait((conn, time.time()))
        except queue.Full:
            conn.close()

    def _check_pool(self):
        while True:
            time.sleep(10)
            self._check_alive()

    def _check_alive(self):
        try:
            conn, last_time = self.pool.get_nowait()
        except queue.Empty:
            return

        try:
            if time.time() - last_time > self._idle_time:
                conn.close()
            else:
                try:
                    self.pool.put_nowait((conn, last_time))
                except queue.Full:
                    conn.close()
        except:
            self.log.error(traceback.format_exc())

    def fetchall(self, sql, data=()):
        """
        Fetch all the rows
        :param sql:
        :param data:
        :return: False - DB Error | () - No result | [{field1: value1, field2: value2}, ...]
        """
        result = False
        conn = None
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            if not data:
                cur.execute(sql)
            else:
                cur.execute(sql, data)
            result = cur.fetchall()
            conn.commit()
        except:
            self.log.error(traceback.format_exc())
        finally:
            self.recycle(conn)
        return result

    def fetchfirst(self, sql, data=()):
        """
        Fetch the first row
        :param sql:
        :param data:
        :return: False - DB Error | None - No Result | {field1: value1, field2: value2}
        """
        result = False
        conn = None
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            if not data:
                cur.execute(sql)
            else:
                cur.execute(sql, data)
            result = cur.fetchone()
            conn.commit()
        except:
            self.log.error(traceback.format_exc())
        finally:
            self.recycle(conn)
        return result

    def fetchone(self, sql, data=()):
        """
        Fetch the next row
        :param sql:
        :param data:
        :return: iterable, False - DB Error | {field1: value1, field2: value2}
        """
        conn = None
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            if not data:
                cur.execute(sql)
            else:
                cur.execute(sql, data)
            for _ in range(cur.rowcount):
                yield cur.fetchone()
            conn.commit()
        except GeneratorExit:
            conn.commit()
        except:
            self.log.error(traceback.format_exc())
            yield False
        finally:
            self.recycle(conn)

    def fetchmany(self, sql, num, data=()):
        """
        Fetch several rows
        :param sql:
        :param num:
        :param data:
        :return: iterable, False - DB Error | [{field1: value1, field2: value2}, ...]
        """
        conn = None
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            if not data:
                cur.execute(sql)
            else:
                cur.execute(sql, data)
            while result := cur.fetchmany(num):
                yield result
            conn.commit()
        except GeneratorExit:
            conn.commit()
        except:
            self.log.error(traceback.format_exc())
            yield False
        finally:
            self.recycle(conn)

    def execute(self, sql, data=()):
        """
        Execute a query
        :param sql: Query to execute.
        :param data:
        :return: False - DB Error | True - execute successfully
        """
        result = False
        conn = None
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            if not data:
                cur.execute(sql)
            else:
                cur.execute(sql, data)
            conn.commit()
            result = True
        except:
            self.log.error(traceback.format_exc())
        finally:
            self.recycle(conn)
        return result

    def executemany(self, sql, data_list):
        """
        Run several data against one query
        :param sql: query to execute on server
        :param data_list: Sequence of sequences.  It is used as parameter.
        :return: False - DB Error | True - execute successfully
        """
        result = False
        conn = None
        try:
            if not isinstance(data_list, list):
                return result

            conn = self.get_conn()
            cur = conn.cursor()
            cur.executemany(sql, data_list)
            conn.commit()
            result = True
        except:
            self.log.error(traceback.format_exc())
        finally:
            self.recycle(conn)
        return result

    def insert(self, tbl, data):
        """
        Insert one row into table
        :param tbl:
        :param data:
        :return: False - DB Error | True - insert successfully
        """
        result = False
        conn = None
        try:
            if isinstance(data, dict):
                names = []
                values = []
                for name in data:
                    names.append(name)
                    values.append(data[name])
                values = tuple(values)
                # names = list(data)
                # cols = ', '.join(map(escape_name, names))
                cols = ', '.join(names)
                placeholders = ', '.join(['?'] * len(names))
                query = f'INSERT INTO `{tbl}` ({cols}) VALUES ({placeholders})'
            else:
                return result

            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute(query, values)
            conn.commit()
            result = True
        except:
            self.log.error(traceback.format_exc())
        finally:
            self.recycle(conn)
        return result
