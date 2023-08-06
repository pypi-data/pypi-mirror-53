import os
import json
import requests
from ibm_ai_openscale.client import APIClient
from ibm_ai_openscale.supporting_classes.payload_record import PayloadRecord
from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2
from datetime import datetime, timedelta
import csv
import random
import os


class DemoData:
    def __init__(self, aios_credentials):
        self.current_time = datetime.utcnow().isoformat() + 'Z'
        self.ai_client = APIClient(aios_credentials)
        self.hrefs_v2 = AIHrefDefinitionsV2(aios_credentials)

    # def load_historical_business_payload(self, data_set_id, file_path, day_template="history_business_payloads_{}.json", days=7):
    #     payload_files = [os.path.join(file_path, day_template.format(x)) for x in range(days)]
    #
    #     for fl in payload_files:
    #         with open(fl) as f:
    #             historical_data = json.load(f)
    #
    #         print("Loading day {}".format(fl))
    #         response = requests.post(url=self.hrefs_v2.get_data_set_records_href(data_set_id),
    #                                  headers=self.ai_client._get_headers(), json=historical_data)
    #         assert response.status_code == 202
    #
    #     print(response.status_code, response.text)
    def load_historical_business_payload(self, data_set_id, file_path=os.getcwd(), file_name="history_business_payloads_week.csv"):
        payload_file = os.path.join(file_path, file_name)

        def _num(string_value):
            try:
                return float(string_value)
            except ValueError:
                return string_value

        with open(payload_file) as f:
            reader = csv.DictReader(f)
            list_payload = [row for row in reader]
            historical_business_payload = []
            for row in list_payload:
                record = dict(row)
                for field in record.keys():
                    record[field] = _num(record[field])

                historical_business_payload.append(record)

        response = requests.post(url=self.hrefs_v2.get_data_set_records_href(data_set_id),
                                 headers=self.ai_client._get_headers(), json=historical_business_payload)

        assert response.status_code == 202

        print(response.status_code, response.text)

    def load_historical_scoring_payload(self, subscription, deployment_id, file_path=os.getcwd(),
                                        day_template="history_correlation_payloads_{}.json", days=7):
        payload_files = [os.path.join(file_path, day_template.format(x)) for x in range(days)]
        subscription.payload_logging.enable(dynamic_schema_update=True)

        for fl in payload_files:
            record_list = []

            with open(fl) as f:
                historical_payload = json.load(f)
            record_list.extend([PayloadRecord(request=hour_payload['request'],
                                              response=hour_payload['response'],
                                              response_time=random.randint(10, 15)) for hour_payload in historical_payload])

            print("Loading day {}".format(fl))
            subscription.payload_logging.store(records=record_list, deployment_id=deployment_id)

    def load_historical_kpi_measurements(self, monitor_instance_id, file_path=os.getcwd(), filename="history_business_metrics.json"):
        with open(os.path.join(file_path, filename)) as json_file:
            historical_kpis = json.load(json_file)

        metrics = historical_kpis['metrics']
        payload = []
        day = 7

        for metric in metrics:
            start_time = datetime.strptime(self.current_time, "%Y-%m-%dT%H:%M:%S.%fZ") - timedelta(days=day)
            start_time = str(start_time.isoformat() + 'Z')

            payload.append({
                "timestamp": str(start_time),
                "metrics": [metric]
            })

            day -= 1

        response = requests.post(
            url=self.hrefs_v2.get_measurements_href(monitor_instance_id),
            headers=self.ai_client._get_headers(),
            json=payload)

        assert 202 == response.status_code

    def load_historical_drift_measurements(self, monitor_instance_id, business_application_id, file_path=os.getcwd(),
                                           filename="history_drift_metrics.json"):
        with open(os.path.join(file_path, filename)) as json_file:
            historical_drift = json.load(json_file)

        metrics_accepted = [metric for metric in historical_drift['metrics'] if
                            metric['business_metric_id'] == 'accepted_credits']
        metric_amount = [metric for metric in historical_drift['metrics'] if
                         metric['business_metric_id'] == 'credit_amount_granted']
        payload = []
        day = 7

        for metric_acc, metric_am in zip(metrics_accepted, metric_amount):
            start_time = datetime.strptime(self.current_time, "%Y-%m-%dT%H:%M:%S.%fZ") - timedelta(days=day)
            start_time = str(start_time.isoformat() + 'Z')
            metric_acc["business_application_id"] = business_application_id
            metric_am["business_application_id"] = business_application_id

            payload.append({
                "timestamp": str(start_time),
                "metrics": [metric_acc]
            })
            payload.append({
                "timestamp": str(start_time),
                "metrics": [metric_am]
            })

            day -= 1

        response = requests.post(
            url=self.hrefs_v2.get_measurements_href(monitor_instance_id),
            headers=self.ai_client._get_headers(),
            json=payload)

        assert response.status_code == 202

