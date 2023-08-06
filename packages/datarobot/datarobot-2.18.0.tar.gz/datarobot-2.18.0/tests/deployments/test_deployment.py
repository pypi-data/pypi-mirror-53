import json

import dateutil
import pytest
import responses

from datarobot import Deployment
from datarobot.utils import from_api
from tests.utils import request_body_to_json


def assert_deployment(deployment, deployment_data):
    def assert_health(health_from_client, health_from_api):
        assert health_from_client['status'] == health_from_client['status']
        if 'startDate' in health_from_api and health_from_api['startDate']:
            timestamp = health_from_api['startDate']
            assert health_from_client.get('start_date') == dateutil.parser.parse(timestamp)
        else:
            assert 'start_date' not in health_from_client
        if 'endDate' in health_from_api and health_from_api['endDate']:
            timestamp = health_from_api['endDate']
            assert health_from_client.get('end_date') == dateutil.parser.parse(timestamp)
        else:
            assert 'end_date' not in health_from_client

    assert deployment.id == deployment_data['id']
    assert deployment.label == deployment_data['label']
    assert deployment.description == deployment_data['description']

    assert deployment.model == from_api(deployment_data['model'])
    assert deployment.default_prediction_server == from_api(
        deployment_data['defaultPredictionServer'])
    assert deployment.capabilities == from_api(deployment_data['capabilities'])
    assert deployment.permissions == deployment_data['permissions']

    prediction_usage_from_api = deployment_data['predictionUsage']
    assert deployment.prediction_usage['daily_rates'] == prediction_usage_from_api['dailyRates']
    if prediction_usage_from_api['lastTimestamp']:
        assert deployment.prediction_usage['last_timestamp'] == dateutil.parser.parse(
            prediction_usage_from_api['lastTimestamp'])

    assert_health(deployment.service_health, deployment_data['serviceHealth'])
    assert_health(deployment.model_health, deployment_data['modelHealth'])
    assert_health(deployment.accuracy_health, deployment_data['accuracyHealth'])

    repr = 'Deployment({label})'.format(label=deployment_data['label'])
    assert str(deployment) == repr


@pytest.fixture()
def deployments_list_response_data(deployments_data):
    return {
        'count': 1,
        'next': None,
        'previous': None,
        'data': deployments_data
    }


@pytest.fixture()
def deployment_list_response(unittest_endpoint, deployments_list_response_data):
    url = '{}/{}/'.format(unittest_endpoint, 'deployments')
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type='application/json',
        body=json.dumps(deployments_list_response_data)
    )


@pytest.fixture()
def deployment_get_response(unittest_endpoint, deployments_data):
    for deployment_data in deployments_data:
        url = '{}/{}/{}/'.format(unittest_endpoint, 'deployments', deployment_data['id'])
        responses.add(
            responses.GET,
            url,
            status=200,
            content_type='application/json',
            body=json.dumps(deployment_data)
        )


@pytest.fixture()
def deployment_delete_response(unittest_endpoint, deployments_data):
    for deployment_data in deployments_data:
        url = '{}/{}/{}/'.format(unittest_endpoint, 'deployments', deployment_data['id'])
        responses.add(
            responses.DELETE,
            url,
            status=204
        )


@responses.activate
@pytest.mark.usefixtures('deployment_get_response')
def test_get_deployment(deployments_data):
    for deployment_data in deployments_data:
        deployment = Deployment.get(deployment_data['id'])
        assert_deployment(deployment, deployment_data)


@responses.activate
@pytest.mark.usefixtures('deployment_get_response', 'deployment_delete_response')
def test_delete_deployment(deployment_data):
    deployment = Deployment.get(deployment_data['id'])
    deployment.delete()

    assert responses.calls[1].request.method == 'DELETE'
    assert responses.calls[1].request.url.endswith('/deployments/5c6f7a9e9ca9b20017ff95a2/')


class TestDeploymentCreateFromLearningModel(object):
    @pytest.fixture
    def learning_model_create_response(self, unittest_endpoint, deployment_data):
        url = '{}/{}/{}/'.format(unittest_endpoint, 'deployments', 'fromLearningModel')
        responses.add(
            responses.POST,
            url,
            body=json.dumps({'id': deployment_data['id']}),
            status=200,
            content_type='application/json')

    @responses.activate
    @pytest.mark.usefixtures('learning_model_create_response', 'deployment_get_response')
    def test_create_minimum(self):
        Deployment.create_from_learning_model('5c76a543962d744efba25b85', 'loan is bad')

        create_body = request_body_to_json(responses.calls[0].request)
        assert create_body['modelId'] == '5c76a543962d744efba25b85'
        assert create_body['label'] == 'loan is bad'
        assert 'description' not in create_body
        assert 'defaultPredictionServerId' not in create_body

    @responses.activate
    @pytest.mark.usefixtures('learning_model_create_response', 'deployment_get_response')
    def test_create_all_options(self):
        Deployment.create_from_learning_model(
            '5c76a543962d744efba25b85', 'loan is bad',
            'predict if a loan is gonna default', '5c0fcdb8962d74370dd0c38e')

        create_body = request_body_to_json(responses.calls[0].request)
        assert create_body['modelId'] == '5c76a543962d744efba25b85'
        assert create_body['label'] == 'loan is bad'
        assert create_body['description'] == 'predict if a loan is gonna default'
        assert create_body['defaultPredictionServerId'] == '5c0fcdb8962d74370dd0c38e'


class TestDeploymentList(object):
    @responses.activate
    @pytest.mark.usefixtures('deployment_list_response')
    def test_list_deployment(self, deployments_data):
        deployments_data = {item['id']: item for item in deployments_data}
        deployments = Deployment.list()
        assert len(deployments) == len(deployments_data)
        for deployment in deployments:
            assert_deployment(deployment, deployments_data[deployment.id])

    @responses.activate
    @pytest.mark.usefixtures('deployment_list_response')
    def test_sort(self):
        Deployment.list(order_by='-label')
        assert 'deployments/?orderBy=-label' in responses.calls[0].request.url

    @responses.activate
    @pytest.mark.usefixtures('deployment_list_response')
    def test_search(self):
        Deployment.list(search='readmitted')
        assert 'deployments/?search=readmitted' in responses.calls[0].request.url
