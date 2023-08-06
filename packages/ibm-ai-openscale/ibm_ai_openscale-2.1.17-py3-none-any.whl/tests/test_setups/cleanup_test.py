# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


from utils.assertions import *
from utils.cleanup import *
from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *


class TestAIOpenScaleClient(unittest.TestCase):
    ai_client = None
    credentials = None

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()
        cls.credentials = get_azure_credentials()

        if "ICP" in get_env():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)

        prepare_env(cls.ai_client)

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)
        details = TestAIOpenScaleClient.ai_client.data_mart.get_details()
        assert_datamart_details(details, schema=self.schema, state='active')

    def test_02_bind_azure_service(self):
        binding_uid = self.ai_client.data_mart.bindings.add("Azure ml service engine", AzureMachineLearningServiceInstance(self.credentials))
        print("Azure service binding uid: {}".format(binding_uid))

    def test_03_bind_azure_studio(self):
        binding_uid = self.ai_client.data_mart.bindings.add("Azure ml engine", AzureMachineLearningStudioInstance(self.credentials))
        print("Azure studio binding uid: {}".format(binding_uid))


if __name__ == '__main__':
    unittest.main()
