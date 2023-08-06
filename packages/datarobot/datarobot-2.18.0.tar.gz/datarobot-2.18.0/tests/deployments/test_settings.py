import json

import pytest
import responses

from datarobot import Deployment
from datarobot.utils import from_api
from tests.utils import request_body_to_json


@pytest.fixture()
def deployment_settings_response():
    return {
        'targetDrift': {'enabled': True},
        'featureDrift': {'enabled': True},
        'otherSettings': {'test': 'value'}
    }


@responses.activate
@pytest.mark.usefixtures('deployment_get_response')
def test_get_drift_tracking_settings(unittest_endpoint, deployment_data,
                                     deployment_settings_response):
    deployment_id = deployment_data['id']
    url = '{}/deployments/{}/settings/'.format(unittest_endpoint, deployment_id)
    responses.add(
        responses.GET,
        url,
        body=json.dumps(deployment_settings_response),
        status=200,
        content_type='application/json')

    deployment = Deployment.get(deployment_id)
    settings = deployment.get_drift_tracking_settings()

    response = from_api(deployment_settings_response)
    expected_settings = {'target_drift': response['target_drift'],
                         'feature_drift': response['feature_drift']}
    assert settings == expected_settings


@responses.activate
@pytest.mark.usefixtures('deployment_get_response')
def test_cannot_update_nothing(deployment_data):
    deployment_id = deployment_data['id']
    deployment = Deployment.get(deployment_id)
    with pytest.raises(ValueError):
        deployment.update_drift_tracking_settings()


@responses.activate
@pytest.mark.usefixtures('deployment_get_response')
@pytest.mark.parametrize('param, expected_request', [
    ({'target_drift_enabled': True}, {'targetDrift': {'enabled': True}}),
    ({'feature_drift_enabled': False}, {'featureDrift': {'enabled': False}}),
    ({'target_drift_enabled': True, 'feature_drift_enabled': True},
     {'targetDrift': {'enabled': True}, 'featureDrift': {'enabled': True}}),
    ({'target_drift_enabled': False, 'feature_drift_enabled': False},
     {'targetDrift': {'enabled': False}, 'featureDrift': {'enabled': False}}),
])
def test_update_drift_tracking_settings(unittest_endpoint, deployment_data,
                                        param, expected_request):
    deployment_id = deployment_data['id']
    update_setting_url = '{}/deployments/{}/settings/'.format(unittest_endpoint, deployment_id)
    deployment_url = '{}/deployments/{}/'.format(unittest_endpoint, deployment_id)
    status_url = '{}/status_url'.format(unittest_endpoint)
    responses.add(
        responses.PATCH,
        update_setting_url,
        headers={'Location': status_url},
        status=202)
    responses.add(
        responses.GET,
        status_url,
        headers={'Location': deployment_url},
        status=303)

    deployment = Deployment.get(deployment_id)
    deployment.update_drift_tracking_settings(**param)

    request_body = request_body_to_json(responses.calls[1].request)
    assert request_body == expected_request
