# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import pandas as pd

from utils.assertions import *
from utils.cleanup import *
from utils.waits import *
from utils.deployments import GermanCreditRisk

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType, FeedbackFormat

from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2
from ibm_ai_openscale.utils.inject_demo_data import DemoData


DAYS = 7
RECORDS_PER_DAY = 2880


class TestAIOpenScaleClient(unittest.TestCase):
    hrefs_v2 = None
    log_loss_random = None
    brier_score_loss = None
    application_instance_id = None
    drift_instance_id = None
    data_set_id = None
    ai_client = None
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    b_app_uid = None
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
    correlation_run_id = None
    correlation_monitor_uid = 'correlations'
    measurement_details = None
    transaction_id = None
    business_payload_records = 0
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

    def test_05_get_model_ids(self):
        TestAIOpenScaleClient.model_uid = self.deployment.get_asset_id()
        TestAIOpenScaleClient.deployment_uid = self.deployment.get_deployment_id()

    def test_06_subscribe(self):
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
                                 'Housing', 'Job', 'Telephone', 'ForeignWorker'],
            training_data_reference=get_cos_training_data_reference()
        ))

        TestAIOpenScaleClient.subscription_uid = subscription.uid

        print("Subscription details: {}".format(subscription.get_details()))

    def test_07_select_subscription(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)

    def test_08_define_business_app(self):
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
                            "default": 502,
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
            ],
        }

        response = requests.post(url=self.hrefs_v2.get_applications_href(),
                                 headers=TestAIOpenScaleClient.ai_client._get_headers(), json=payload)
        print(response.status_code, response.json())
        self.assertEqual(response.status_code, 202)
        TestAIOpenScaleClient.b_app_uid = response.json()['metadata']['id']
        self.assertIsNotNone(TestAIOpenScaleClient.b_app_uid)

    def test_09_get_application_details(self):
        application_details = wait_for_business_app(url_get_details=self.hrefs_v2.get_application_details_href(TestAIOpenScaleClient.b_app_uid),
                                 headers=TestAIOpenScaleClient.ai_client._get_headers())
        print(application_details)

    def test_10_enable_drift(self):
        self.subscription.drift_monitoring.enable(threshold=0.6, min_records=10, model_path=os.path.join(self.drift_model_path, self.drift_model_name))
        drift_monitor_details = self.subscription.monitoring.get_details(monitor_uid='drift')
        print('drift monitor details', drift_monitor_details)

    def test_11_list_monitors_instances(self):
        self.ai_client.data_mart.monitors.list()
        time.sleep(5)
        response = requests.get(url=self.hrefs_v2.get_monitor_instances_href(), headers=self.ai_client._get_headers())
        print(response.json())
        instances = response.json()['monitor_instances']

        for instance in instances:
            if 'managed_by' in instance['entity'] and instance['entity']['managed_by'] == self.b_app_uid:
                TestAIOpenScaleClient.application_instance_id = instance['metadata']['id']

            if instance['entity']['monitor_definition_id'] == 'correlations':
                TestAIOpenScaleClient.corr_monitor_instance_id = instance['metadata']['id']

            if instance['entity']['monitor_definition_id'] == 'drift':
                TestAIOpenScaleClient.drift_instance_id = instance['metadata']['id']

        self.assertIsNotNone(TestAIOpenScaleClient.application_instance_id)
        self.assertIsNotNone(TestAIOpenScaleClient.corr_monitor_instance_id)
        self.assertIsNotNone(TestAIOpenScaleClient.drift_instance_id)
        print('application_instance_id', self.application_instance_id)
        print('corr_monitor_instance_id', self.corr_monitor_instance_id)
        print('drift_instance_id', self.drift_instance_id)

    def test_12_load_historical_bkpis(self):
        self.hd.load_historical_kpi_measurements(
            file_path=TestAIOpenScaleClient.historical_data_path,
            monitor_instance_id=self.application_instance_id,
        )
        time.sleep(3)

    def test_13_get_historical_kpi(self):
        query = '?start=2018-01-23T12:46:55.677590Z&end=2019-12-04T12:46:55.677590Z&limit=1000'
        metrics_url = self.hrefs_v2.get_measurements_href(self.application_instance_id) + query
        response = requests.get(url=metrics_url, headers=self.ai_client._get_headers())
        print(response.json())
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json()['measurements'])

    def test_14_store_drift_measurements(self):
        self.hd.load_historical_drift_measurements(
            file_path=TestAIOpenScaleClient.historical_data_path,
            monitor_instance_id=self.drift_instance_id,
            business_application_id=self.b_app_uid)
        time.sleep(3)

    def test_15_get_drift_measurements(self):
        query = '?start=2018-01-23T12:46:55.677590Z&end=2019-12-04T12:46:55.677590Z'
        metrics_url = self.hrefs_v2.get_measurements_href(self.drift_instance_id) + query
        response = requests.get(url=metrics_url, headers=self.ai_client._get_headers())

        print(response.json())
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json()['measurements'])

    def test_16_run_correlation_monitor(self):
        time.sleep(30)

        payload = {
            "triggered_by": "user",
            "parameters": {
                "max_number_of_days": "1000"
            },
            "business_metric_context": {
                "business_application_id": TestAIOpenScaleClient.b_app_uid,
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

    def test_17_check_correlations_metrics(self):
        run_url = self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.corr_monitor_instance_id)
        print(run_url)
        final_run_details = wait_for_monitor_instance(run_url, run_id=self.correlation_run_id, headers=self.ai_client._get_headers())
        self.assertIsNot(final_run_details['entity']['status']['state'], 'error',
                         msg="Error during computing correlations. Run details: {}".format(final_run_details))

        query = '?start=2018-01-23T12:46:55.677590Z&end=2019-12-04T12:46:55.677590Z'
        url = self.hrefs_v2.get_measurements_href(TestAIOpenScaleClient.corr_monitor_instance_id) + query
        print(url)
        print(final_run_details)

        response = requests.get(url=url, headers=self.ai_client._get_headers())

        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('significant_coefficients' in str(response.json()))

        corr_metrics = response.json()['measurements'][0]['entity']['values'][0]['metrics']
        self.assertGreater([metric['value'] for metric in corr_metrics if metric['id'] == 'significant_coefficients'][0], 0,
                           msg="No significant coefficients")

    @classmethod
    def tearDownClass(cls):
        clean_up_env(cls.ai_client)


if __name__ == '__main__':
    unittest.main()
