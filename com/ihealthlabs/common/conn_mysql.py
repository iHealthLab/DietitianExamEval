"""
Connects to the database in MySQL Workbench
"""
import time

import pandas as pd
import pymysql.cursors
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from config import env
from log import Log


class ClientMysql:
    """
    This class includes functions to interact with the database in MYSQL Workbench.
    """
    def __init__(self):
        """
        Initializes a ClientMysql object.
        """
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
        """
        Connects to the database, retrying up to 5 times if the connection fails.

        Returns:
            conn: A connection object for the database.

        Raises:
            Exception: If unable to connect to the database after 5 attempts.
        """
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
        """
        Executes the provided SQL query in the database, retrying up to 3 times if execution fails.

        Parameters:
            sql (str): The SQL query to execute.

        Returns:
            res: The result of the SQL execution.

        Raises:
            Exception: If the query fails after 3 attempts.
        """
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
        """
        Reads data from a specified table in the database and returns it as a DataFrame.

        Parameters:
            table (str): The name of the table to query.
            select_cols (list of str, optional): A list of column names to select. 
            If not provided, all columns will be selected.

        Returns:
            pd.DataFrame: A DataFrame containing the queried data.
        """
        if not select_cols:
            sql = """select * from {}""".format(table)
        else:
            select_cols = ','.join(['`{}`'.format(col) for col in select_cols])
            sql = """select {} from {}""".format(select_cols, table)
        return pd.read_sql(sql, con=self.engine)


    def save(self, table_name, pd_data, if_exists):
        """
        Saves a DataFrame to a specified table in the database.

        Parameters:
            table_name (str): The name of the table where the data will be saved.
            pd_data (pd.DataFrame): The DataFrame containing the data to save.
            if_exists (str): Specifies the behavior if the table already exists.
            Options are 'fail', 'replace', or 'append'.

        Returns:
            None
        """
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
