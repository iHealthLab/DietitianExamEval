from conn_mysql import ClientMysql


class DBUtils:

    def __init__(self):
        self.mysql_client = ClientMysql()

    def create_non_cover_patients(self, table_name):
        table = table_name
        self.mysql_client.execute('''DROP TABLE IF EXISTS {}'''.format(table))
        self.mysql_client.execute(
            '''
               CREATE TABLE IF NOT EXISTS `{}` (
                `id`                        int AUTO_INCREMENT,
                `memberId`                  varchar(24) NOT NULL,
                `firstName`                 varchar(50) NOT NULL,
                `lastName`                  varchar(50) NOT NULL,
                `birthday`                  datetime,
                `teamId`                    varchar(24),
                `organizationId`            varchar(24),
                PRIMARY KEY `id` (`id`)
            ) 
        '''.format(table))

    def create_auto_message(self, table_name):
        table = table_name
        # self.mysql_client.execute('''DROP TABLE IF EXISTS {}'''.format(table))
        self.mysql_client.execute(
            '''
               CREATE TABLE IF NOT EXISTS `{}` (
                `id`                        int AUTO_INCREMENT,
                `memberId`                  varchar(24) NOT NULL,
                `reminder_msg_date`         datetime,
                `ack_date`                  datetime,
                `check_after_reminder`      tinyint,
                `month`                     date,
                PRIMARY KEY `id` (`id`)
            ) 
        '''.format(table))


if __name__ == '__main__':
    db = DBUtils()
    db.create_non_cover_patients('gs_non_cover_patients')
