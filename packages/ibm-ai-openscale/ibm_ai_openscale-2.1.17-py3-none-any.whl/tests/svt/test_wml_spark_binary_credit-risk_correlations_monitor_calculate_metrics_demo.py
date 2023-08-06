# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import pandas as pd
import datetime

from utils.assertions import *
from utils.cleanup import *
from utils.waits import *
from utils.deployments import GermanCreditRisk

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *

from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2
from ibm_ai_openscale.utils.inject_demo_data import DemoData
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType


DAYS = 7
RECORDS_PER_DAY = 2880


class TestAIOpenScaleClient(unittest.TestCase):
    hrefs_v2 = None
    log_loss_random = None
    brier_score_loss = None
    business_metrics_monitor_instance_id = None
    drift_instance_id = None
    business_data_set_id = None
    transaction_batches_data_set_id = None
    scoring_payload_data_set_id = None
    ai_client = None
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    business_application_id = None
    x_uid = None
    labels = None
    corr_monitor_instance_id = None
    variables = None
    wml_client = None
    subscription = None
    binding_uid = None
    deployment = None

    scoring_result = None
    payload_scoring = None
    published_model_details = None
    monitor_uid = None
    source_uid = None
    correlation_monitor_uid = 'correlations'
    measurement_details = None
    transaction_id = None
    business_payload_records = 0
    business_metrics_ids = None
    correlation_monitor_run_id = None
    business_metrics_monitor_run_id = None

    drift_model_name = "drift_detection_model.tar.gz"
    drift_model_path = os.path.join(os.getcwd(), 'artifacts', 'drift_models')
    historical_data_path = os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'historical_records')
    data_df = pd.read_csv(
        "./datasets/German_credit_risk/credit_risk_training.csv",
        dtype={'LoanDuration': int, 'LoanAmount': int, 'InstallmentPercent': int, 'CurrentResidenceDuration': int,
               'Age': int, 'ExistingCreditsCount': int, 'Dependents': int})

    test_uid = str(uuid.uuid4())


    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.hrefs_v2 = AIHrefDefinitionsV2(cls.aios_credentials)
        cls.database_credentials = get_database_credentials()
        cls.hd = DemoData(cls.aios_credentials)
        cls.database_credentials = get_database_credentials()
        cls.deployment = GermanCreditRisk()


        if "ICP" in get_env():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
            # upload_credit_risk_training_data_to_db2(cls.database_credentials)

        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

        prepare_env(cls.ai_client)

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_bind_wml_instance(self):
        if "ICP" in get_env():
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on ICP", WatsonMachineLearningInstance4ICP())
        else:
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on Cloud", WatsonMachineLearningInstance(self.wml_credentials))

    def test_03_get_model_ids(self):
        TestAIOpenScaleClient.model_uid = self.deployment.get_asset_id()
        TestAIOpenScaleClient.deployment_uid = self.deployment.get_deployment_id()

    def test_04_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(
            source_uid=TestAIOpenScaleClient.model_uid,
            binding_uid=self.binding_uid,
            problem_type=ProblemType.BINARY_CLASSIFICATION,
            input_data_type=InputDataType.STRUCTURED,
            prediction_column='predictedLabel',
            probability_column='probability',
            feature_columns=['CheckingStatus', 'LoanDuration', 'CreditHistory', 'LoanPurpose', 'LoanAmount',
                             'ExistingSavings', 'EmploymentDuration', 'InstallmentPercent', 'Sex', 'OthersOnLoan',
                             'CurrentResidenceDuration', 'OwnsProperty', 'Age', 'InstallmentPlans', 'Housing',
                             'ExistingCreditsCount', 'Job', 'Dependents', 'Telephone', 'ForeignWorker'],
            categorical_columns=['CheckingStatus', 'CreditHistory', 'LoanPurpose', 'ExistingSavings',
                                 'EmploymentDuration', 'Sex', 'OthersOnLoan', 'OwnsProperty', 'InstallmentPlans',
                                 'Housing', 'Job', 'Telephone', 'ForeignWorker']
        ))

        TestAIOpenScaleClient.subscription_uid = subscription.uid

    def test_07_select_subscription(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)

    def test_08a_payload_logging_update(self):
        self.subscription.payload_logging.enable(dynamic_schema_update=True)
        payload_logging_details = self.subscription.payload_logging.get_details()
        assert_payload_logging_configuration(payload_logging_details=payload_logging_details)

    def test_08b_set_transaction_id_field(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        asset_properties = subscription_details['entity']['asset_properties']
        asset_properties['transaction_id_field'] = 'transaction_id'

        response = requests.patch(
            '{}/v1/data_marts/{}/service_bindings/{}/subscriptions/{}'.format(
                TestAIOpenScaleClient.ai_client._service_credentials['url'],
                TestAIOpenScaleClient.ai_client._service_credentials['data_mart_id'],
                TestAIOpenScaleClient.subscription.binding_uid,
                TestAIOpenScaleClient.subscription_uid
            ),
            headers=TestAIOpenScaleClient.ai_client._get_headers(),
            json=[{
                'op': 'replace',
                'path': '/asset_properties',
                'value': asset_properties
            }]
        )
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_09_load_historical_scoring_payload(self):
        self.hd.load_historical_scoring_payload(TestAIOpenScaleClient.subscription, TestAIOpenScaleClient.deployment_uid,
                                                TestAIOpenScaleClient.historical_data_path, day_template="history_correlation_payloads_{}.json" )

    def test_10_stats_on_payload_logging_table(self):
        wait_for_payload_table(subscription=self.subscription, payload_records=RECORDS_PER_DAY*DAYS)

        TestAIOpenScaleClient.subscription.payload_logging.show_table(limit=5)
        records_no = TestAIOpenScaleClient.subscription.payload_logging.get_records_count()

        print("Rows count in payload logging table", records_no)

    def test_11a_get_data_sets(self):

        response = requests.get(
            self.hrefs_v2.get_data_sets_href(),
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )

        self.assertEqual(response.status_code, 200)
        print("DATASETS", response.json())

        scoring_payload_data_set_details = [x for x in response.json()['data_sets'] if x['entity']['type'] == 'payload_logging'][0]
        TestAIOpenScaleClient.scoring_payload_data_set_id = scoring_payload_data_set_details['metadata']['id']

        response = requests.get(
            self.hrefs_v2.get_data_set_details_href(TestAIOpenScaleClient.scoring_payload_data_set_id),
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )

        self.assertEqual(response.status_code, 200)
        print("PAYLOAD DATASET:", response.json())

        self.assertIn('transaction_id_key', response.text, msg="Transaction_id_key is not set in payload data set.")

    def test_11b_get_subscription_details(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))
        self.assertIn('transaction_id_key', str(subscription_details), msg="transaction_id_key not found set in subscription details")

    def test_12_define_business_app(self):
        payload = {
            "name": "Credit Risk Application",
            "description": "Test Business Application",
            "payload_fields": [
                {
                    "name": "LoanDuration",
                    "type": "number",
                    "description": "Duration of the loan"
                },
                {
                    "name": "LoanPurpose",
                    "type": "string",
                    "description": "Purpose of the loan"
                },
                {
                    "name": "LoanAmount",
                    "type": "number",
                    "description": "Amount of the loan"
                },
                {
                    "name": "InstallmentPercent",
                    "type": "number",
                    "description": "Installment percents"
                },
                {
                    "name": "AcceptedPercent",
                    "type": "number"
                },
                {
                    "name": "AmountGranted",
                    "type": "number",
                    "description": "Risk percent"
                },
                {
                    "name": "Accepted",
                    "type": "number",
                    "description": "Number of loans accepted"
                }
            ],
            "business_metrics": [
                {
                    "name": "Accepted Credits",
                    "description": "Accepted Credits Daily",
                    "expected_direction": "increasing",
                    "thresholds": [
                        {
                            "type": "lower_limit",
                            "default": 55,
                            "default_recommendation": "string"
                        }
                    ],
                    "required": False,
                    "calculation_metadata": {
                        "field_name": "Accepted",
                        "aggregation": "sum",
                        "time_frame": {
                            "count": 1,
                            "unit": "day"
                        }
                    }
                },
                {
                    "name": "Credit Amount Granted",
                    "description": "Credit Amount Granted Daily",
                    "expected_direction": "increasing",
                    "thresholds": [
                        {
                            "type": "lower_limit",
                            "default": 1000,
                            "default_recommendation": "string"
                        }
                    ],
                    "required": False,
                    "calculation_metadata": {
                        "field_name": "AmountGranted",
                        "aggregation": "sum",
                        "time_frame": {
                            "count": 1,
                            "unit": "day"
                        }
                    }
                }
            ],
            "subscription_ids": [
                TestAIOpenScaleClient.subscription_uid
            ]
        }

        response = requests.post(url=self.hrefs_v2.get_applications_href(),
                                 headers=TestAIOpenScaleClient.ai_client._get_headers(),
                                 json=payload)
        print(response.status_code, response.json())
        self.assertEqual(response.status_code, 202)
        TestAIOpenScaleClient.business_application_id = response.json()['metadata']['id']
        TestAIOpenScaleClient.business_metrics_ids = [b_metric['id'] for b_metric in response.json()['entity']['business_metrics']]
        self.assertIsNotNone(TestAIOpenScaleClient.business_application_id)

    def test_13_get_application_details(self):
        application_details = wait_for_business_app(
            url_get_details=self.hrefs_v2.get_application_details_href(TestAIOpenScaleClient.business_application_id),
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )
        print(application_details)

    def test_14_enable_drift(self):
        self.subscription.drift_monitoring.enable(threshold=0.6, min_records=10,
                                                  model_path=os.path.join(self.drift_model_path, self.drift_model_name))
        drift_monitor_details = self.subscription.monitoring.get_details(monitor_uid='drift')
        print('drift monitor details', drift_monitor_details)

    def test_15_list_monitors_instances(self):
        self.ai_client.data_mart.monitors.list()
        time.sleep(5)
        response = requests.get(url=self.hrefs_v2.get_monitor_instances_href(), headers=self.ai_client._get_headers())
        print(response.status_code, response.json())
        self.assertEqual(response.status_code, 200)
        instances = response.json()['monitor_instances']

        for instance in instances:
            if 'managed_by' in instance['entity'] and instance['entity']['managed_by'] == self.business_application_id:
                if instance['entity']['monitor_definition_id'] not in ('correlations', 'drift'):
                    TestAIOpenScaleClient.business_metrics_monitor_instance_id = instance['metadata']['id']

            if instance['entity']['monitor_definition_id'] == 'correlations':
                TestAIOpenScaleClient.corr_monitor_instance_id = instance['metadata']['id']

            if instance['entity']['monitor_definition_id'] == 'drift':
                TestAIOpenScaleClient.drift_instance_id = instance['metadata']['id']

        self.assertIsNotNone(TestAIOpenScaleClient.business_metrics_monitor_instance_id)
        self.assertIsNotNone(TestAIOpenScaleClient.corr_monitor_instance_id)
        self.assertIsNotNone(TestAIOpenScaleClient.drift_instance_id)

        print('business_metrics_monitor_instance_id', self.business_metrics_monitor_instance_id)
        print('corr_monitor_instance_id', self.corr_monitor_instance_id)
        print('drift_instance_id', self.drift_instance_id)

    def test_16_get_business_payload_data_set_details(self):
        response = requests.get(url=self.hrefs_v2.get_data_sets_href(), headers=self.ai_client._get_headers())
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

        data_sets = response.json()['data_sets']
        print(data_sets)

        TestAIOpenScaleClient.business_data_set_id = \
            [ds['metadata']['id'] for ds in data_sets if ds['entity']['type'] == 'business_payload'][0]
        print("business_payload data_set id: {}".format(TestAIOpenScaleClient.business_data_set_id))

    def test_17_correct_schema(self):

        response = requests.patch(
            self.hrefs_v2.get_data_set_details_href(self.business_data_set_id),
            headers=TestAIOpenScaleClient.ai_client._get_headers(),
            json=[{
                'op': 'replace',
                'path': '/schema_update_mode',
                'value': 'none'
            }]
        )

        print(response.status_code)
        print("DATASETS", response.json())

        self.assertEqual(200, response.status_code)

    def test_18_insert_business_payload(self):
        self.hd.load_historical_business_payload(
            file_path=TestAIOpenScaleClient.historical_data_path,
            data_set_id=TestAIOpenScaleClient.business_data_set_id,
            file_name="history_business_payloads_week.csv"
        )
        TestAIOpenScaleClient.business_payload_records = RECORDS_PER_DAY*DAYS

    def test_19_stats_on_business_payload_data(self):
        business_records_no = wait_for_records_in_data_set(
            url_get_data_set_records=self.hrefs_v2.get_data_set_records_href(TestAIOpenScaleClient.business_data_set_id),
            headers=self.ai_client._get_headers(),
            data_set_records=self.business_payload_records,
            waiting_timeout=270
        )
        self.assertEqual(self.business_payload_records, business_records_no)

    def test_20_run_business_application(self):
        run_url = self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.business_metrics_monitor_instance_id)
        response = requests.post(
            url=run_url,
            headers=TestAIOpenScaleClient.ai_client._get_headers(),
            json={}
        )
        print(response.status_code)
        print(response.json())
        self.assertEqual(response.status_code, 201)

        TestAIOpenScaleClient.business_metrics_monitor_run_id = response.json()['metadata']['id']

        final_run_details = wait_for_monitor_instance(run_url,
                                                      run_id=TestAIOpenScaleClient.business_metrics_monitor_run_id,
                                                      headers=self.ai_client._get_headers())
        print(final_run_details)
        self.assertIsNot(final_run_details['entity']['status']['state'], 'failure',
                         msg="Error during computing BKPIs. Run details: {}".format(final_run_details))

    def test_21_get_bkpis(self):
        query = '?start=2018-01-23T12:46:55.677590Z&end={}Z'.format(datetime.datetime.utcnow().isoformat())
        url = self.hrefs_v2.get_measurements_href(TestAIOpenScaleClient.business_metrics_monitor_instance_id) + query
        print(url)
        response = requests.get(url=url, headers=self.ai_client._get_headers())

        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        print("Measurements: ", response.json())

    def test_22a_get_drift_runs(self):
        run_drift_url = self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.drift_instance_id)
        response = requests.get(
            url=self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.drift_instance_id),
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )
        print(response.status_code)
        print(response.json())

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()['runs']), 0, msg="No drift runs")

        drift_run_details = response.json()['runs']
        print(drift_run_details[0]['entity']['status']['state'])
        final_drift_run_details = wait_for_monitor_instance(run_drift_url,
                                  headers=TestAIOpenScaleClient.ai_client._get_headers(),
                                  run_id=drift_run_details[0]['metadata']['id'],
                                  waiting_timeout=120)
        print("final_drift_run_details", final_drift_run_details)

    def test_22b_get_drift_measurements(self):
        query = '?start=2018-01-23T12:46:55.677590Z&end={}Z'.format(datetime.datetime.utcnow().isoformat())
        url = self.hrefs_v2.get_measurements_href(TestAIOpenScaleClient.drift_instance_id) + query
        print(url)
        response = requests.get(url=url, headers=self.ai_client._get_headers())

        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        print("Measurements: ", response.json())

    def test_23_run_correlation_monitor(self):
        time.sleep(20)

        payload = {
            "triggered_by": "user",
            "parameters": {
                "max_number_of_days": "1000"
            },
            "business_metric_context": {
                "business_application_id": TestAIOpenScaleClient.business_application_id,
                "metric_id": "",
                "transaction_data_set_id": "",
                "transaction_batch_id": ""
            }
        }

        response = requests.post(
            url=self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.corr_monitor_instance_id),
            json=payload,
            headers=TestAIOpenScaleClient.ai_client._get_headers())

        print(response.json())
        self.assertEqual(response.status_code, 201)

        TestAIOpenScaleClient.correlation_run_id = response.json()['metadata']['id']

    def test_24_check_correlations_metrics(self):
        run_url = self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.corr_monitor_instance_id)
        final_run_details = wait_for_monitor_instance(run_url, run_id=self.correlation_run_id,
                                                      headers=self.ai_client._get_headers())
        self.assertIsNot(final_run_details['entity']['status']['state'], 'error',
                         msg="Error during computing correlations. Run details: {}".format(final_run_details))
        print(final_run_details)

        query = '?start=2018-01-23T12:46:55.677590Z&end=2019-12-04T12:46:55.677590Z'
        url = self.hrefs_v2.get_measurements_href(TestAIOpenScaleClient.corr_monitor_instance_id) + query
        print(url)
        response = requests.get(url=url, headers=self.ai_client._get_headers())
        print(response.json())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('significant_coefficients' in str(response.json()))

        corr_metrics = response.json()['measurements'][0]['entity']['values'][0]['metrics']
        self.assertGreater([metric['value'] for metric in corr_metrics if metric['id'] == 'significant_coefficients'][0]
                           , 0, msg="No significant coefficients")

    @classmethod
    def tearDownClass(cls):
        clean_up_env(cls.ai_client)


if __name__ == '__main__':
    unittest.main()
