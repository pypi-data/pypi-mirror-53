# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


import pandas as pd
from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2

from ibm_ai_openscale.supporting_classes.measurement_record import MeasurementRecord

from pyspark import SparkContext, SQLContext
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import StringIndexer, VectorAssembler, IndexToString
from pyspark.sql.types import StructType, DoubleType, StringType, ArrayType

from utils.assertions import *
from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType
from preparation_and_cleaning import *


DAYS = 1


class TestAIOpenScaleClient(unittest.TestCase):
    subscription_s1 = None
    subscription_s2 = None
    subscription_s3 = None

    model_uid_1 = None
    model_uid_2 = None
    model_uid_3 = None

    deployment_uid_1 = None
    deployment_uid_2 = None
    deployment_uid_3 = None

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
    binding_uid = None

    scoring_result = None
    payload_scoring = None
    published_model_details = None
    monitor_uid = None
    source_uid = None
    correlation_monitor_uid = 'correlations'
    measurement_details = None
    transaction_id = None
    drift_model_name = "drift_detection_model.tar.gz"
    drift_model_path = os.path.join(os.getcwd(), 'artifacts', 'drift_models')
    data_df = pd.read_csv(
        "./datasets/German_credit_risk/credit_risk_training.csv",
        dtype={'LoanDuration': int, 'LoanAmount': int, 'InstallmentPercent': int, 'CurrentResidenceDuration': int,
               'Age': int, 'ExistingCreditsCount': int, 'Dependents': int})

    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()
        cls.hrefs_v2 = AIHrefDefinitionsV2(cls.aios_credentials)

        if "ICP" in get_env():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
            upload_credit_risk_training_data_to_db2(cls.database_credentials)

        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

        # clean_up_wml_instance()
        prepare_env(cls.ai_client)

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_binding(self):
        if "ICP" in get_env():
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on ICP",
                                                                                      WatsonMachineLearningInstance4ICP())
        else:
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on Cloud",
                                                                                      WatsonMachineLearningInstance(
                                                                                          self.wml_credentials))

    def test_03_get_binding_details(self):
        binding_details = self.ai_client.data_mart.bindings.get_details()
        print("Binding details: {}".format(binding_details))
        self.assertIsNotNone(binding_details)

    def test_04_list_assets(self):
        self.ai_client.data_mart.bindings.list_assets()
        self.ai_client.data_mart.bindings.list_asset_deployments()

    def test_05_get_wml_client(self):
        print("Binding details:\n{}".format(self.ai_client.data_mart.bindings.get_details(self.binding_uid)))
        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(
            self.binding_uid)

    def test_06a_prepare_credit_model(self):
        asset_name = "Credit risk model"
        deployment_name = "Credit risk deployment"

        TestAIOpenScaleClient.model_uid_1, TestAIOpenScaleClient.deployment_uid_1 = get_wml_model_and_deployment_id(
            model_name=asset_name, deployment_name=deployment_name)

        if self.deployment_uid_1 is None:
            ctx = SparkContext.getOrCreate()
            sc = SQLContext(ctx)

            spark_df = sc.read.format("com.databricks.spark.csv").option("header", "true").option("delimiter", ",").option("inferSchema", "true").load(
                os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'credit_risk_training.csv'))
            spark_df.printSchema()

            (train_data, test_data) = spark_df.randomSplit([0.8, 0.2], 24)
            print("Number of records for training: " + str(train_data.count()))
            print("Number of records for evaluation: " + str(test_data.count()))

            si_CheckingStatus = StringIndexer(inputCol='CheckingStatus', outputCol='CheckingStatus_IX')
            si_CreditHistory = StringIndexer(inputCol='CreditHistory', outputCol='CreditHistory_IX')
            si_LoanPurpose = StringIndexer(inputCol='LoanPurpose', outputCol='LoanPurpose_IX')
            si_ExistingSavings = StringIndexer(inputCol='ExistingSavings', outputCol='ExistingSavings_IX')
            si_EmploymentDuration = StringIndexer(inputCol='EmploymentDuration', outputCol='EmploymentDuration_IX')
            si_Sex = StringIndexer(inputCol='Sex', outputCol='Sex_IX')
            si_OthersOnLoan = StringIndexer(inputCol='OthersOnLoan', outputCol='OthersOnLoan_IX')
            si_OwnsProperty = StringIndexer(inputCol='OwnsProperty', outputCol='OwnsProperty_IX')
            si_InstallmentPlans = StringIndexer(inputCol='InstallmentPlans', outputCol='InstallmentPlans_IX')
            si_Housing = StringIndexer(inputCol='Housing', outputCol='Housing_IX')
            si_Job = StringIndexer(inputCol='Job', outputCol='Job_IX')
            si_Telephone = StringIndexer(inputCol='Telephone', outputCol='Telephone_IX')
            si_ForeignWorker = StringIndexer(inputCol='ForeignWorker', outputCol='ForeignWorker_IX')
            si_Label = StringIndexer(inputCol="Risk", outputCol="label").fit(spark_df)
            label_converter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=si_Label.labels)

            va_features = VectorAssembler(
                inputCols=["CheckingStatus_IX", "CreditHistory_IX", "LoanPurpose_IX", "ExistingSavings_IX",
                           "EmploymentDuration_IX", "Sex_IX", "OthersOnLoan_IX", "OwnsProperty_IX", "InstallmentPlans_IX",
                           "Housing_IX", "Job_IX", "Telephone_IX", "ForeignWorker_IX", "LoanDuration", "LoanAmount",
                           "InstallmentPercent", "CurrentResidenceDuration", "LoanDuration", "Age", "ExistingCreditsCount",
                           "Dependents"], outputCol="features")

            classifier = RandomForestClassifier(featuresCol="features")

            pipeline = Pipeline(
                stages=[si_CheckingStatus, si_CreditHistory, si_EmploymentDuration, si_ExistingSavings, si_ForeignWorker,
                        si_Housing, si_InstallmentPlans, si_Job, si_LoanPurpose, si_OthersOnLoan,
                        si_OwnsProperty, si_Sex, si_Telephone, si_Label, va_features, classifier, label_converter])

            model = pipeline.fit(train_data)
            predictions = model.transform(test_data)
            evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction")
            auc = evaluator.evaluate(predictions)

            print("Accuracy = %g" % auc)

            train_data_schema = spark_df.schema
            label_field = next(f for f in train_data_schema.fields if f.name == "Risk")
            label_field.metadata['values'] = si_Label.labels
            input_fileds = filter(lambda f: f.name != "Risk", train_data_schema.fields)

            output_data_schema = StructType(list(input_fileds)). \
                add("prediction", DoubleType(), True, {'modeling_role': 'prediction'}). \
                add("predictedLabel", StringType(), True,
                    {'modeling_role': 'decoded-target', 'values': si_Label.labels}). \
                add("probability", ArrayType(DoubleType()), True, {'modeling_role': 'probability'})

            if "ICP" in get_env():
                training_data_reference = {
                    "name": "Credit Risk feedback",
                    "connection": self.database_credentials,
                    "source": {
                        "tablename": "CREDIT_RISK_TRAINING",
                        'schema_name': 'TRAININGDATA',
                        "type": "db2"
                    }
                }
            else:
                db2_credentials = {
                    "hostname": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
                    "password": "89TsmoAN_Sb_",
                    "https_url": "https://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:8443",
                    "port": 50000,
                    "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;Security=SSL;",
                    "host": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
                    "jdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
                    "uri": "db2://dash14647:89TsmoAN_Sb_@dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
                    "db": "BLUDB",
                    "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;",
                    "username": "dash14647",
                    "ssljdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50001/BLUDB:sslConnection=true;"
                }

                training_data_reference = {
                    "name": "Credit Risk feedback",
                    "connection": db2_credentials,
                    "source": {
                        "tablename": "CREDIT_RISK_TRAINING",
                        "type": "dashdb"
                    }
                }

            print("Training data reference:\n{}".format(training_data_reference))

            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(asset_name),
                self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: training_data_reference,
                self.wml_client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA: output_data_schema.jsonValue(),
                self.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                    {
                        "name": "AUC",
                        "value": auc,
                        "threshold": 0.8
                    }
                ]
            }

            print("Publishing a new model...")
            published_model_details = self.wml_client.repository.store_model(model=model, meta_props=model_props, training_data=train_data, pipeline=pipeline)

            print("Published model details:\n{}".format(published_model_details))
            TestAIOpenScaleClient.model_uid_1 = self.wml_client.repository.get_model_uid(published_model_details)

            print("Deploying model: {}, deployment name: {}".format(asset_name, deployment_name))
            deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid_1, name=deployment_name, asynchronous=False)
            TestAIOpenScaleClient.deployment_uid_1 = self.wml_client.deployments.get_uid(deployment)

            deployment_details = self.wml_client.deployments.get_details(self.deployment_uid_1)
            print("Deployment details:\n{}".format(deployment_details))

    def test_06b_prepare_interest_model(self):
        asset_name = "Interest rate model"
        deployment_name = "Interest rate deployment"

        TestAIOpenScaleClient.model_uid_2, TestAIOpenScaleClient.deployment_ui_2 = get_wml_model_and_deployment_id(
            model_name=asset_name, deployment_name=deployment_name)

        if self.deployment_uid_2 is None:
            ctx = SparkContext.getOrCreate()
            sc = SQLContext(ctx)

            spark_df = sc.read.format("com.databricks.spark.csv").option("header", "true").option("delimiter", ",").option("inferSchema", "true").load(
                os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'credit_risk_training.csv'))
            spark_df.printSchema()

            (train_data, test_data) = spark_df.randomSplit([0.8, 0.2], 24)
            print("Number of records for training: " + str(train_data.count()))
            print("Number of records for evaluation: " + str(test_data.count()))

            si_CheckingStatus = StringIndexer(inputCol='CheckingStatus', outputCol='CheckingStatus_IX')
            si_CreditHistory = StringIndexer(inputCol='CreditHistory', outputCol='CreditHistory_IX')
            si_LoanPurpose = StringIndexer(inputCol='LoanPurpose', outputCol='LoanPurpose_IX')
            si_ExistingSavings = StringIndexer(inputCol='ExistingSavings', outputCol='ExistingSavings_IX')
            si_EmploymentDuration = StringIndexer(inputCol='EmploymentDuration', outputCol='EmploymentDuration_IX')
            si_Sex = StringIndexer(inputCol='Sex', outputCol='Sex_IX')
            si_OthersOnLoan = StringIndexer(inputCol='OthersOnLoan', outputCol='OthersOnLoan_IX')
            si_OwnsProperty = StringIndexer(inputCol='OwnsProperty', outputCol='OwnsProperty_IX')
            si_InstallmentPlans = StringIndexer(inputCol='InstallmentPlans', outputCol='InstallmentPlans_IX')
            si_Housing = StringIndexer(inputCol='Housing', outputCol='Housing_IX')
            si_Job = StringIndexer(inputCol='Job', outputCol='Job_IX')
            si_Telephone = StringIndexer(inputCol='Telephone', outputCol='Telephone_IX')
            si_ForeignWorker = StringIndexer(inputCol='ForeignWorker', outputCol='ForeignWorker_IX')
            si_Label = StringIndexer(inputCol="Risk", outputCol="label").fit(spark_df)
            label_converter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=si_Label.labels)

            va_features = VectorAssembler(
                inputCols=["CheckingStatus_IX", "CreditHistory_IX", "LoanPurpose_IX", "ExistingSavings_IX",
                           "EmploymentDuration_IX", "Sex_IX", "OthersOnLoan_IX", "OwnsProperty_IX", "InstallmentPlans_IX",
                           "Housing_IX", "Job_IX", "Telephone_IX", "ForeignWorker_IX", "LoanDuration", "LoanAmount",
                           "InstallmentPercent", "CurrentResidenceDuration", "LoanDuration", "Age", "ExistingCreditsCount",
                           "Dependents"], outputCol="features")

            classifier = RandomForestClassifier(featuresCol="features")

            pipeline = Pipeline(
                stages=[si_CheckingStatus, si_CreditHistory, si_EmploymentDuration, si_ExistingSavings, si_ForeignWorker,
                        si_Housing, si_InstallmentPlans, si_Job, si_LoanPurpose, si_OthersOnLoan,
                        si_OwnsProperty, si_Sex, si_Telephone, si_Label, va_features, classifier, label_converter])

            model = pipeline.fit(train_data)
            predictions = model.transform(test_data)
            evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction")
            auc = evaluator.evaluate(predictions)

            print("Accuracy = %g" % auc)

            train_data_schema = spark_df.schema
            label_field = next(f for f in train_data_schema.fields if f.name == "Risk")
            label_field.metadata['values'] = si_Label.labels
            input_fileds = filter(lambda f: f.name != "Risk", train_data_schema.fields)

            output_data_schema = StructType(list(input_fileds)). \
                add("prediction", DoubleType(), True, {'modeling_role': 'prediction'}). \
                add("predictedLabel", StringType(), True,
                    {'modeling_role': 'decoded-target', 'values': si_Label.labels}). \
                add("probability", ArrayType(DoubleType()), True, {'modeling_role': 'probability'})

            if "ICP" in get_env():
                training_data_reference = {
                    "name": "Credit Risk feedback",
                    "connection": self.database_credentials,
                    "source": {
                        "tablename": "CREDIT_RISK_TRAINING",
                        'schema_name': 'TRAININGDATA',
                        "type": "db2"
                    }
                }
            else:
                db2_credentials = {
                    "hostname": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
                    "password": "89TsmoAN_Sb_",
                    "https_url": "https://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:8443",
                    "port": 50000,
                    "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;Security=SSL;",
                    "host": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
                    "jdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
                    "uri": "db2://dash14647:89TsmoAN_Sb_@dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
                    "db": "BLUDB",
                    "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;",
                    "username": "dash14647",
                    "ssljdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50001/BLUDB:sslConnection=true;"
                }

                training_data_reference = {
                    "name": "Credit Risk feedback",
                    "connection": db2_credentials,
                    "source": {
                        "tablename": "CREDIT_RISK_TRAINING",
                        "type": "dashdb"
                    }
                }

            print("Training data reference:\n{}".format(training_data_reference))

            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(asset_name),
                self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: training_data_reference,
                self.wml_client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA: output_data_schema.jsonValue(),
                self.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                    {
                        "name": "AUC",
                        "value": auc,
                        "threshold": 0.8
                    }
                ]
            }

            print("Publishing a new model...")
            published_model_details = self.wml_client.repository.store_model(model=model, meta_props=model_props, training_data=train_data, pipeline=pipeline)

            print("Published model details:\n{}".format(published_model_details))
            TestAIOpenScaleClient.model_uid_2 = self.wml_client.repository.get_model_uid(published_model_details)

            print("Deploying model: {}, deployment name: {}".format(asset_name, deployment_name))
            deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid_2, name=deployment_name, asynchronous=False)
            TestAIOpenScaleClient.deployment_uid_2 = self.wml_client.deployments.get_uid(deployment)

            deployment_details = self.wml_client.deployments.get_details(self.deployment_uid_2)
            print("Deployment details:\n{}".format(deployment_details))

    def test_06c_prepare_currency_model(self):
        asset_name = "Currency rate model"
        deployment_name = "Currency rate deployment"

        TestAIOpenScaleClient.model_uid_3, TestAIOpenScaleClient.deployment_uid_3 = get_wml_model_and_deployment_id(
            model_name=asset_name, deployment_name=deployment_name)

        if self.deployment_uid_3 is None:
            ctx = SparkContext.getOrCreate()
            sc = SQLContext(ctx)

            spark_df = sc.read.format("com.databricks.spark.csv").option("header", "true").option("delimiter", ",").option("inferSchema", "true").load(
                os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'credit_risk_training.csv'))
            spark_df.printSchema()

            (train_data, test_data) = spark_df.randomSplit([0.8, 0.2], 24)
            print("Number of records for training: " + str(train_data.count()))
            print("Number of records for evaluation: " + str(test_data.count()))

            si_CheckingStatus = StringIndexer(inputCol='CheckingStatus', outputCol='CheckingStatus_IX')
            si_CreditHistory = StringIndexer(inputCol='CreditHistory', outputCol='CreditHistory_IX')
            si_LoanPurpose = StringIndexer(inputCol='LoanPurpose', outputCol='LoanPurpose_IX')
            si_ExistingSavings = StringIndexer(inputCol='ExistingSavings', outputCol='ExistingSavings_IX')
            si_EmploymentDuration = StringIndexer(inputCol='EmploymentDuration', outputCol='EmploymentDuration_IX')
            si_Sex = StringIndexer(inputCol='Sex', outputCol='Sex_IX')
            si_OthersOnLoan = StringIndexer(inputCol='OthersOnLoan', outputCol='OthersOnLoan_IX')
            si_OwnsProperty = StringIndexer(inputCol='OwnsProperty', outputCol='OwnsProperty_IX')
            si_InstallmentPlans = StringIndexer(inputCol='InstallmentPlans', outputCol='InstallmentPlans_IX')
            si_Housing = StringIndexer(inputCol='Housing', outputCol='Housing_IX')
            si_Job = StringIndexer(inputCol='Job', outputCol='Job_IX')
            si_Telephone = StringIndexer(inputCol='Telephone', outputCol='Telephone_IX')
            si_ForeignWorker = StringIndexer(inputCol='ForeignWorker', outputCol='ForeignWorker_IX')
            si_Label = StringIndexer(inputCol="Risk", outputCol="label").fit(spark_df)
            label_converter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=si_Label.labels)

            va_features = VectorAssembler(
                inputCols=["CheckingStatus_IX", "CreditHistory_IX", "LoanPurpose_IX", "ExistingSavings_IX",
                           "EmploymentDuration_IX", "Sex_IX", "OthersOnLoan_IX", "OwnsProperty_IX", "InstallmentPlans_IX",
                           "Housing_IX", "Job_IX", "Telephone_IX", "ForeignWorker_IX", "LoanDuration", "LoanAmount",
                           "InstallmentPercent", "CurrentResidenceDuration", "LoanDuration", "Age", "ExistingCreditsCount",
                           "Dependents"], outputCol="features")

            classifier = RandomForestClassifier(featuresCol="features")

            pipeline = Pipeline(
                stages=[si_CheckingStatus, si_CreditHistory, si_EmploymentDuration, si_ExistingSavings, si_ForeignWorker,
                        si_Housing, si_InstallmentPlans, si_Job, si_LoanPurpose, si_OthersOnLoan,
                        si_OwnsProperty, si_Sex, si_Telephone, si_Label, va_features, classifier, label_converter])

            model = pipeline.fit(train_data)
            predictions = model.transform(test_data)
            evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction")
            auc = evaluator.evaluate(predictions)

            print("Accuracy = %g" % auc)

            train_data_schema = spark_df.schema
            label_field = next(f for f in train_data_schema.fields if f.name == "Risk")
            label_field.metadata['values'] = si_Label.labels
            input_fileds = filter(lambda f: f.name != "Risk", train_data_schema.fields)

            output_data_schema = StructType(list(input_fileds)). \
                add("prediction", DoubleType(), True, {'modeling_role': 'prediction'}). \
                add("predictedLabel", StringType(), True,
                    {'modeling_role': 'decoded-target', 'values': si_Label.labels}). \
                add("probability", ArrayType(DoubleType()), True, {'modeling_role': 'probability'})

            if "ICP" in get_env():
                training_data_reference = {
                    "name": "Credit Risk feedback",
                    "connection": self.database_credentials,
                    "source": {
                        "tablename": "CREDIT_RISK_TRAINING",
                        'schema_name': 'TRAININGDATA',
                        "type": "db2"
                    }
                }
            else:
                db2_credentials = {
                    "hostname": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
                    "password": "89TsmoAN_Sb_",
                    "https_url": "https://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:8443",
                    "port": 50000,
                    "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;Security=SSL;",
                    "host": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
                    "jdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
                    "uri": "db2://dash14647:89TsmoAN_Sb_@dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
                    "db": "BLUDB",
                    "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;",
                    "username": "dash14647",
                    "ssljdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50001/BLUDB:sslConnection=true;"
                }

                training_data_reference = {
                    "name": "Credit Risk feedback",
                    "connection": db2_credentials,
                    "source": {
                        "tablename": "CREDIT_RISK_TRAINING",
                        "type": "dashdb"
                    }
                }

            print("Training data reference:\n{}".format(training_data_reference))

            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(asset_name),
                self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: training_data_reference,
                self.wml_client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA: output_data_schema.jsonValue(),
                self.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                    {
                        "name": "AUC",
                        "value": auc,
                        "threshold": 0.8
                    }
                ]
            }

            print("Publishing a new model...")
            published_model_details = self.wml_client.repository.store_model(model=model, meta_props=model_props, training_data=train_data, pipeline=pipeline)

            print("Published model details:\n{}".format(published_model_details))
            TestAIOpenScaleClient.model_uid_3 = self.wml_client.repository.get_model_uid(published_model_details)

            print("Deploying model: {}, deployment name: {}".format(asset_name, deployment_name))
            deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid_3, name=deployment_name, asynchronous=False)
            TestAIOpenScaleClient.deployment_uid_3 = self.wml_client.deployments.get_uid(deployment)

            deployment_details = self.wml_client.deployments.get_details(self.deployment_uid_3)
            print("Deployment details:\n{}".format(deployment_details))

    def test_07a_subscribe_credit(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(
                    source_uid=TestAIOpenScaleClient.model_uid_1,
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

        print("Subscription details: {}".format(subscription.get_details()))
        TestAIOpenScaleClient.subscription_uid = subscription.uid
        TestAIOpenScaleClient.subscription_s1 = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)

    def test_07b_subscribe_interest(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(
            source_uid=TestAIOpenScaleClient.model_uid_2,
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

        print("Subscription details: {}".format(subscription.get_details()))

        TestAIOpenScaleClient.subscription_uid = subscription.uid
        TestAIOpenScaleClient.subscription_s2 = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)

    def test_07c_subscribe_currency(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(
            source_uid=TestAIOpenScaleClient.model_uid_3,
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

        print("Subscription details: {}".format(subscription.get_details()))

        TestAIOpenScaleClient.subscription_uid = subscription.uid
        TestAIOpenScaleClient.subscription_s3 = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)

    def test_08a_score_credit(self):
        deployment_details = self.wml_client.deployments.get_details(TestAIOpenScaleClient.deployment_uid_1)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        fields = ["CheckingStatus", "LoanDuration", "CreditHistory", "LoanPurpose", "LoanAmount", "ExistingSavings",
                  "EmploymentDuration", "InstallmentPercent", "Sex", "OthersOnLoan", "CurrentResidenceDuration",
                  "OwnsProperty", "Age", "InstallmentPlans", "Housing", "ExistingCreditsCount", "Job", "Dependents",
                  "Telephone", "ForeignWorker"]
        values = [
            ["no_checking", 13, "credits_paid_to_date", "car_new", 1343, "100_to_500", "1_to_4", 2, "female", "none", 3,
             "savings_insurance", 46, "none", "own", 2, "skilled", 1, "none", "yes"],
            ["no_checking", 24, "prior_payments_delayed", "furniture", 4567, "500_to_1000", "1_to_4", 4, "male", "none",
             4, "savings_insurance", 36, "none", "free", 2, "management_self-employed", 1, "none", "yes"],
            ["0_to_200", 26, "all_credits_paid_back", "car_new", 863, "less_100", "less_1", 2, "female", "co-applicant",
             2, "real_estate", 38, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["0_to_200", 14, "no_credits", "car_new", 2368, "less_100", "1_to_4", 3, "female", "none", 3, "real_estate",
             29, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["0_to_200", 4, "no_credits", "car_new", 250, "less_100", "unemployed", 2, "female", "none", 3,
             "real_estate", 23, "none", "rent", 1, "management_self-employed", 1, "none", "yes"],
            ["no_checking", 17, "credits_paid_to_date", "car_new", 832, "100_to_500", "1_to_4", 2, "male", "none", 2,
             "real_estate", 42, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["no_checking", 33, "outstanding_credit", "appliances", 5696, "unknown", "greater_7", 4, "male",
             "co-applicant", 4, "unknown", 54, "none", "free", 2, "skilled", 1, "yes", "yes"],
            ["0_to_200", 13, "prior_payments_delayed", "retraining", 1375, "100_to_500", "4_to_7", 3, "male", "none", 3,
             "real_estate", 37, "none", "own", 2, "management_self-employed", 1, "none", "yes"]
        ]

        payload_scoring = {"fields": fields, "values": values}
        print("Scoring payload: {}".format(payload_scoring))

        scoring_records = 32
        for i in range(0, scoring_records):
            scorings = self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
            self.assertIsNotNone(scorings)

        print("Scoring output: {}".format(scorings))

    def test_08b_score_interest(self):
        deployment_details = self.wml_client.deployments.get_details(TestAIOpenScaleClient.deployment_uid_2)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        fields = ["CheckingStatus", "LoanDuration", "CreditHistory", "LoanPurpose", "LoanAmount", "ExistingSavings",
                  "EmploymentDuration", "InstallmentPercent", "Sex", "OthersOnLoan", "CurrentResidenceDuration",
                  "OwnsProperty", "Age", "InstallmentPlans", "Housing", "ExistingCreditsCount", "Job", "Dependents",
                  "Telephone", "ForeignWorker"]
        values = [
            ["no_checking", 13, "credits_paid_to_date", "car_new", 1343, "100_to_500", "1_to_4", 2, "female", "none", 3,
             "savings_insurance", 46, "none", "own", 2, "skilled", 1, "none", "yes"],
            ["no_checking", 24, "prior_payments_delayed", "furniture", 4567, "500_to_1000", "1_to_4", 4, "male", "none",
             4, "savings_insurance", 36, "none", "free", 2, "management_self-employed", 1, "none", "yes"],
            ["0_to_200", 26, "all_credits_paid_back", "car_new", 863, "less_100", "less_1", 2, "female", "co-applicant",
             2, "real_estate", 38, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["0_to_200", 14, "no_credits", "car_new", 2368, "less_100", "1_to_4", 3, "female", "none", 3, "real_estate",
             29, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["0_to_200", 4, "no_credits", "car_new", 250, "less_100", "unemployed", 2, "female", "none", 3,
             "real_estate", 23, "none", "rent", 1, "management_self-employed", 1, "none", "yes"],
            ["no_checking", 17, "credits_paid_to_date", "car_new", 832, "100_to_500", "1_to_4", 2, "male", "none", 2,
             "real_estate", 42, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["no_checking", 33, "outstanding_credit", "appliances", 5696, "unknown", "greater_7", 4, "male",
             "co-applicant", 4, "unknown", 54, "none", "free", 2, "skilled", 1, "yes", "yes"],
            ["0_to_200", 13, "prior_payments_delayed", "retraining", 1375, "100_to_500", "4_to_7", 3, "male", "none", 3,
             "real_estate", 37, "none", "own", 2, "management_self-employed", 1, "none", "yes"]
        ]

        payload_scoring = {"fields": fields, "values": values}
        print("Scoring payload: {}".format(payload_scoring))

        scoring_records = 32
        for i in range(0, scoring_records):
            scorings = self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
            self.assertIsNotNone(scorings)

        print("Scoring output: {}".format(scorings))

    def test_08c_score_currency(self):
        deployment_details = self.wml_client.deployments.get_details(TestAIOpenScaleClient.deployment_uid_3)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        fields = ["CheckingStatus", "LoanDuration", "CreditHistory", "LoanPurpose", "LoanAmount", "ExistingSavings",
                  "EmploymentDuration", "InstallmentPercent", "Sex", "OthersOnLoan", "CurrentResidenceDuration",
                  "OwnsProperty", "Age", "InstallmentPlans", "Housing", "ExistingCreditsCount", "Job", "Dependents",
                  "Telephone", "ForeignWorker"]
        values = [
            ["no_checking", 13, "credits_paid_to_date", "car_new", 1343, "100_to_500", "1_to_4", 2, "female", "none", 3,
             "savings_insurance", 46, "none", "own", 2, "skilled", 1, "none", "yes"],
            ["no_checking", 24, "prior_payments_delayed", "furniture", 4567, "500_to_1000", "1_to_4", 4, "male", "none",
             4, "savings_insurance", 36, "none", "free", 2, "management_self-employed", 1, "none", "yes"],
            ["0_to_200", 26, "all_credits_paid_back", "car_new", 863, "less_100", "less_1", 2, "female", "co-applicant",
             2, "real_estate", 38, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["0_to_200", 14, "no_credits", "car_new", 2368, "less_100", "1_to_4", 3, "female", "none", 3, "real_estate",
             29, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["0_to_200", 4, "no_credits", "car_new", 250, "less_100", "unemployed", 2, "female", "none", 3,
             "real_estate", 23, "none", "rent", 1, "management_self-employed", 1, "none", "yes"],
            ["no_checking", 17, "credits_paid_to_date", "car_new", 832, "100_to_500", "1_to_4", 2, "male", "none", 2,
             "real_estate", 42, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["no_checking", 33, "outstanding_credit", "appliances", 5696, "unknown", "greater_7", 4, "male",
             "co-applicant", 4, "unknown", 54, "none", "free", 2, "skilled", 1, "yes", "yes"],
            ["0_to_200", 13, "prior_payments_delayed", "retraining", 1375, "100_to_500", "4_to_7", 3, "male", "none", 3,
             "real_estate", 37, "none", "own", 2, "management_self-employed", 1, "none", "yes"]
        ]

        payload_scoring = {"fields": fields, "values": values}
        print("Scoring payload: {}".format(payload_scoring))

        scoring_records = 32
        for i in range(0, scoring_records):
            scorings = self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
            self.assertIsNotNone(scorings)

        print("Scoring output: {}".format(scorings))

    def test_09_enable_drift(self):
        self.subscription_s1.drift_monitoring.enable(threshold=0.6, min_records=10, model_path=os.path.join(self.drift_model_path, self.drift_model_name))
        drift_monitor_details = self.subscription_s1.monitoring.get_details(monitor_uid='drift')
        print('drift monitor details', drift_monitor_details)

    def test_10_run_drift(self):
        result = self.subscription_s1.drift_monitoring.run(background_mode=False)
        print('drift run', result)
        self.assertTrue('predicted_accuracy' in str(result))

    def test_11_setup_quality_monitoring(self):
        self.subscription_s1.quality_monitoring.enable(threshold=0.8, min_records=5)

    def test_12_setup_fairness_monitoring(self):
        from ibm_ai_openscale.supporting_classes import Feature

        self.assertIsNotNone(TestAIOpenScaleClient.data_df)

        TestAIOpenScaleClient.subscription_s2.fairness_monitoring.enable(
            features=[
                Feature("Sex", majority=['male'], minority=['female'], threshold=0.95),
                Feature("Age", majority=[[26, 75]], minority=[[18, 25]], threshold=0.95)
            ],
            favourable_classes=['No Risk'],
            unfavourable_classes=['Risk'],
            min_records=4,
            training_data=TestAIOpenScaleClient.data_df)

    def test_13_inject_quality_metrics(self):
        quality_metric = {'area_under_roc': 0.666}
        self.subscription_s1.monitoring.store_metrics(monitor_uid='quality', metrics=quality_metric)

        time.sleep(10)

        self.subscription_s1.quality_monitoring.show_table()
        self.subscription_s1.monitoring.show_table(monitor_uid='quality')

        quality_metrics_py = self.subscription_s1.quality_monitoring.get_table_content(format='python')
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

        details = self.subscription_s1.monitoring.store_measurements(monitor_uid='quality', measurements=measurements)
        print('Measurement details', details)

        time.sleep(10)

        measurement_id = details[0]['measurement_id']

        print('measurement_id', measurement_id)
        self.subscription_s1.quality_monitoring.show_table()
        self.subscription_s1.quality_monitoring.show_confusion_matrix(measurement_id=measurement_id)

        quality_metrics_py = self.subscription_s1.quality_monitoring.get_table_content(format='python')
        self.assertTrue(str(quality_metric['area_under_roc']) in str(quality_metrics_py))
        self.assertTrue('20' in str(quality_metrics_py))

        self.subscription_s1.quality_monitoring.show_table()
        self.subscription_s1.monitoring.show_table(monitor_uid='quality')

    def test_15_inject_performance_metrics(self):
        if "ICP" in get_env():
            self.skipTest("Performance monitoring is not working on ICP with WML scoring.")

        performance_metric = {'records': 245, 'response_time': 62.33809845686894}
        self.subscription_s1.monitoring.store_metrics(monitor_uid='performance', metrics=performance_metric)

        time.sleep(10)

        self.subscription_s1.performance_monitoring.show_table()

        performance_table_python = self.subscription_s1.performance_monitoring.get_table_content(format='python')
        self.assertTrue('62.33809845686894' in str(performance_table_python))

    def test_16_inject_performance_measurements(self):
        measurements = [
            MeasurementRecord(metrics={'records': 245, 'response_time': 62.33809845686894}),
            MeasurementRecord(metrics={'records': 45, 'response_time': 2.33809845686894})
        ]

        details = self.subscription_s1.monitoring.store_measurements(monitor_uid='performance',
                                                                               measurements=measurements)
        time.sleep(10)

        self.assertTrue('2.33809845686894' in str(details))

    def test_17_inject_fairness_metrics(self):
        fairness_metric = {'metrics': [{'feature': 'Sex', 'majority': {'values': [{'value': 'male', 'distribution': {'male': [{'count': 65, 'label': 'No Risk', 'is_favourable': True}, {'count': 4, 'label': 'Risk', 'is_favourable': False}]}, 'fav_class_percent': 95.0}], 'total_fav_percent': 95.0, 'total_rows_percent': 33.33333333333333}, 'minority': {'values': [{'value': 'female', 'is_biased': True, 'distribution': {'female': [{'count': 29, 'label': 'No Risk', 'is_favourable': True}, {'count': 2, 'label': 'Risk', 'is_favourable': False}]}, 'fairness_value': 0.947333, 'fav_class_percent': 90.0}], 'total_fav_percent': 90.0, 'total_rows_percent': 33.33333333333333}}, {'feature': 'Age', 'majority': {'values': [{'value': [26, 75], 'distribution': {'26': [{'count': 4, 'label': 'No Risk', 'is_favourable': True}], '28': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '29': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '30': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '31': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '32': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '33': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '34': [{'count': 1, 'label': 'Risk', 'is_favourable': False}, {'count': 4, 'label': 'No Risk', 'is_favourable': True}], '35': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '36': [{'count': 3, 'label': 'No Risk', 'is_favourable': True}], '37': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '38': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '39': [{'count': 3, 'label': 'No Risk', 'is_favourable': True}, {'count': 1, 'label': 'Risk', 'is_favourable': False}], '40': [{'count': 3, 'label': 'No Risk', 'is_favourable': True}], '41': [{'count': 3, 'label': 'No Risk', 'is_favourable': True}], '43': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '45': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '47': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '49': [{'count': 1, 'label': 'Risk', 'is_favourable': False}], '50': [{'count': 3, 'label': 'No Risk', 'is_favourable': True}, {'count': 1, 'label': 'Risk', 'is_favourable': False}], '52': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '54': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '55': [{'count': 1, 'label': 'Risk', 'is_favourable': False}, {'count': 1, 'label': 'No Risk', 'is_favourable': True}], '71': [{'count': 1, 'label': 'Risk', 'is_favourable': False}]}, 'fav_class_percent': 88.43537414965986}], 'total_fav_percent': 88.43537414965986, 'total_rows_percent': 49.0}, 'minority': {'values': [{'value': [18, 25], 'is_biased': False, 'distribution': {'19': [{'count': 16, 'label': 'No Risk', 'is_favourable': True}], '20': [{'count': 16, 'label': 'No Risk', 'is_favourable': True}], '21': [{'count': 11, 'label': 'No Risk', 'is_favourable': True}], '23': [{'count': 2, 'label': 'No Risk', 'is_favourable': True}], '24': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}], '25': [{'count': 1, 'label': 'No Risk', 'is_favourable': True}]}, 'fairness_value': 1.101, 'fav_class_percent': 97.38562091503267}], 'total_fav_percent': 97.38562091503267, 'total_rows_percent': 51.0}, 'bias_source': {'values': []}}], 'score_type': 'desperate impact', 'response_time': '13.128683', 'rows_analyzed': 100, 'perturbed_data_size': 200, 'manual_labelling_store': 'Manual_Labeling_dd79dd1b-0afc-436e-9999-6fd6414f81c2'}
        self.subscription_s2.monitoring.store_metrics(monitor_uid='fairness', metrics=fairness_metric)

        time.sleep(10)

        self.subscription_s2.fairness_monitoring.show_table()

        python_table_content = self.subscription_s2.fairness_monitoring.get_table_content(format='python')
        self.assertTrue('0.947333' in str(python_table_content))

    def test_18_enable_drift(self):
        self.subscription_s3.drift_monitoring.enable(threshold=0.6, min_records=10,
                                                     model_path=os.path.join(self.drift_model_path,
                                                                             self.drift_model_name))
        drift_monitor_details = self.subscription_s3.monitoring.get_details(monitor_uid='drift')
        print('drift monitor details', drift_monitor_details)

    def test_19_run_drift(self):
        result = self.subscription_s3.drift_monitoring.run(background_mode=False)
        print('drift run', result)
        self.assertTrue('predicted_accuracy' in str(result))

    def test_20_get_details(self):

        print("all subscriptions:")
        print(self.ai_client.data_mart.subscriptions.get_details())

        print("\nsubscription 1:")
        print(self.subscription_s1.get_details())

        print("subscription 1 metrics:")
        print(self.subscription_s1.get_deployment_metrics())

        print("\nsubscription 2:")
        print(self.subscription_s2.get_details())

        print("subscription 2 metrics:")
        print(self.subscription_s2.get_deployment_metrics())

        print("\nsubscription 3:")
        print(self.subscription_s3.get_details())

        print("subscription 3 metrics:")
        print(self.subscription_s3.get_deployment_metrics())

        print("All metrics:\n")
        print(self.ai_client.data_mart.get_deployment_metrics())


if __name__ == '__main__':
    unittest.main()
