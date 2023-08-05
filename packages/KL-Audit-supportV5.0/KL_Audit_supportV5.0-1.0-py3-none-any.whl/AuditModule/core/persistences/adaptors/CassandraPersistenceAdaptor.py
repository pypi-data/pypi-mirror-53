import traceback


import cassandra.cluster
from AuditModule.common import AppConstants
from AuditModule.util import Logging as LOGG

Logger = LOGG.get_logger()

class CassandraDButility:
    def __init__(self):
        """
            Initializer
        """
        try:
            Logger.info("Initializing DB connection")
            self.cluster = cassandra.cluster.Cluster(AppConstants.CassandraConstants.CLUSTER)
            self.session = self.cluster.connect()
            scada_create_statement = AppConstants.CassandraConstants.SCADA_CREATE_STATEMENT
            useraccess_create_statement = AppConstants.CassandraConstants.USERACCESS_CREATE_STATEMENT
            dbupdates_create_statement = AppConstants.CassandraConstants.DBUPDATES_CREATE_STATEMENT
            keyspace_statement = AppConstants.CassandraConstants.KEYSPACE_STATEMENT
            self.session.execute(keyspace_statement)
            self.session.execute(useraccess_create_statement)
            self.session.execute(dbupdates_create_statement)
            self.session.execute(scada_create_statement)
            Logger.info("DB initialised successfully")
            self.var = True
        except Exception as e:
            self.var = False
            Logger.error("Exception in the cassandradb initialization" + str(e))
            traceback.print_exc()

    def table_check(self, table):
        try:
            Logger.info("entered in to table check function")
            insert_statement = """
                CREATE TABLE audit_logs.{0}(id int, time timestamp,name text,
                PRIMARY KEY(name, id))
                WITH CLUSTERING ORDER BY (id DESC)""".format(table)
            if self.var is True:
                self.session.execute(insert_statement)
                Logger.info("Table check completed")
                return True
            else:
                self.__init__()
                if self.var is True:
                    Logger.info("Reconnecting to the cassandra DB")
                    return self.table_check(table)
                else:
                    Logger.info("Cassandra DB is not up, try again after restarting to cassandra")
                    traceback.print_exc()

        except Exception as e:
            Logger.exception("Exception occured while cheking or creating the table" + str(e))
            return False

    def insert_table_id(self, table, json_obj):
        try:
            if self.var is True:
                insert_statment = self.session.prepare(AppConstants.CassandraConstants.TABLE_INSERT_STATEMENT.format(table))
                self.session.execute(insert_statment, json_obj)
                Logger.info("Data inserted successfully")
                return True
            else:
                self.__init__()
                if self.var is True:
                    Logger.info("Reconnecting to the cassandra DB")
                    return self.insert_table_id(table, json_obj)
                else:
                    Logger.info("Cassandra DB is not up, try again after restarting to cassandra")
                    traceback.print_exc()
        except Exception as e:
            Logger.exception("Exception while inserting the data " + str(e))
            return False

    def fetch_table_id(self, table):
        try:
            if self.var is True:
                insert_statement = self.session.prepare(
                    AppConstants.CassandraConstants.SELECT_STATEMENT.format(table, table))
                response = self.session.execute(insert_statement)
                return response.current_rows
            else:
                self.__init__()
                if self.var is True:
                    Logger.info("Reconnecting to the cassandra DB")
                    return self.fetch_table_id(table)
                else:
                    Logger.info("Cassandra DB is not up, try again after restarting to cassandra")
                    traceback.print_exc()
        except Exception as e:
            traceback.print_exc()
            raise Exception(str(e))

    def insert_record(self, json_obj, table):
        """
            sample json
            {
            "id": "",
            "lable": "",
        :param json:
        :return:
        """
        try:
            if self.var is True:
                insert_statment = self.session.prepare(AppConstants.CassandraConstants.INSERT_STATEMENT.format(table))
                self.session.execute(insert_statment, json_obj)
                Logger.info("Data inserted successfully")
                return True
            else:
                self.__init__()
                if self.var is True:
                    Logger.info("Reconnecting to the cassandra DB")
                    return self.insert_record(json_obj, table)
                else:
                    Logger.info("Cassandra DB is not up, try again after restarting to cassandra")
                    traceback.print_exc()
        except Exception as e:
            Logger.exception("Exception while inserting the data " + str(e))
            return False
