# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


from .configuration import *


def _check_for_payload_logging_error_table(database, subscription_uid):
    tables = database.list_tables_in_schema(schema=get_schema_name())
    payload_error_table_name = "{}_{}".format("PayloadError", subscription_uid)

    if payload_error_table_name in tables:
        return True
    else:
        return False


def _print_payload_logging_error_table_content(database, subscription_uid):
    payload_error_table_name = "{}_{}".format("PayloadError", subscription_uid)

    if _check_for_payload_logging_error_table(database, subscription_uid):
        print("{} content:".format(payload_error_table_name))
        print(database.get_table_data(schema=get_schema_name(), table=payload_error_table_name))


def _print_measurement_facts_table_content(database,):
    measurement_facts_table_name = "MeasurementFacts"

    print("{} content:".format(measurement_facts_table_name))
    print(database.get_table_data(schema=get_schema_name(), table=measurement_facts_table_name))


def wait_for_payload_table(subscription, payload_records):
    print("Waiting {} seconds for payload records on {} env".format(get_payload_timeout(), get_env()))
    rows = subscription.payload_logging.get_records_count()

    database = get_database()
    start_time = time.time()
    elapsed_time = 0

    while rows < payload_records and elapsed_time < get_payload_timeout():
        time.sleep(10)
        rows = subscription.payload_logging.get_records_count()

        if _check_for_payload_logging_error_table(database, subscription.uid):
            _print_payload_logging_error_table_content(database, subscription.uid)
            import unittest
            tc = unittest.TestCase()
            tc.fail("PayloadError table found for subscription: {}".format(subscription.uid))

        elapsed_time = time.time() - start_time

    if rows != payload_records:
        print("--> After {} seconds only {} of {} records stored in payload - timout !!!".format(
            get_payload_timeout(),
            rows,
            payload_records))
    else:
        print("--> All payload rows stored.")


def wait_for_performance_table(subscription):
    print("Waiting {} seconds for performance records...".format(get_performance_timeout()))
    rows = subscription.performance_monitoring._get_data_from_rest_api()

    start_time = time.time()
    elapsed_time = 0

    while len(rows) == 0 and elapsed_time < get_performance_timeout():
        time.sleep(10)
        rows = subscription.performance_monitoring._get_data_from_rest_api()
        elapsed_time = time.time() - start_time

    if len(rows) == 0:
        print("--> After {} seconds only performance table is still empty - timout !!!".format(get_performance_timeout()))
        _print_measurement_facts_table_content(database=get_database())


def wait_for_feedback_table(subscription, feedback_records):
    print("Waiting {} seconds for feedback records...".format(get_feedback_payload_timeout()))
    rows = subscription.feedback_logging._get_data_from_rest_api()

    start_time = time.time()
    elapsed_time = 0

    while len(rows) != feedback_records and elapsed_time < get_feedback_payload_timeout():
        time.sleep(5)
        rows = subscription.feedback_logging._get_data_from_rest_api()
        elapsed_time = time.time() - start_time

    if len(rows) != feedback_records:
        print("--> After {} seconds only {} of {} feedback records stored in payload - timout !!!".format(
            get_feedback_payload_timeout(),
            len(rows),
            feedback_records))


def wait_until_deleted(ai_client, binding_uid=None, subscription_uid=None, data_mart=None):
    uids_sum = sum([1 if b else 0 for b in [binding_uid, subscription_uid, data_mart]])

    if uids_sum > 1:
        raise Exception('More than one uid passed.')
    elif uids_sum == 0:
        raise Exception('No uids passed.')

    def can_be_found():
        if binding_uid is not None:
            try:
                print(ai_client.data_mart.bindings.get_details(binding_uid))
                return True
            except:
                return False
        elif subscription_uid is not None:
            try:
                print(ai_client.data_mart.subscriptions.get_details(subscription_uid))
                return True
            except:
                return False
        elif data_mart is not None:
            try:
                print(ai_client.data_mart.get_details())
                return True
            except Exception as e:
                print(e)
                return False

    import time

    print('Waiting for {} to delete...'.format(
        'binding with uid=\'{}\''.format(binding_uid) if binding_uid is not None
        else 'subscription with uid=\'{}\''.format(subscription_uid) if subscription_uid is not None
        else 'data_mart'
    ), end='')

    iterator = 0

    while can_be_found() and iterator < 20:
        time.sleep(3)
        print('.', end='')
        iterator += 1

    print(' DELETED')


def wait_for_business_app(url_get_details, headers, busines_app_timeout = 15):
    def get_details(url_get_details, headers):
        response = requests.get(url=url_get_details,
                            headers=headers)
        if(response.status_code == 200):
            print(response.status_code)
            business_app_details = response.json()
        return business_app_details

    business_app_details = get_details(url_get_details, headers)
    start_time = time.time()
    elapsed_time = 0

    while business_app_details['entity']['status']['state'] != 'active' and elapsed_time < busines_app_timeout:
        time.sleep(1)
        business_app_details = get_details(url_get_details, headers)
        elapsed_time = time.time() - start_time

    if elapsed_time >= busines_app_timeout:
        print("Waiting for business application details more than {} seconds - TIMEOUT".format(elapsed_time))

    return business_app_details


def wait_for_records_in_data_set(url_get_data_set_records, headers, data_set_records, waiting_timeout = 75):

    def get_data_set_records(url_get_data_set_records, headers):
        if 'include_total_count' not in url_get_data_set_records:
            additional_sign = '?' if '?' not in url_get_data_set_records else '&'
            url = url_get_data_set_records+additional_sign+'include_total_count=true'
        else:
            url = url_get_data_set_records
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()['total_count']
        else:
            print(response.status_code)
            print(response.json())
            return response.json()

    data_set_records_count = get_data_set_records(url_get_data_set_records, headers)
    start_time = time.time()
    elapsed_time = 0

    while data_set_records_count < data_set_records and elapsed_time < waiting_timeout:
        time.sleep(10)
        data_set_records_count = get_data_set_records(url_get_data_set_records, headers)
        elapsed_time = time.time() - start_time

    if data_set_records_count < data_set_records:
        print("Loaded only {} records in {} sec - TIMEOUT".format(data_set_records_count, elapsed_time))

    return data_set_records_count


def wait_for_monitor_instance(run_url, headers, run_id,  waiting_timeout=430):
    run_url = run_url + "/" + run_id

    def get_run_details(url, headers):
        response = requests.get(
            url=url,
            headers=headers
        )
        return response.json()

    run_monitor_details = get_run_details(run_url, headers)
    status = run_monitor_details['entity']['status']['state']

    start_time = time.time()
    elapsed_time = 0

    while status != 'finished' and elapsed_time < waiting_timeout and status != 'error':
        time.sleep(5)
        run_monitor_details = get_run_details(run_url, headers)
        status = run_monitor_details['entity']['status']['state']
        elapsed_time = time.time() - start_time

    if elapsed_time >= waiting_timeout:
        print("Metrics calculation timeout, waiting more than: {} \n RUN MONITOR DETAILS: {}".format(
            elapsed_time, run_monitor_details))
    return run_monitor_details
