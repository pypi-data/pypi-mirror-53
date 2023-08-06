# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import json
import os
import time
import requests
import uuid
from datetime import datetime
from configparser import ConfigParser
from .database import PostgresDatabase, DB2DatabaseICP, DB2DatabaseCloud


if "ENV" in os.environ:
    environment = os.environ['ENV']
else:
    environment = "YP_QA"


timeouts = "TIMEOUTS"
credentials = "CREDENTIALS"
training_data = "TRAINING_DATA"
configDir = "./config.ini"

config = ConfigParser()
config.read(configDir)


def get_env():
    return environment


def get_schema_name():
    return config.get(environment, 'schema_name')


def get_aios_credentials():
    return json.loads(config.get(environment, 'aios_credentials'))


def get_azure_credentials():
    return json.loads(config.get(credentials, 'azure_credentials'))


def get_aws_credentials():
    return json.loads(config.get(credentials, 'aws_credentials'))


def get_spss_cnds_credentials():
    return json.loads(config.get(credentials, 'spss_credentials'))


def is_manual_cleanup():
    return True if "MANCLEANUP" in os.environ else False


def is_icp():
    return True if "ICP" in get_env() else False


def is_sanity():
    return True if "SANITY" in get_env() else False


def _get_timeout(name):
    timeout = json.loads(config.get(timeouts, name))

    return timeout * 4 if is_sanity() else timeout


def get_payload_timeout():
    return _get_timeout(name='payload_timeout')


def get_performance_timeout():
    return _get_timeout(name='performance_timeout')


def get_feedback_payload_timeout():
    return _get_timeout(name='feedback_payload_timeout')


def get_quality_run_timeout():
    return _get_timeout(name='quality_run_timeout')


def get_database_credentials():
    if config.has_option(environment, 'database_credentials'):
        return json.loads(config.get(environment, 'database_credentials'))
    elif config.has_option(environment, 'postgres_credentials'):
        return get_postgres_credentials()
    elif config.has_option(environment, 'db2_datamart'):
        return get_db2_datamart_credentials()
    else:
        raise Exception("There is no database in config!")


def is_postgres_database():
    db_credentials = get_database_credentials()

    if "connection" in db_credentials.keys() and "postgres" in db_credentials['connection'].keys():
        return True

    if "db_type" in db_credentials.keys() and "postgresql" == db_credentials['db_type']:
        return True

    if 'postgres' in str(db_credentials):
        return True

    if 'dashdb' in str(db_credentials):
        return False

    if 'db2' in str(db_credentials):
        return False

    return False


def get_database():
    if is_postgres_database():
        return PostgresDatabase(credentials=get_database_credentials())
    elif is_icp():
        return DB2DatabaseICP(credentials=get_database_credentials())
    else:
        return DB2DatabaseCloud(credentials=get_database_credentials())


def get_db2_datamart_credentials():
    return json.loads(config.get(environment, 'db2_datamart'))


def get_db2_schema_name():
    return json.loads(config.get(environment, 'db2_schema'))


def get_wml_credentials(env=environment):
    return json.loads(config.get(env, 'wml_credentials'))


def get_wml_credentials_other_icp(env=environment):
    return json.loads(config.get(env, 'wml_credentials_other_icp'))


def get_postgres_credentials():
    return json.loads(config.get(environment, 'postgres_credentials'))


def get_db2_training_data_reference():
    db2_connection = json.loads(config.get(training_data, 'database_credentials'))
    db2_tablename = json.loads(config.get(training_data, 'table_name'))
    db2_schema_name = json.loads(config.get(training_data, 'schema_name'))
    return {
                'type': 'db2',
                'location': {
                    'table_name': db2_tablename,
                    'schema_name': db2_schema_name
                },
                'connection': db2_connection,
                'name': 'DB2 training data reference.'
            }


def get_cos_training_data_reference():
    cos_credentials = json.loads(config.get(training_data, 'cos_credentials'))
    bucket_name = json.loads(config.get(training_data, 'bucket_name'))
    file_name = json.loads(config.get(training_data, 'file_name'))
    return {
                'type': 'cos',
                'location': {
                    'bucket': bucket_name,
                    'file_name': file_name,
                    'firstlineheader': True,
                    'file_format': 'csv'
                },
                'connection': cos_credentials,
                'name': 'DB2 training data reference.'
            }


def get_cos_credentials():
    return json.loads(config.get(environment, 'cos_credentials'))


def get_feedback_data_reference():
    return json.loads(config.get(environment, 'feedback_data_reference'))


def get_db2_credentials():
    return json.loads(config.get(environment, 'db2_reference'))


def get_spark_reference():
    return json.loads(config.get(environment, 'spark_reference'))


def get_cos_auth_endpoint():
    return config.get(environment, 'cos_auth_endpoint')


def get_cos_service_endpoint():
    return config.get(environment, 'cos_service_endpoint')


def get_client():
    wml_lib = __import__('watson_machine_learning_client', globals(), locals())
    return wml_lib.WatsonMachineLearningAPIClient(get_wml_credentials())