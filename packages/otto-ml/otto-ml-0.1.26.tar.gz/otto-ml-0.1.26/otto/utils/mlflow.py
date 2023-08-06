import mlflow


def create_experiment(tracking_uri, project_name):
    mlflow_client = mlflow.tracking.MlflowClient(tracking_uri)
    return mlflow_client.create_experiment(project_name)
