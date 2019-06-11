import os
import sqlite3


class SQL:

    def __init__(self):
        self.connect = self.get_connect()
        self.cursor = self.connect.cursor()

    @staticmethod
    def get_connect():
        dir_path = os.getcwd()
        database_path = os.path.join(dir_path, "database.db")
        if os.path.exists(database_path):
            connect = sqlite3.connect(database_path)
            return connect
        else:
            connect = sqlite3.connect(database_path)
            sql_create_table = '''
            create table test(
            download_date varchar ,
            target varchar ,
            file_md5 varchar ,
            download_url varchar ,
            );
            '''
            connect.cursor().execute(sql_create_table)
            connect.commit()
            return connect

    def insert(self, sql):
        self.cursor.execute(sql)
        self.cursor.close()
        self.connect.close()

    def select(self, sql):
        result = self.cursor.execute(sql).fetchall()
        print(result)
        self.cursor.close()
        self.connect.close()


if __name__ == "__main__":
    # SQL().select("select * from test ;")
    SQL().insert("insert into test('id','Datetime', 'FileMd5','FilePath', 'DownloadUrl')values ('aa', 'bb', 'cc', 'dd', 'ee');")
