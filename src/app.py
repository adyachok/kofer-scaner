#!/usr/bin/env python
import asyncio
import json
import os

import aiohttp
import faust

from models.faust_dao import DeploymentConfigInfo, ModelMetadata
from utils.logger import get_logger


logger = get_logger('app')

KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL')
if not KAFKA_BROKER_URL:
    KAFKA_BROKER_URL = 'kafka://localhost'
MODEL_REST_PORT = 8501

app = faust.App('scanner', broker=KAFKA_BROKER_URL, debug=True)
model_updates_topic = app.topic('model-updates',
                                value_type=DeploymentConfigInfo)
model_metadata_updates_topic = app.topic('model-metadata-updates',
                                         value_type=DeploymentConfigInfo)


@app.agent(model_updates_topic)
async def scan(dc_infos):
    """Checks from new updates, picks one and gathers model's metadata.
    :param dc_infos: stream of DeploymentConfigInfo
    """
    async for dc in dc_infos:
        logger.info(f'Model {dc.name} with version {dc.latest_version} is '
                    f'updated. Gathering the model metadata.')
        async with aiohttp.ClientSession() as session:
            url = f'http://{dc.name}:{MODEL_REST_PORT}/v1/models/{dc.name}'
            # url = 'https://mod-dummy-501-zz-test.22ad.bi-x.openshiftapps.' \
            # com/v1/models/mod-dummy'
            async with session.get(url) as response:
                if response.status < 400:
                    data = await response.json()
                    logger.info(f'Working with model data {data}')
                    model_version_status = data.get('model_version_status')[0]
                    model_version = model_version_status.get('version')
                    results = await asyncio.gather(
                        *[fetch_server_metadata(session,
                                                model_name=dc.name,
                                                model_version=model_version),
                          fetch_business_metadata(session,
                                                  model_name=dc.name)],
                        return_exceptions=True)
                    logger.info(f'Is about to send next model server '
                                f'metadata {results[0]}')
                    logger.info(f'Is about to send next model business '
                                f'metadata {results[1]}')
                    await model_metadata_updates_topic.send(
                        value=ModelMetadata(name=dc.name,
                                            latest_version=dc.latest_version,
                                            server_metadata=results[0],
                                            business_metadata=results[1]))


async def fetch_server_metadata(session, model_name, model_version):
    url = f'http://{model_name}:{MODEL_REST_PORT}/v1/models/{model_name}/' \
          f'versions/{model_version}/metadata'
    # url = 'https://mod-dummy-501-zz-test.22ad.bi-x.openshiftapps.com/' \
    #       'v1/models/mod-dummy/versions/9/metadata'
    async with session.get(url) as response:
        return await response.json()


async def fetch_business_metadata(session, model_name):
    data = json.dumps({"signature_name": "info", "inputs": True})
    url = f'http://{model_name}:{MODEL_REST_PORT}/v1/models/' \
          f'{model_name}:predict'
    # url = "https://mod-dummy-501-zz-test.22ad.bi-x.openshiftapps.com/" \
    #       "v1/models/mod-dummy:predict"
    async with session.post(url, data=data) as response:
        return await response.json()


if __name__ == '__main__':
    app.main()
