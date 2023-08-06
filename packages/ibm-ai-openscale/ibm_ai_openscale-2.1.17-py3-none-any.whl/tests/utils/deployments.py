import os
import pandas as pd
from abc import ABC, abstractmethod
from .configuration import get_client


class WMLDeployment(ABC):
    scoring_url = None
    deployment_uid = None
    asset_uid = None

    def __init__(self, name, asset_name):
        self.name = name
        self.asset_name = asset_name
        self.wml_client = get_client()

        self._get_ids()
        if self.deployment_uid is None:
            self.deploy()
            self._get_ids()

    def get_asset_id(self):
        return self.asset_uid

    def get_deployment_id(self):
        return self.deployment_uid

    def score(self, payload):
        self.wml_client.deployments.score(self.scoring_url, payload)

    @abstractmethod
    def deploy(self):
        pass

    def _get_ids(self):
        for deployment in self.wml_client.deployments.get_details()['resources']:
            if deployment['entity']['name'] == self.name:
                self.asset_uid = deployment['entity']['deployable_asset']['guid']
                self.deployment_uid = deployment['metadata']['guid']
                self.scoring_url = deployment['entity']['scoring_url']


class GermanCreditRisk(WMLDeployment):
    def __init__(self):
        super(GermanCreditRisk, self).__init__(
            name="AIOS Spark German Risk deployment",
            asset_name="AIOS Spark German Risk model"
        )

    def deploy(self):
        from pyspark import SparkContext, SQLContext
        from pyspark.ml import Pipeline
        from pyspark.ml.classification import RandomForestClassifier
        from pyspark.ml.evaluation import BinaryClassificationEvaluator
        from pyspark.ml.feature import StringIndexer, VectorAssembler, IndexToString

        ctx = SparkContext.getOrCreate()
        sc = SQLContext(ctx)

        spark_df = sc.read.format(
            "com.databricks.spark.csv").option(
            "header", "true").option(
            "delimiter", ",").option(
            "inferSchema", "true").load(
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
                       "EmploymentDuration_IX", "Sex_IX", "OthersOnLoan_IX", "OwnsProperty_IX",
                       "InstallmentPlans_IX",
                       "Housing_IX", "Job_IX", "Telephone_IX", "ForeignWorker_IX", "LoanDuration", "LoanAmount",
                       "InstallmentPercent", "CurrentResidenceDuration", "LoanDuration", "Age",
                       "ExistingCreditsCount",
                       "Dependents"], outputCol="features")

        classifier = RandomForestClassifier(featuresCol="features")

        pipeline = Pipeline(
            stages=[si_CheckingStatus, si_CreditHistory, si_EmploymentDuration, si_ExistingSavings,
                    si_ForeignWorker,
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

        model_props = {
            self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
            self.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                {
                    "name": "AUC",
                    "value": auc,
                    "threshold": 0.8
                }
            ]
        }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(
            model=model,
            meta_props=model_props,
            training_data=train_data,
            pipeline=pipeline)

        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        deployment = self.wml_client.deployments.create(
            artifact_uid=self.asset_uid,
            name=self.name,
            asynchronous=False)

        self.deployment_uid = self.wml_client.deployments.get_uid(deployment)

        deployment_details = self.wml_client.deployments.get_details(self.deployment_uid)


class Drug(WMLDeployment):
    def __init__(self):
        super(Drug, self).__init__(
            name="AIOS Spark Drugs feedback deployment",
            asset_name="AIOS Spark Drugs feedback model"
        )

    def deploy(self):
        from pyspark import SparkContext, SQLContext
        from pyspark.ml import Pipeline
        from pyspark.ml.classification import RandomForestClassifier
        from pyspark.ml.evaluation import BinaryClassificationEvaluator
        from pyspark.ml.feature import StringIndexer, VectorAssembler, IndexToString

        ctx = SparkContext.getOrCreate()
        sc = SQLContext(ctx)

        spark_df = sc.read.format(
            "com.databricks.spark.csv").option(
            "header", "true").option(
            "delimiter", ",").option(
            "inferSchema", "true").load(
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
                       "EmploymentDuration_IX", "Sex_IX", "OthersOnLoan_IX", "OwnsProperty_IX",
                       "InstallmentPlans_IX",
                       "Housing_IX", "Job_IX", "Telephone_IX", "ForeignWorker_IX", "LoanDuration", "LoanAmount",
                       "InstallmentPercent", "CurrentResidenceDuration", "LoanDuration", "Age",
                       "ExistingCreditsCount",
                       "Dependents"], outputCol="features")

        classifier = RandomForestClassifier(featuresCol="features")

        pipeline = Pipeline(
            stages=[si_CheckingStatus, si_CreditHistory, si_EmploymentDuration, si_ExistingSavings,
                    si_ForeignWorker,
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

        model_props = {
            self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
            self.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                {
                    "name": "AUC",
                    "value": auc,
                    "threshold": 0.8
                }
            ]
        }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(
            model=model,
            meta_props=model_props,
            training_data=train_data,
            pipeline=pipeline)

        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        deployment = self.wml_client.deployments.create(
            artifact_uid=self.asset_uid,
            name=self.name,
            asynchronous=False)

        self.deployment_uid = self.wml_client.deployments.get_uid(deployment)

        deployment_details = self.wml_client.deployments.get_details(self.deployment_uid)


class BostonHouse(WMLDeployment):
    def __init__(self):
        super(BostonHouse, self).__init__(
            name="AIOS Xgboost Boston House Deployment",
            asset_name="AIOS Xgboost Boston House Model"
        )

    def deploy(self):
        from sklearn.model_selection import train_test_split
        import xgboost as xgb
        from sklearn.datasets import load_boston

        boston_dataset = load_boston()
        model_meta_props = {
            self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
            self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
            self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "xgboost",
            self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "0.8",
        }

        data = pd.DataFrame(boston_dataset.data)
        data.columns = boston_dataset.feature_names
        X, y = data.iloc[:, :-1], data.iloc[:, -1]
        data_dmatrix = xgb.DMatrix(data=X, label=y)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
        xg_reg = xgb.XGBRegressor(objective='reg:linear', colsample_bytree=0.3, learning_rate=0.1, max_depth=5,
                                  alpha=10, n_estimators=10)

        xg_reg.fit(X_train, y_train)

        # preds = xg_reg.predict(X_test)
        # print(preds)
        #
        # bst = xgb.XGBRegressor()
        # bst.load_model("artifacts/XGboost/boston-house-xgboost.model")

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=xg_reg, meta_props=model_meta_props)

        print("Published model details:\n{}".format(published_model_details))
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Deploying model: {}, deployment name: {}".format(self.asset_name, self.name))
        deployment = self.wml_client.deployments.create(
            artifact_uid=self.asset_uid,
            name=self.name,
            asynchronous=False)
        self.deployment_uid = self.wml_client.deployments.get_uid(deployment)

        deployment_details = self.wml_client.deployments.get_details(self.deployment_uid)
        print("Deployment details:\n{}".format(deployment_details))

