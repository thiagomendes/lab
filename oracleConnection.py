import cx_Oracle


class OracleConnection(object):

    __connection_string = None
    __conn = None
    __cursor = None

    def __init__(self, connection_string):
        print '__init__::connection_string=' + connection_string
        self.__connection_string = connection_string

    def open_connection(self):
        print 'open_connection'
        self.__conn = cx_Oracle.connect(self.__connection_string)

    def close_connection(self):
        print 'close_connection'
        self.__conn.close()

    def close_cursor(self):
        print 'close_cursor'
        self.__cursor.close()

    def open_cursor(self):
        print 'open_cursor'
        self.__cursor = self.__conn.cursor()

    def execute(self, query, params, auto_commit=False, open_cursor=False, close_cursor=False):
        print 'execute'

        if open_cursor:
            self.open_cursor()

        if isinstance(params, tuple):
            print 'execute single'
            self.__cursor.execute(query, params)

        if isinstance(params, list):
            print 'execute many'
            self.__cursor.executemany(query, params)

        if auto_commit:
            self.commit()

        if close_cursor:
            self.close_cursor()

    def commit(self):
        print 'commit'
        self.__conn.commit()
