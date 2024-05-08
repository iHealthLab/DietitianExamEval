import time

import pandas as pd
import pymysql.cursors
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from config import env
from log import Log


class ClientMysql:
    def __init__(self):
        self.user = env.str("MYSQL_USER")
        self.password = env.str("MYSQL_PASSWORD")
        self.host = env.str("MYSQL_HOST")
        self.port = env.str("MYSQL_PORT")
        self.db = env.str('DB_NAME')
        self.logger = Log().get_logger()
        self.conn = self.get_conn()
        ssl = {'ssl': {'fake_flag_to_enable_tls': True}}

        self.engine = create_engine(
            'mysql+pymysql://{}:{}@{}:{}/{}'.format(self.user, self.password,
                                                    self.host, self.port,
                                                    self.db), connect_args=ssl)

    def get_conn(self):
        count = 0
        while True:
            try:
                if count >= 5:
                    raise Exception("Can't connect to mysql")
                count += 1
                conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    port=int(self.port),
                    database=self.db,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor,
                    ssl={'ssl': {}}
                )
                return conn
            except pymysql.err.OperationalError as e:
                self.logger.error(e)
                time.sleep(5)

    def execute(self, sql):
        count = 0
        while True:
            with self.engine.connect() as con:
                try:
                    if count >= 3:
                        raise Exception("Failed to execute query")
                    count += 1
                    con.execution_options(isolation_level="AUTOCOMMIT")
                    res = con.execute(sql)
                    return res
                except Exception as e:
                    self.logger.error(e)
                    time.sleep(5)

    def read_df(self, table, select_cols=None):
        if not select_cols:
            sql = """select * from {}""".format(table)
        else:
            select_cols = ','.join(['`{}`'.format(col) for col in select_cols])
            sql = """select {} from {}""".format(select_cols, table)
        return pd.read_sql(sql, con=self.engine)

    def save(self, table_name, pd_data, if_exists):
        conn = self.engine.connect()
        try:
            pd_data.to_sql(name=table_name, con=conn, if_exists=if_exists, index=False)
        except Exception as e:
            self.logger.error(e)
            self.logger.warning('Exception Occurred when save to {}'.format(table_name))
        finally:
            conn.close()


if __name__ == '__main__':
    mysql = ClientMysql()
