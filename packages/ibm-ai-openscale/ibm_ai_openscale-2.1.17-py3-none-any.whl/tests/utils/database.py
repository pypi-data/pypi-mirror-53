# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
import requests
import psycopg2
from psycopg2.sql import Identifier, SQL


class Database(ABC):

    def __init__(self, credentials):
        self.credentials = credentials

    @abstractmethod
    def delete_schema(self, schema):
        pass

    @abstractmethod
    def create_schema(self, schema):
        pass

    @abstractmethod
    def execute_sql_query(self, query):
        pass

    @abstractmethod
    def list_tables_in_schema(self, schema):
        pass

    @abstractmethod
    def get_table_data(self, table, schema):
        pass


class PostgresDatabase(Database):

    def __init__(self, credentials):
        super(PostgresDatabase, self).__init__(credentials)

    def __prepare_connection(self):
        if 'uri' in self.credentials.keys():
            uri = self.credentials['uri']

            import re
            res = re.search('^[0-9a-zA-Z]+://([0-9a-zA-Z]+):([0-9a-zA-Z]+)@([^:]+):([0-9]+)/([0-9a-zA-Z]+)$', uri)

            if res is None:
                raise Exception('Unexpected format of db uri: {}'.format(uri))

            username = res.group(1)
            password = res.group(2)
            host = res.group(3)
            port = res.group(4)
            database = res.group(5)

            return psycopg2.connect(
                database=database,
                user=username,
                password=password,
                host=host,
                port=port
            )
        elif 'connection' in self.credentials.keys():
            pstg_connection = self.credentials['connection']['postgres']
            conn_str = "host='{}' port='{}' dbname='{}' user='{}' password='{}' sslmode='require'".format(
                pstg_connection['hosts'][0]['hostname'],
                pstg_connection['hosts'][0]['port'],
                pstg_connection['database'],
                pstg_connection['authentication']['username'],
                pstg_connection['authentication']['password'])
            return psycopg2.connect(conn_str)

    def execute_sql_query(self, query):
        conn = self.__prepare_connection()
        conn.autocommit = True
        query_result = None

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            query_result = cursor.fetchall()
        except psycopg2.ProgrammingError as ex:
            if "no results to fetch" not in str(ex):
                print("SQL execution failed. Query: {}\nReason: {}".format(query, ex))
        finally:
            cursor.close()
            conn.close()

        return query_result

    def delete_schema(self, schema):
        self.execute_sql_query(SQL("DROP SCHEMA {} CASCADE").format(Identifier(schema)))

    def create_schema(self, schema):
        self.execute_sql_query(SQL("CREATE SCHEMA {}").format(Identifier(schema)))

    def list_tables_in_schema(self, schema):
        query_result = self.execute_sql_query(
            query=SQL("""SELECT table_name FROM information_schema.tables WHERE table_schema = '{}'""".format(schema))
        )

        tables = []
        for res in query_result:
            tables.append(res[0])
        return tables

    def get_table_data(self, table, schema):
        query_result = self.execute_sql_query(
            query=SQL("""SELECT * FROM {}.{}""".format(schema, table))
        )

        return query_result


class DB2DatabaseICP(Database):
    import ibm_db

    def __init__(self, credentials):
        super(DB2DatabaseICP, self).__init__(credentials)

        if 'dsn' in self.credentials.keys():
            self.db2_dsn = self.credentials["dsn"]
        else:
            self.db2_dsn = self.credentials['ssldsn']

    def __prepare_connection(self):
        return self.ibm_db.connect(self.db2_dsn, "", "")

    def execute_sql_query(self, query):
        results_array = []

        connection = self.__prepare_connection()
        statement = self.ibm_db.prepare(connection, query)

        try:
            res = self.ibm_db.execute(statement)
            result_dict = self.ibm_db.fetch_tuple(statement)

            while result_dict is not False:
                results_array.append(result_dict[0])
                result_dict = self.ibm_db.fetch_tuple(statement)
        except Exception as ex:
            print("SQL execution failed:")
            print(ex)
        finally:
            self.ibm_db.close(connection)

        return results_array

    def delete_schema(self, schema):
        self.execute_sql_query(SQL("DROP SCHEMA {} CASCADE").format(Identifier(schema)))

    def create_schema(self, schema):
        self.execute_sql_query(SQL("CREATE SCHEMA {}").format(Identifier(schema)))

    def execute_immediately_query(self, query):
        connection = self.__prepare_connection()
        try:
            self.ibm_db.exec_immediate(connection, query)
        except Exception as ex:
            print("SQL immediately execution failed:")
            print(ex)
        finally:
            self.ibm_db.close(connection)

    def list_tables_in_schema(self, schema):
        query_result = self.execute_sql_query(""" SELECT TABNAME FROM syscat.tables WHERE TABSCHEMA = '{}' """.format(schema))
        db2_tables = []
        for record in query_result:
            db2_tables.append(record)

        return db2_tables

    def get_table_data(self, table, schema):
        query_result = self.execute_sql_query(
            """ SELECT * FROM "{}"."{}" """.format(schema, table))

        return str(query_result)


class DB2DatabaseCloud(Database):
    def __init__(self, credentials):
        super(DB2DatabaseCloud, self).__init__(credentials)

    def __generate_token(self,):
        payload = {
            "userid": self.credentials['username'],
            "password": self.credentials['password']
        }
        response = requests.post(
            url="https://{}/dbapi/v4/auth/tokens".format(self.credentials['hostname']),
            json=payload
        )

        if response.status_code == 200:
            return response.json()['token']

    def execute_sql_query(self, query):
        raise NotImplemented

    def delete_schema(self, schema):
        raise NotImplemented

    def create_schema(self, schema):
        raise NotImplemented

    def list_tables_in_schema(self, schema):
        headers = {
            "authorization": "Bearer {}".format(self.__generate_token()),
            "content-type": "application/json"
        }

        response = requests.get(
            url="https://{}/dbapi/v4/schemas/{}/tables".format(
                self.credentials['hostname'],
                schema
            ),
            headers=headers
        )

        if response.status_code != 200:
            return []

        tables_list = []
        resources = response.json()['resources']
        for res in resources:
            tables_list.append(res['name'])

        return tables_list

    def get_table_data(self, table, schema):
        headers = {
            "authorization": "Bearer {}".format(self.__generate_token()),
            "content-type": "application/json"
        }
        response = requests.get(
            url="https://{}/dbapi/v4/admin/schemas/{}/tables/{}/data?rows_return=1000".format(
                self.credentials['hostname'],
                schema,
                table
            ),
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            print(response.text)

    def get_views_in_schema(self, schema):
        headers = {
            "authorization": "Bearer {}".format(self.__generate_token()),
            "content-type": "application/json"
        }
        payload = {"search_name": "", "rows_return": 100, "show_systems": False, "obj_type": "view",
                   "sort": {"field": "view_name", "is_ascend": True}, "schemas": [{"name": schema}],
                   "filters_match": "ALL", "filters": []}
        response = requests.post(
            url="https://{}/dbapi/v4/admin/views".format(
                self.credentials['hostname']
            ),
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return response.json()

    def drop_views_in_schema(self, views, schema):
        headers = {
            "authorization": "Bearer {}".format(self.__generate_token()),
            "content-type": "application/json"
        }

        payload = []

        for view in views:
            payload.append({
                "schema": view['view_schema'],
                "view": view['view_name']
            })

        response = requests.delete(
            url="https://{}/dbapi/v4/admin/views".format(
                self.credentials['hostname']
            ),
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return

    def drop_tables_in_schema(self, tables, schema):
        headers = {
            "authorization": "Bearer {}".format(self.__generate_token()),
            "content-type": "application/json"
        }

        payload = []

        for table in tables:
            payload.append({
                "schema": schema,
                "table": table
            })

        response = requests.delete(
            url="https://{}/dbapi/v4/admin/tables".format(
                self.credentials['hostname']
            ),
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return
