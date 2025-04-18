import os

import mlflow


def start_mlflow_run(run_name: str = "transcription-run", experiment_name: str = "TranscriptionExperiments"):
    mlflow.set_tracking_uri("file:./mlruns")  # You can change this to a remote URI
    mlflow.set_experiment(experiment_name)
    return mlflow.start_run(run_name=run_name)

def log_params(params: dict):
    for key, value in params.items():
        mlflow.log_param(key, value)

def log_metrics(metrics: dict):
    for key, value in metrics.items():
        mlflow.log_metric(key, value)

def log_artifact_text(filename: str, content: str):
    filepath = f"/tmp/{filename}"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    mlflow.log_artifact(filepath)
    os.remove(filepath)
