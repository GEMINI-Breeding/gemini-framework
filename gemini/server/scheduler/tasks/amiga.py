from dagster import asset, AssetExecutionContext
from dagster_aws.s3.resources import S3Resource
from dagster import asset, Config

from typing import List

from gemini.api.sensors import amiga

class AmigaConfig(Config):
    file_path: str

@asset
def events_index(context: AssetExecutionContext, config: AmigaConfig) -> List[dict]:
    try:
        index = amiga.get_events_index(config.file_path)
        context.log.info(f"Events index: {index}")
        return index
    except Exception as e:
        context.log.error(f"Error getting events index: {e}")
        return None
