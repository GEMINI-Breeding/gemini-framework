from gemini.scheduler.flows.dataset import dataset_flow_deployments
from gemini.scheduler.flows.storage import minio_flow_deployments
from gemini.scheduler.flows.settings import settings_flow_deployments

all_flow_deployments = [
    *dataset_flow_deployments,
    *settings_flow_deployments,
    *minio_flow_deployments,
]