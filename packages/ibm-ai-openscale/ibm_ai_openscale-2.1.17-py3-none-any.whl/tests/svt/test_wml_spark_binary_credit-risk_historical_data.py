# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from utils.assertions import *
from utils.cleanup import *
from utils.waits import *
from utils.deployments import GermanCreditRisk

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import PayloadRecord, Feature, MeasurementRecord
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType, FeedbackFormat


class TestAIOpenScaleClient(unittest.TestCase):
    transaction_id = None
    ai_client = None
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    labels = None
    wml_client = None
    subscription = None
    binding_uid = None
    deployment = None

    scoring_result = None
    payload_scoring = None
    published_model_details = None
    source_uid = None

    scoring_records = 0
    feedback_records = 0

    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()
        cls.deployment = GermanCreditRisk()

        if "ICP" in get_env():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)

        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

        prepare_env(cls.ai_client)

    def test_01_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_data_mart_get_details(self):
        details = TestAIOpenScaleClient.ai_client.data_mart.get_details()
        assert_datamart_details(details, schema=self.schema, state='active')

    def test_03_bind_wml_instance(self):
        if "ICP" in get_env():
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on ICP", WatsonMachineLearningInstance4ICP())
        else:
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on Cloud", WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_model_ids(self):
        TestAIOpenScaleClient.model_uid = self.deployment.get_asset_id()
        TestAIOpenScaleClient.deployment_uid = self.deployment.get_deployment_id()

    def test_05_subscribe(self):
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
            training_data_reference=get_db2_training_data_reference()
        ))

        TestAIOpenScaleClient.subscription_uid = subscription.uid
        TestAIOpenScaleClient.subscription = subscription

    def test_09_score(self):
        fields = ["CheckingStatus", "LoanDuration", "CreditHistory", "LoanPurpose", "LoanAmount", "ExistingSavings",
                  "EmploymentDuration", "InstallmentPercent", "Sex", "OthersOnLoan", "CurrentResidenceDuration",
                  "OwnsProperty", "Age", "InstallmentPlans", "Housing", "ExistingCreditsCount", "Job", "Dependents",
                  "Telephone", "ForeignWorker"]
        values = [
            ["no_checking", 33, "outstanding_credit", "appliances", 5696, "unknown", "greater_7", 4, "male",
             "co-applicant", 4, "unknown", 54, "none", "free", 2, "skilled", 1, "yes", "yes"],
            ["0_to_200", 13, "prior_payments_delayed", "retraining", 1375, "100_to_500", "4_to_7", 3, "male", "none", 3,
             "real_estate", 37, "none", "own", 2, "management_self-employed", 1, "none", "yes"]
        ]

        payload_scoring = {"fields": fields, "values": values}
        print("Scoring payload: {}".format(payload_scoring))

        TestAIOpenScaleClient.scoring_records = 6
        for i in range(0, int(self.scoring_records/2)):
            self.deployment.score(payload_scoring)

        wait_for_payload_table(subscription=TestAIOpenScaleClient.subscription, payload_records=self.scoring_records)

    def test_10_stats_on_payload_logging_table(self):
        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['prediction', 'probability'])

    def test_11_setup_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.8, min_records=5)

    def test_12_setup_fairness_monitoring(self):
        TestAIOpenScaleClient.subscription.fairness_monitoring.enable(
            features=[
                Feature("Sex", majority=['male'], minority=['female'], threshold=0.95),
                Feature("Age", majority=[[26, 75]], minority=[[18, 25]], threshold=0.95)
            ],
            favourable_classes=['No Risk'],
            unfavourable_classes=['Risk'],
            min_records=4,
        )

    def test_13_inject_quality_metrics(self):
        quality_metric = {'area_under_roc': 0.666}
        TestAIOpenScaleClient.subscription.monitoring.store_metrics(monitor_uid='quality', metrics=quality_metric)

        time.sleep(10)

        TestAIOpenScaleClient.subscription.quality_monitoring.show_table()
        TestAIOpenScaleClient.subscription.monitoring.show_table(monitor_uid='quality')

        quality_metrics_py = self.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue('0.666' in str(quality_metrics_py))

    def test_14_inject_quality_measurements(self):
        quality_metric = {'area_under_roc': 0.999}
        source = {
            "id": "confusion_matrix_1",
            "type": "confusion_matrix",
            "data": {
                "labels": ["Risk", "No Risk"],
                "values": [[11, 21],
                           [20, 10]]}
        }

        measurements = [
            MeasurementRecord(metrics=quality_metric, sources=source),
            MeasurementRecord(metrics=quality_metric, sources=source)
        ]

        details = TestAIOpenScaleClient.subscription.monitoring.store_measurements(monitor_uid='quality', measurements=measurements)
        print('Measurement details', details)

        time.sleep(10)

        measurement_id = details[0]['measurement_id']

        print('measurement_id', measurement_id)
        self.subscription.quality_monitoring.show_table()
        self.subscription.quality_monitoring.show_confusion_matrix(measurement_id=measurement_id)

        quality_metrics_py = self.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue(str(quality_metric['area_under_roc']) in str(quality_metrics_py))
        self.assertTrue('20' in str(quality_metrics_py))

        TestAIOpenScaleClient.subscription.quality_monitoring.show_table()
        TestAIOpenScaleClient.subscription.monitoring.show_table(monitor_uid='quality')

    def test_15_inject_performance_metrics(self):
        if "ICP" in get_env():
            self.skipTest("Performance monitoring is not working on ICP with WML scoring.")

        performance_metric = {'records': 245, 'response_time': 62.33809845686894}
        TestAIOpenScaleClient.subscription.monitoring.store_metrics(monitor_uid='performance', metrics=performance_metric)

        time.sleep(10)

        self.subscription.performance_monitoring.show_table()

        performance_table_python = self.subscription.performance_monitoring.get_table_content(format='python')
        self.assertTrue('62.33809845686894' in str(performance_table_python))

    def test_16_inject_performance_measurements(self):
        if "ICP" in get_env():
            self.skipTest("Performance monitoring is not working on ICP with WML scoring.")

        measurements = [
            MeasurementRecord(metrics={'records': 245, 'response_time': 62.33809845686894}),
            MeasurementRecord(metrics={'records': 45, 'response_time': 2.33809845686894})
        ]

        details = TestAIOpenScaleClient.subscription.monitoring.store_measurements(monitor_uid='performance',
                                                                               measurements=measurements)
        time.sleep(10)

        self.assertTrue('2.33809845686894' in str(details))

    def test_17_inject_fairness_metrics(self):
        fairness_metric = {'metrics': [{'feature': 'Sex', 'majority': {'values': [{'value': 'male', 'distribution': {'male': [{'count': 65, 'label': 'No Risk', 'is_favourable': True}, {'count': 4, 'label': 'Risk', 'is_favourable': False}]}, 'fav_class_percent': 95.0}], 'total_fav_percent': 95.0, 'total_rows_percent': 33.33333333333333}, 'minority': {'values': [{'value': 'female', 'is_biased': True, 'distribution': {'female': [{'count': 29, 'label': 'No Risk', 'is_favourable': True}, {'count': 2, 'label': 'Risk', 'is_favourable': False}]}, 'fairness_value': 0.947333, 'fav_class_percent': 90.0}], 'total_fav_percent': 90.0, 'total_rows_percent': 33.33333333333333}}, {'feature': 'Age', 'majority': {'values': [{'value': [26, 75], 'distribution': {'26': [{'count': 4, 'label': 'No Risk', 'is_favourable': True}], '28': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '29': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '30': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '31': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '32': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '33': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '34': [{'count': 1, 'label': 'Risk', 'is_favourable': False}, {'count': 4, 'label': 'No Risk', 'is_favourable': True}], '35': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '36': [{'count': 3, 'label': 'No Risk', 'is_favourable': True}], '37': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '38': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '39': [{'count': 3, 'label': 'No Risk', 'is_favourable': True}, {'count': 1, 'label': 'Risk', 'is_favourable': False}], '40': [{'count': 3, 'label': 'No Risk', 'is_favourable': True}], '41': [{'count': 3, 'label': 'No Risk', 'is_favourable': True}], '43': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '45': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '47': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '49': [{'count': 1, 'label': 'Risk', 'is_favourable': False}], '50': [{'count': 3, 'label': 'No Risk', 'is_favourable': True}, {'count': 1, 'label': 'Risk', 'is_favourable': False}], '52': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '54': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '55': [{'count': 1, 'label': 'Risk', 'is_favourable': False}, {'count': 1, 'label': 'No Risk', 'is_favourable': True}], '71': [{'count': 1, 'label': 'Risk', 'is_favourable': False}]}, 'fav_class_percent': 88.43537414965986}], 'total_fav_percent': 88.43537414965986, 'total_rows_percent': 49.0}, 'minority': {'values': [{'value': [18, 25], 'is_biased': False, 'distribution': {'19': [{'count': 16, 'label': 'No Risk', 'is_favourable': True}], '20': [{'count': 16, 'label': 'No Risk', 'is_favourable': True}], '21': [{'count': 11, 'label': 'No Risk', 'is_favourable': True}], '23': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '24': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '25': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}]}, 'fairness_value': 1.101, 'fav_class_percent': 97.38562091503267}], 'total_fav_percent': 97.38562091503267, 'total_rows_percent': 51.0}, 'bias_source': {'values': []}}], 'score_type': 'desperate impact', 'response_time': '13.128683', 'rows_analyzed': 100, 'perturbed_data_size': 200, 'manual_labelling_store': 'Manual_Labeling_dd79dd1b-0afc-436e-9999-6fd6414f81c2'}
        TestAIOpenScaleClient.subscription.monitoring.store_metrics(monitor_uid='fairness', metrics=fairness_metric)

        time.sleep(10)

        TestAIOpenScaleClient.subscription.fairness_monitoring.show_table()

        python_table_content = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content(format='python')
        self.assertTrue('0.947333' in str(python_table_content))

    def test_19_inject_debias_metrics(self):
        debiased_fairness_metric = {'metrics': [{'feature': 'Sex', 'majority': {'values': [{'value': 'male', 'distribution': {'male': [{'count': 5, 'label': 'Risk', 'is_favourable': False}, {'count': 56, 'label': 'No Risk', 'is_favourable': False}]}, 'fav_class_percent': 95.0}], 'total_fav_percent': 95.0, 'total_rows_percent': 50.0}, 'minority': {'values': [{'value': 'female', 'is_biased': False, 'distribution': {'female': [{'count': 39, 'label': 'No Risk', 'is_favourable': False}]}, 'fairness_value': 1.0, 'fav_class_percent': 95.0}], 'total_fav_percent': 95.0, 'total_rows_percent': 50.0}}, {'feature': 'Age', 'majority': {'values': [{'value': [26, 75], 'distribution': {'26': [{'count': 2, 'label': 'No Risk', 'is_favourable': False}], '28': [{'count': 5, 'label': 'No Risk', 'is_favourable': False}], '29': [{'count': 2, 'label': 'No Risk', 'is_favourable': False}], '30': [{'count': 1, 'label': 'No Risk', 'is_favourable': False}], '31': [{'count': 1, 'label': 'No Risk', 'is_favourable': False}], '32': [{'count': 4, 'label': 'No Risk', 'is_favourable': False}], '34': [{'count': 4, 'label': 'No Risk', 'is_favourable': False}], '35': [{'count': 1, 'label': 'No Risk', 'is_favourable': False}], '36': [{'count': 1, 'label': 'No Risk', 'is_favourable': False}], '37': [{'count': 1, 'label': 'No Risk', 'is_favourable': False}], '39': [{'count': 2, 'label': 'No Risk', 'is_favourable': False}], '40': [{'count': 2, 'label': 'No Risk', 'is_favourable': False}], '41': [{'count': 2, 'label': 'No Risk', 'is_favourable': False}], '42': [{'count': 1, 'label': 'Risk', 'is_favourable': False}], '43': [{'count': 1, 'label': 'No Risk', 'is_favourable': False}], '44': [{'count': 3, 'label': 'No Risk', 'is_favourable': False}], '45': [{'count': 2, 'label': 'No Risk', 'is_favourable': False}], '48': [{'count': 2, 'label': 'No Risk', 'is_favourable': False}], '49': [{'count': 1, 'label': 'Risk', 'is_favourable': False}], '52': [{'count': 1, 'label': 'No Risk', 'is_favourable': False}], '59': [{'count': 1, 'label': 'Risk', 'is_favourable': False}], '60': [{'count': 1, 'label': 'No Risk', 'is_favourable': False}], '66': [{'count': 1, 'label': 'No Risk', 'is_favourable': False}], '67': [{'count': 1, 'label': 'Risk', 'is_favourable': False}]}, 'fav_class_percent': 96.17834394904459}], 'total_fav_percent': 96.17834394904459, 'total_rows_percent': 78.5}, 'minority': {'values': [{'value': [18, 25], 'is_biased': True, 'distribution': {'19': [{'count': 17, 'label': 'No Risk', 'is_favourable': False}], '20': [{'count': 18, 'label': 'No Risk', 'is_favourable': False}, {'count': 1, 'label': 'Risk', 'is_favourable': False}], '21': [{'count': 13, 'label': 'No Risk', 'is_favourable': False}], '22': [{'count': 4, 'label': 'No Risk', 'is_favourable': False}], '23': [{'count': 1, 'label': 'No Risk', 'is_favourable': False}], '24': [{'count': 1, 'label': 'No Risk', 'is_favourable': False}], '25': [{'count': 2, 'label': 'No Risk', 'is_favourable': False}]}, 'fairness_value': 0.974, 'fav_class_percent': 93.7062937062937}], 'total_fav_percent': 93.7062937062937, 'total_rows_percent': 71.5}, 'bias_source': {'values': [{'range': '[18,19]', 'fav_percent': 88.23529411764706}]}}], 'debiased': True, 'score_type': 'desperate impact', 'response_time': '237.744371', 'rows_analyzed': 100, 'perturbed_data_size': 100, 'manual_labelling_store': 'Manual_Labeling_dd79dd1b-0afc-436e-9999-6fd6414f81c2'}
        TestAIOpenScaleClient.subscription.monitoring.store_metrics(monitor_uid='debiased_fairness',                                                                    metrics=debiased_fairness_metric)

        time.sleep(10)

    def test_20_get_metrics(self):
        print("Old metrics:")
        print(self.ai_client.data_mart.get_deployment_metrics())
        print(self.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(self.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(self.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))

        ### BINARY CHECK

        metrics = {
            'area_under_roc': None,
        }

        quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        print("Old quality metric:\n{}".format(quality_metrics))

        for metric in quality_metrics['deployment_metrics'][0]['metrics'][0]['value']['metrics']:
            if metric['name'] in metrics.keys():
                metrics[metric['name']] = metric['value']

        ootb_quality_metrics = self.subscription.quality_monitoring.get_metrics()
        print("New quality metrics:\n{}".format(ootb_quality_metrics))

        for metric in ootb_quality_metrics[0]['metrics']:
            if metric['id'] in metrics.keys():
                print("Comparing metrics: {}".format(metric['id']))
                self.assertEqual(metric['value'], metrics[metric['id']],
                                 msg="metric {} has different value in ootb api".format(metric['id']))

        print(self.subscription.quality_monitoring.get_metrics(format="samples"))

    def test_21_insert_quality_historical_records(self):
        import json
        from ibm_ai_openscale.utils import generate_historical_timestamps

        data_path = os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'historical_records', 'credit_risk_quality_measurements.json')

        with open(data_path) as json_file:
            records = json.load(json_file)

        history_days = int(len(records)/24)
        timestamps = generate_historical_timestamps(days=history_days)
        measurements = []

        for record, timestamp in zip(records, timestamps):
            measurements.append(
                MeasurementRecord(
                    metrics=record['metrics'],
                    sources=record['sources'],
                    timestamp=timestamp))

        details = TestAIOpenScaleClient.subscription.monitoring.store_measurements(
            monitor_uid='quality',
            measurements=measurements)

        time.sleep(10)
        
        print('Data insert details', details)
        self.assertTrue('0.7485207100591716' in str(details))

    @classmethod
    def tearDownClass(cls):
        clean_up_env(cls.ai_client)


if __name__ == '__main__':
    unittest.main()
