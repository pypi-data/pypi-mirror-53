# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from .configuration import *


def _clean_up_openscale(ai_client):
    for uid in ai_client.data_mart.subscriptions.get_uids():
        print('Deleting \'{}\' subscription.'.format(uid))
        try:
            ai_client.data_mart.subscriptions.delete(uid)
        except Exception as e:
            print('Deleting of subscription failed:', e)

    for uid in ai_client.data_mart.bindings.get_uids():
        try:
            ai_client.data_mart.bindings.delete(uid)
        except:
            pass
    try:
        ai_client.data_mart.delete()
    except:
        pass


def _clean_up_database(internal=False):
    if internal:
        return

    schema_name = get_schema_name()

    database = get_database()

    if isinstance(database, PostgresDatabase):
        database.delete_schema(schema_name)
        database.create_schema(schema_name)

    elif isinstance(database, DB2DatabaseICP):
        tables_drop_query = database.execute_sql_query(
            query=""" select 'DROP TABLE "'||rtrim(tabschema)||'"."'||rtrim(tabname)||'"' from syscat.tables where OWNER = 'DB2INST1' and TABSCHEMA = '{}' and type = 'T' """.format(
                schema_name))
        views_drop_query = database.execute_sql_query(
            query=""" select 'DROP VIEW "'||rtrim(tabschema)||'"."'||rtrim(tabname)||'"' from syscat.tables where OWNER = 'DB2INST1' and TABSCHEMA = '{}' and type = 'V' """.format(
                schema_name))

        for table_query in tables_drop_query:
            database.execute_sql_query(query=table_query)

        for view_query in views_drop_query:
            database.execute_sql_query(query=view_query)

    elif isinstance(database, DB2DatabaseCloud):
        m_tables = database.list_tables_in_schema(schema_name)
        m_views = database.get_views_in_schema(schema_name)
        database.drop_views_in_schema(m_views, schema_name)
        database.drop_tables_in_schema(m_tables, schema_name)


def prepare_env(ai_client, internal=False):
    if is_manual_cleanup():
        return

    _clean_up_openscale(ai_client)
    _clean_up_database(internal=internal)


def clean_up_env(ai_client):
    if is_manual_cleanup():
        return

    _clean_up_openscale(ai_client)


def clean_wml_instance(model_id, deployment_id, binding_id=None):
    print("Cleaning WML instance ...")
    if binding_id is not None:
        from ibm_ai_openscale import APIClient
        ai_client = APIClient(get_aios_credentials())
        wml_client = ai_client.data_mart.bindings.get_native_engine_client(binding_id)
    else:
        wml_client = get_client()

    print("Deleting deployment: {}".format(deployment_id))
    wml_client.deployments.delete(deployment_id)

    print("Deleting model: {}".format(model_id))
    wml_client.repository.delete(model_id)

    # if "ICP" in get_env():
    #     clean_up_wml_instance()


def clean_up_wml_instance():
    wml_client = get_client()

    print("Cleaning wml instance.")
    print("Removing all deployments...")

    for deployment in wml_client.deployments.get_details()['resources']:
        wml_client.deployments.delete(deployment['metadata']['guid'])

    details = wml_client.repository.get_details()

    print("Removing all models...")
    for model in details['models']['resources']:
        wml_client.repository.delete(model['metadata']['guid'])

    print("Removing all runtimes...")
    for runtime in details['runtimes']['resources']:
        wml_client.repository.delete(runtime['metadata']['guid'])

    # print("Removing definitions...")
    # for definition in details['definitions']['resources']:
    #     wml_client.repository.delete(definition['metadata']['guid'])

    print("Cleaning done.")


def clean_up_wml_instance_spss(wml_client):
    env_clean = False
    try:
        details = wml_client.repository.get_details()

        for deployment in details['deployments']['resources']:
            if "spss" in str(deployment['entity']['runtime_environment']).lower():
                print("Removing spss deployment: {}".format(deployment))
                wml_client.deployments.delete(deployment['metadata']['guid'])

        for model in details['models']['resources']:
            if "spss" in str(model['entity']['runtime_environment']).lower():
                print("Removing spss model: {}".format(model))
                wml_client.repository.delete(model['metadata']['guid'])

        env_clean = True

    except Exception as ex:
        print("First cleanup failed. Trying the second approach\n{}".format(ex))

    if not env_clean:
        try:
            models = wml_client._models.get_details()
            deployments = wml_client.deployments.get_details()

            for deployment in deployments['resources']:
                if "spss" in str(deployment['entity']['runtime_environment']).lower():
                    print("Removing spss deployment: {}".format(deployment))
                    wml_client.deployments.delete(deployment['metadata']['guid'])

            for model in models['resources']:
                if "spss" in str(model['entity']['runtime_environment']).lower():
                    print("Removing spss model: {}".format(model))
                    wml_client.repository.delete(model['metadata']['guid'])

        except Exception as ex:
            print("Second cleanup failed.\n{}".format(ex))
