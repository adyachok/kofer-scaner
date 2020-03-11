import faust
from typing import Any, List


class ImageTriggerInfo(faust.Record):
    image_name: str
    trigger_type: str


class DeploymentConfigInfo(faust.Record):
    name: str
    latest_version: int
    image_triggers: List[ImageTriggerInfo]


class ModelMetadata(faust.Record):
    name: str
    latest_version: int
    server_metadata: Any
    business_metadata: Any
