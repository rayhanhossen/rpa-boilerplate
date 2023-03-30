import mysql.connector
from mysql.connector import Error

from apps.helper.common_class_instance import CommonClassInstance

# instance of other class
common_cls_ins = CommonClassInstance.get_instance()


class MySQLDatabase:
    def __init__(self):
        self.host = common_cls_ins.config.get("mysql_db_host")
        self.database = common_cls_ins.config.get("mysql_db_name")
        self.port = int(common_cls_ins.config.get("mysql_db_port"))
        self.username = common_cls_ins.config.get("mysql_db_username")
        self.password = common_cls_ins.config.get("mysql_db_password")
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                      database=self.database,
                                                      port=self.port,
                                                      user=self.username,
                                                      password=self.password)

            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.close()

        except Error as e:
            print("Error while connecting to MySQL", e)

    def create_table(self, table_query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(table_query)
            print('Table created successfully')
            cursor.close()
        except Error as e:
            print("Failed to create table in MySQL: {}".format(e))

    def insert_data_into_table(self, insert_query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_query)
            self.connection.commit()
            print("Record inserted successfully")
            cursor.close()
        except Error as e:
            print("Failed to insert record {}".format(e))

    def select_data_from_table(self, select_query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            records = cursor.fetchall()
            return records
        except Error as e:
            print("Error reading data from MySQL table", e)

    def update_data_from_table(self, update_query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(update_query)
            self.connection.commit()
            print("Record Updated successfully")
            cursor.close()
        except Error as e:
            print("Failed to update table record: {}".format(e))

    def delete_data_from_table(self, delete_query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(delete_query)
            self.connection.commit()
            print("Record Deleted successfully ")
            cursor.close()
        except Error as e:
            print("Failed to delete record from table: {}".format(e))
