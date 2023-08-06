from collections import defaultdict
from datetime import datetime

import dateutil
import pandas as pd
import pytz
import trafaret as t

from datarobot.enums import DEFAULT_MAX_WAIT
from datarobot.models.api_object import APIObject
from .accuracy import Accuracy, AccuracyOverTime
from .service_stats import ServiceStats, ServiceStatsOverTime
from ..utils import encode_utf8_if_py2, get_id_from_location, from_api
from ..utils.pagination import unpaginate
from ..utils.waiters import wait_for_async_resolution


class Deployment(APIObject):
    """A deployment created from a DataRobot model.

    Attributes
    ----------
    id : str
        the id of the deployment
    label : str
        the label of the deployment
    description : str
        the description of the deployment
    default_prediction_server : dict
        information on the default prediction server of the deployment
    model : dict
        information on the model of the deployment
    capabilities : dict
        information on the capabilities of the deployment
    prediction_usage : dict
        information on the prediction usage of the deployment
    permissions : list
        (New in version v2.18) user's permissions on the deployment
    service_health : dict
        information on the service health of the deployment
    model_health : dict
        information on the model health of the deployment
    accuracy_health : dict
        information on the accuracy health of the deployment
    """

    _path = 'deployments/'
    _default_prediction_server_converter = t.Dict({
        t.Key('id'): t.String(),
        t.Key('url', optional=True): t.String(allow_blank=True),
        t.Key('datarobot-key', optional=True): t.String(allow_blank=True),
    }).allow_extra('*')
    _model_converter = t.Dict({
        t.Key('id', optional=True): t.String(),
        t.Key('type', optional=True): t.String(allow_blank=True),
        t.Key('target_name', optional=True): t.String(allow_blank=True),
        t.Key('project_id', optional=True): t.String(allow_blank=True),
    }).allow_extra('*')
    _capabilities = t.Dict({
        t.Key('supports_drift_tracking', optional=True): t.Bool(),
        t.Key('supports_model_replacement', optional=True): t.Bool(),
    }).allow_extra('*')
    _prediction_usage = t.Dict({
        t.Key('daily_rates', optional=True): t.List(t.Float()),
        t.Key('last_timestamp', optional=True): t.String >> (lambda s: dateutil.parser.parse(s))
    }).allow_extra('*')
    _health = t.Dict({
        t.Key('status', optional=True): t.String(allow_blank=True),
        t.Key('message', optional=True): t.String(allow_blank=True),
        t.Key('start_date', optional=True): t.String >> (lambda s: dateutil.parser.parse(s)),
        t.Key('end_date', optional=True): t.String >> (lambda s: dateutil.parser.parse(s)),
    }).allow_extra('*')
    _converter = t.Dict({
        t.Key('id'): t.String(),
        t.Key('label', optional=True): t.String(allow_blank=True),
        t.Key('description', optional=True): t.String(allow_blank=True) | t.Null(),
        t.Key('default_prediction_server', optional=True): _default_prediction_server_converter,
        t.Key('model', optional=True): _model_converter,
        t.Key('capabilities', optional=True): _capabilities,
        t.Key('prediction_usage', optional=True): _prediction_usage,
        t.Key('permissions', optional=True): t.List(t.String),
        t.Key('service_health', optional=True): _health,
        t.Key('model_health', optional=True): _health,
        t.Key('accuracy_health', optional=True): _health,
    }).allow_extra('*')

    def __init__(self, id=None, label=None, description=None, default_prediction_server=None,
                 model=None, capabilities=None, prediction_usage=None, permissions=None,
                 service_health=None, model_health=None, accuracy_health=None):
        self.id = id
        self.label = label
        self.description = description
        self.default_prediction_server = default_prediction_server
        self.model = model
        self.capabilities = capabilities
        self.prediction_usage = prediction_usage
        self.permissions = permissions
        self.service_health = service_health
        self.model_health = model_health
        self.accuracy_health = accuracy_health

    def __repr__(self):
        return encode_utf8_if_py2(u'{}({})'.format(self.__class__.__name__, self.label or self.id))

    @classmethod
    def create_from_learning_model(cls, model_id, label, description=None,
                                   default_prediction_server_id=None):
        """Create a deployment from a DataRobot model.

        .. versionadded:: v2.17

        Parameters
        ----------
        model_id : str
            id of the DataRobot model to deploy
        label : str
            a human readable label of the deployment
        description : str, optional
            a human readable description of the deployment
        default_prediction_server_id : str
            an identifier of a prediction server to be used as the default prediction server

        Returns
        -------
        deployment : Deployment
            The created deployment

        Examples
        --------
        .. code-block:: python

            from datarobot import Project, Deployment
            project = Project.get('5506fcd38bd88f5953219da0')
            model = project.get_models()[0]
            deployment = Deployment.create_from_learning_model(model.id, 'New Deployment')
            deployment
            >>> Deployment('New Deployment')
        """

        payload = {'model_id': model_id, 'label': label, 'description': description}
        if default_prediction_server_id:
            payload['default_prediction_server_id'] = default_prediction_server_id

        url = '{}fromLearningModel/'.format(cls._path)
        deployment_id = cls._client.post(url, data=payload).json()['id']
        return cls.get(deployment_id)

    @classmethod
    def list(cls, order_by=None, search=None):
        """List all deployments a user can view.

        .. versionadded:: v2.17

        Parameters
        ----------
        order_by : str, optional
            (New in version v2.18) the order to sort the deployment list by, defaults to `label`

            Allowed attributes to sort by are:

            * ``label``
            * ``serviceHealth``
            * ``modelHealth``
            * ``accuracyHealth``
            * ``recentPredictions``
            * ``lastPredictionTimestamp``

            If the sort attribute is preceded by a hyphen, deployments will be sorted in descending
            order, otherwise in ascending order.

            For health related sorting, ascending means failing, warning, passing, unknown.
        search : str, optional
            (New in version v2.18) case insensitive search against deployment's
            label and description

        Returns
        -------
        deployments : list
            a list of deployments the user can view

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment
            deployments = Deployment.list()
            deployments
            >>> [Deployment('New Deployment'), Deployment('Previous Deployment')]
        """

        param = {}
        if order_by:
            param['order_by'] = order_by
        if search:
            param['search'] = search
        data = unpaginate(cls._path, param, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, deployment_id):
        """Get information about a deployment.

        .. versionadded:: v2.17

        Parameters
        ----------
        deployment_id : str
            the id of the deployment

        Returns
        -------
        deployment : Deployment
            the queried deployment

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment
            deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
            deployment.id
            >>>'5c939e08962d741e34f609f0'
            deployment.label
            >>>'New Deployment'
        """

        path = '{}{}/'.format(cls._path, deployment_id)
        return cls.from_location(path)

    def delete(self):
        """
        Delete this deployment.

        .. versionadded:: v2.17
        """

        url = '{}{}/'.format(self._path, self.id)
        self._client.delete(url)

    def replace_model(self, new_model_id, reason):
        """Replace the model used in this deployment. To confirm model replacement eligibility, use
         :meth:`~datarobot.Deployment.validate_replacement_model` beforehand.

        .. versionadded:: v2.17

        Model replacement is an asynchronous process, which means some preparatory work may
        be performed after the initial request is completed. This function will not return until all
        preparatory work is fully finished.

        Predictions made against this deployment will start using the new model as soon as the
        initial request is completed. There will be no interruption for predictions throughout
        the process.

        Parameters
        ----------
        new_model_id : str
            The id of the new model to use
        reason : MODEL_REPLACEMENT_REASON
            The reason for the model replacement. Must be one of 'ACCURACY', 'DATA_DRIFT', 'ERRORS',
            'SCHEDULED_REFRESH', 'SCORING_SPEED', or 'OTHER'. This value will be stored in the model
            history to keep track of why a model was replaced

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment
            deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
            deployment.model['id'], deployment.model['type']
            >>>('5c0a979859b00004ba52e431', 'Decision Tree Classifier (Gini)')

            deployment.replace_model('5c0a969859b00004ba52e41b', MODEL_REPLACEMENT_REASON.ACCURACY)
            deployment.model['id'], deployment.model['type']
            >>>('5c0a969859b00004ba52e41b', 'Support Vector Classifier (Linear Kernel)')
        """

        url = '{}{}/model/'.format(self._path, self.id)
        payload = {'modelId': new_model_id, 'reason': reason}
        response = self._client.patch(url, data=payload)
        deployment_loc = wait_for_async_resolution(self._client, response.headers['Location'])
        deployment_id = get_id_from_location(deployment_loc)
        deployment = Deployment.get(deployment_id)
        self.model = deployment.model

    def validate_replacement_model(self, new_model_id):
        """Validate a model can be used as the replacement model of the deployment.

        .. versionadded:: v2.17

        Parameters
        ----------
        new_model_id : str
            the id of the new model to validate

        Returns
        -------
        status : str
            status of the validation, will be one of 'passing', 'warning' or 'failing'.
            If the status is passing or warning, use :meth:`~datarobot.Deployment.replace_model` to
            perform a model replacement. If the status is failing, refer to ``checks`` for more
            detail on why the new model cannot be used as a replacement.
        message : str
            message for the validation result
        checks : dict
            explain why the new model can or cannot replace the deployment's current model
        """

        url = '{}{}/model/validation/'.format(self._path, self.id)
        payload = {'modelId': new_model_id}
        data = from_api(self._client.post(url, data=payload).json())
        return data.get('status'), data.get('message'), data.get('checks')

    def get_features(self):
        """Retrieve the list of features needed to make predictions on this deployment.

        Notes
        -----

        Each `feature` dict contains the following structure:

        - ``name`` : str, feature name
        - ``feature_type`` : str, feature type
        - ``importance`` : float, numeric measure of the relationship strength between
          the feature and target (independent of model or other features)
        - ``date_format`` : str or None, the date format string for how this feature was
          interpreted, null if not a date feature, compatible with
          https://docs.python.org/2/library/time.html#time.strftime.
        - ``known_in_advance`` : bool, whether the feature was selected as known in advance in
          a time-series model, false for non-time-series models.

        Returns
        -------
        features: list
            a list of `feature` dict

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment
            deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
            features = deployment.get_features()
            features[0]['feature_type']
            >>>'Categorical'
            features[0]['importance']
            >>>0.133
        """
        url = '{}{}/features/'.format(self._path, self.id)
        data = unpaginate(url, {}, self._client)
        return from_api([feature for feature in data], keep_null_keys=True)

    def submit_actuals(self, data):
        """Submit actuals for processing.
        The acutals submitted will be used to calculate accuracy metrics.

        Parameters
        ----------
        data: list or pandas.DataFrame

        If `data` is a list, each item should be a dict-like object with the following keys and
        values; if `data` is a pandas.DataFrame, it should contain the following columns:

        - association_id: str, a unique identifier used with a prediction,
            max length 128 characters
        - actual_value: str or int or float, the actual value of a prediction;
            should be numeric for deployments with regression models or
            string for deployments with classification model
        - was_acted_on: bool, optional, indicates if the prediction was acted on in a way that
            could have affected the actual outcome
        - timestamp: datetime or string in RFC3339 format. If the datetime provided does not
            have a timezone, we assume it is UTC.

        Raises
        ------
        ValueError
            if input data is not a list of dict-like objects or a pandas.DataFrame
            if input data is empty

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment, AccuracyOverTime
            deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
            data = [{
                'association_id': '439917',
                'actual_value': 'True',
                'was_acted_on': True
            }]
            deployment.submit_actuals(data)
        """

        if not isinstance(data, (list, pd.DataFrame)):
            raise ValueError(('data should be either a list of dict-like objects '
                              'or a pandas.DataFrame'))

        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient='records')

        if not data:
            raise ValueError('data should not be empty')

        url = '{}{}/actuals/fromJSON/'.format(self._path, self.id)
        payload_data = []
        for item in data:
            actual = {
                'associationId': item['association_id'],
                'actualValue': item['actual_value'],
            }

            was_acted_on = item.get('was_acted_on')
            if not pd.isna(was_acted_on):
                actual['wasActedOn'] = item['was_acted_on']

            # format timestamp
            timestamp = item.get('timestamp')
            if timestamp and not pd.isna(timestamp):
                timestamp = item['timestamp']
                if isinstance(timestamp, datetime):
                    if not timestamp.tzinfo:
                        timestamp = timestamp.replace(tzinfo=pytz.utc)
                    timestamp = timestamp.isoformat()
                actual['timestamp'] = timestamp

            payload_data.append(actual)
        response = self._client.post(url, data={'data': payload_data})
        wait_for_async_resolution(self._client, response.headers['Location'])

    def get_drift_tracking_settings(self):
        """Retrieve drift tracking settings of this deployment.

        .. versionadded:: v2.17

        Returns
        -------
        settings : dict
            Drift tracking settings of the deployment containing two nested dicts with key
            ``target_drift`` and ``feature_drift``, which are further described below.

            ``Target drift`` setting contains:

            enabled : bool
                If target drift tracking is enabled for this deployment. To create or update
                existing ''target_drift'' settings, see
                :meth:`~datarobot.Deployment.update_drift_tracking_settings`

            ``Feature drift`` setting contains:

            enabled : bool
                If feature drift tracking is enabled for this deployment. To create or update
                existing ''feature_drift'' settings, see
                :meth:`~datarobot.Deployment.update_drift_tracking_settings`
        """

        url = '{}{}/settings/'.format(self._path, self.id)
        response_json = from_api(self._client.get(url).json())
        return {key: value for key, value in response_json.items()
                if key in ['target_drift', 'feature_drift']}

    def update_drift_tracking_settings(self, target_drift_enabled=None, feature_drift_enabled=None,
                                       max_wait=DEFAULT_MAX_WAIT):
        """Update drift tracking settings of this deployment.

        .. versionadded:: v2.17

        Updating drift tracking setting is an asynchronous process, which means some preparatory
        work may be performed after the initial request is completed. This function will not return
        until all preparatory work is fully finished.

        Parameters
        ----------
        target_drift_enabled : bool, optional
            if target drift tracking is to be turned on
        feature_drift_enabled : bool, optional
            if feature drift tracking is to be turned on
        max_wait : int, optional
            seconds to wait for successful resolution
        """

        payload = defaultdict(dict)
        if target_drift_enabled is not None:
            payload['targetDrift']['enabled'] = target_drift_enabled
        if feature_drift_enabled is not None:
            payload['featureDrift']['enabled'] = feature_drift_enabled
        if not payload:
            raise ValueError()

        url = '{}{}/settings/'.format(self._path, self.id)
        response = self._client.patch(url, data=payload)
        wait_for_async_resolution(self._client, response.headers['Location'], max_wait)

    def get_service_stats(self, model_id=None, start_time=None, end_time=None,
                          execution_time_quantile=None, response_time_quantile=None,
                          slow_requests_threshold=None):
        """Retrieve value of service stat metrics over a certain time period.

        .. versionadded:: v2.18

        Parameters
        ----------
        model_id : str, optional
            the id of the model
        start_time : datetime, optional
            start of the time period
        end_time : datetime, optional
            end of the time period
        execution_time_quantile : float, optional
            quantile for `executionTime`, defaults to 0.5
        response_time_quantile : float, optional
            quantile for `responseTime`, defaults to 0.5
        slow_requests_threshold : float, optional
            threshold for `slowRequests`, defaults to 1000

        Returns
        -------
        service_stats : ServiceStats
            the queried service stats metrics information
        """

        kwargs = {
            'model_id': model_id,
            'start_time': start_time,
            'end_time': end_time,
            'execution_time_quantile': execution_time_quantile,
            'response_time_quantile': response_time_quantile,
            'slow_requests_threshold': slow_requests_threshold,
        }
        return ServiceStats.get(self.id, **kwargs)

    def get_service_stats_over_time(self, metric=None, model_id=None, start_time=None,
                                    end_time=None, bucket_size=None, quantile=None, threshold=None):
        """Retrieve information about how a service stat metric changes over a certain time period.

        .. versionadded:: v2.18

        Parameters
        ----------
        metric : SERVICE_STAT_METRIC, optional
            the service stat metric to retrieve
        model_id : str, optional
            the id of the model
        start_time : datetime, optional
            start of the time period
        end_time : datetime, optional
            end of the time period
        bucket_size : str, optional
            time duration of a bucket, in ISO 8601 time duration format
        quantile : float, optional
            quantile for 'executionTime' or 'responseTime', ignored when querying other metrics
        threshold : int, optional
            threshold for 'slowQueries', ignored when querying other metrics

        Returns
        -------
        service_stats_over_time : ServiceStatsOverTime
            the queried service stats metric over time information
        """

        kwargs = {
            'metric': metric,
            'model_id': model_id,
            'start_time': start_time,
            'end_time': end_time,
            'bucket_size': bucket_size,
            'quantile': quantile,
            'threshold': threshold,
        }
        return ServiceStatsOverTime.get(self.id, **kwargs)

    def get_accuracy(self, model_id=None, start=None, end=None):
        """Retrieve values of accuracy metrics over a certain time period.

        .. versionadded:: v2.18

        Parameters
        ----------
        model_id : str
            the id of the model
        start_time : datetime
            start of the time period
        end_time : datetime
            end of the time period

        Returns
        -------
        accuracy : Accuracy
            the queried accuracy metrics information
        """

        return Accuracy.get(self.id, model_id=model_id, start_time=start, end_time=end)

    def get_accuracy_over_time(self, metric=None, model_id=None,
                               start_time=None, end_time=None, bucket_size=None):
        """Retrieve information about how an accuracy metric changes over a certain time period.

        .. versionadded:: v2.18

        Parameters
        ----------
        metric : ACCURACY_METRIC
            the accuracy metric to retrieve
        model_id : str
            the id of the model
        start_time : datetime
            start of the time period
        end_time : datetime
            end of the time period
        bucket_size : str
            time duration of a bucket, in ISO 8601 time duration format

        Returns
        -------
        accuracy_over_time : AccuracyOverTime
            the queried accuracy metric over time information
        """

        return AccuracyOverTime.get(self.id, metric=metric, model_id=model_id,
                                    start_time=start_time, end_time=end_time,
                                    bucket_size=bucket_size)
