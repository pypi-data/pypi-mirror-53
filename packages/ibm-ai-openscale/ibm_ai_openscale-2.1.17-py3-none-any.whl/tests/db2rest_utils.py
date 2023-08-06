import requests
import time

def generate_token(db2_credentials):
    payload = {
      "userid": db2_credentials['username'],
      "password": db2_credentials['password']
    }
    response = requests.post(
        url="https://{}/dbapi/v4/auth/tokens".format(db2_credentials['hostname']),
        json=payload
    )

    if response.status_code == 200:
        return response.json()['token']


def get_tables_in_schema(token, db2_credentials):
    headers = {
        "authorization": "Bearer {}".format(token),
        "content-type": "application/json"
    }

    response = requests.get(
        url="https://{}/dbapi/v4/schemas/{}/tables".format(
            db2_credentials['hostname'],
            'AIOPSSVT'
        ),
        headers=headers
    )

    print(response.status_code)
    if response.status_code == 200:
        return response.json()['resources']


def get_views_in_schema(token, db2_credentials):
    headers = {
        "authorization": "Bearer {}".format(token),
        "content-type": "application/json"
    }
    payload = {"search_name":"","rows_return":100,"show_systems":False,"obj_type":"view","sort":{"field":"view_name","is_ascend":True},"schemas":[{"name":"AIOPSSVT"}],"filters_match":"ALL","filters":[]}
    response = requests.post(
        url="https://{}/dbapi/v4/admin/views".format(
            db2_credentials['hostname']
        ),
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()


def drop_views_in_schema(token, views, db2_credentials, repeated=0):
    headers = {
        "authorization": "Bearer {}".format(token),
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
            db2_credentials['hostname']
        ),
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return
    elif repeated > 5:
        print("Unable to drop views after 5 requests.")
        return
    else:
        time.sleep(10)
        drop_views_in_schema(token, views, db2_credentials, repeated=(repeated+1))


def drop_tables_in_schema(token, tables, db2_credentials, repeated=0):
    headers = {
        "authorization": "Bearer {}".format(token),
        "content-type": "application/json"
    }

    payload = []

    for table in tables:
        payload.append({
            "schema": table['schema'],
            "table": table['name']
        })

    response = requests.delete(
        url="https://{}/dbapi/v4/admin/tables".format(
            db2_credentials['hostname']
        ),
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return
    else:
        time.sleep(10)
        drop_tables_in_schema(token, tables, db2_credentials, repeated=(repeated+1))


def cleanupdb2(db2_credentials):
    token = generate_token(db2_credentials)
    m_tables = get_tables_in_schema(token, db2_credentials)
    m_views = get_views_in_schema(token, db2_credentials)
    time.sleep(5)
    drop_views_in_schema(token, m_views, db2_credentials)
    time.sleep(5)
    drop_tables_in_schema(token, m_tables, db2_credentials)