import cx_Oracle

from apps.helper.common_class_instance import CommonClassInstance

# instance of other class
common_cls_ins = CommonClassInstance.get_instance()


class OracleDatabase:
    def __init__(self):
        try:
            print("Loading Database Configuration Files....")
            common_cls_ins.logger.log_info(msg="Loading Database Configuration Files....")
            self.db_host = common_cls_ins.config.get("oracle_db_host", "")
            self.db_service_name = common_cls_ins.config.get("oracle_db_name", "")
            self.db_port = common_cls_ins.config.get("oracle_db_port", "")
            self.db_user = common_cls_ins.config.get("oracle_db_username", "")
            self.db_password = common_cls_ins.config.get("oracle_db_password", "")
            self._conn = None
            self._cursor = None
        except Exception as e:
            print(e)
            common_cls_ins.logger.log_critical(msg=f"Config file not loaded....{e}")

    def connect(self):
        try:
            common_cls_ins.logger.log_info(msg="Attempting ORACLE Connection")
            dsn_tns = cx_Oracle.makedsn(self.db_host, self.db_port, service_name=self.db_service_name)
            self._conn = cx_Oracle.connect(user=self.db_user, password=self.db_password, dsn=dsn_tns)
            self._cursor = self._conn.cursor()
            print("Connected To Database")
        except Exception as e:
            common_cls_ins.logger.log_critical(
                msg=f"There is a problem with Oracle DETAIL(single_data_record): EXCEPTION - {e}")
            common_cls_ins.logger.log_error(exception=e)
            print(e)
            raise

    def close_connection(self):
        try:
            self._cursor.close()
        except Exception as e:
            print(e)
            common_cls_ins.logger.log_error(exception=e)
            raise

    def commit_execution(self):
        self._conn.commit()

    def total_rows_count(self, query):
        common_cls_ins.logger.log_info(msg="Initiated totalRowsCount Query = " + query)
        return self.select_query(query, 'count')

    def select_single_row(self, query):
        common_cls_ins.logger.log_info("Initiated single row Query = " + query)
        return self.select_query(query=query, return_type='single_row')

    def select_query(self, query, return_type='row'):
        try:
            # connect to database
            self.connect()
            common_cls_ins.logger.log_info(msg="Initiated Query = " + query)

            if return_type == 'row':
                self._cursor.execute(query)
                res = self._cursor.fetchall()
            elif return_type == 'single_row':
                self._cursor.arraysize = 1
                self._cursor.execute(query)
                res = self._cursor.fetchone()
            else:
                self._cursor.execute(query)
                self._cursor.fetchall()
                res = self._cursor.rowcount
            print('Query Response Size = ', len(res))
            common_cls_ins.logger.log_info(msg=f"Query Response - {res}")
            # closing database connection
            self.close_connection()
            if not res:
                common_cls_ins.logger.log_critical(msg="Query Failed")
                return 0
            else:
                common_cls_ins.logger.log_info(msg="Query Successful")
                return res
        except cx_Oracle.DatabaseError as e:
            print(e)
            self.close_connection()
            common_cls_ins.logger.log_critical(msg="Query Failed Due To " + str(e))
            return 0

    def execute_query(self, query):
        common_cls_ins.logger.log_info(msg="Attempting Query = " + query)

        try:
            # connect to database
            self.connect()
            print("Attempting query = " + query)
            self._cursor.execute(query)
            self.commit_execution()
            common_cls_ins.logger.log_info(msg="Execution Successful")
            self.close_connection()
            return 1
        except cx_Oracle.DatabaseError as e:
            common_cls_ins.logger.log_critical(msg="Execution Failed Due To " + str(e))
            print(e)
            return 0

    def execute_many_query(self, query, param):
        common_cls_ins.logger.log_info(msg="Attempting Query = " + query)
        try:
            # connect to database
            self.connect()
            # param = [
            #     (10, 'Parent 10'),
            #     (20, 'Parent 20'),
            #     (30, 'Parent 30'),
            #     (40, 'Parent 40'),
            #     (50, 'Parent 50')
            # ]
            # Query = "insert into RPA_DIV_ERASE_VOUCHER (COMPLAIN_ID, MSISDN) values (:1, :2)"
            self._cursor.setinputsizes(None, 200)
            self._cursor.executemany(query, param)
            self.commit_execution()
            # closing database connection
            self.close_connection()
            common_cls_ins.logger.log_info(msg="Execution Batch Query Successful")
            print("Execution Batch Query Successful")
            return 1
        except Exception as e:
            common_cls_ins.logger.log_critical(msg="Execution Failed Due To " + str(e))
            self.close_connection()
            print(e)
            return 0
        except cx_Oracle.DatabaseError as e:
            common_cls_ins.logger.log_critical(msg="Execution Failed Due To " + str(e))
            self.close_connection()
            print(e)
            return 0
