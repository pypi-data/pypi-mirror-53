import logging

from enum import IntEnum
from typing import Tuple, List, Optional

from arps.core.payload_factory import PayloadType
from arps.core.touchpoint import Sensor, Actuator
from arps.core.metrics_logger import Metric


class ActionType(IntEnum):
    event = 0,
    result = 1


class ReflexPolicy:
    '''
    Policy based on Event Condition Action
    '''
    required_metrics: List[Metric]

    def __init__(self,
                 required_sensors: Optional[List[Sensor]] = None,
                 required_actuators: Optional[List[Actuator]] = None):
        '''
        The __init__ method should be called by derived classes to
        defined required sensors and actuators

        Keyword parameters:
        - required_sensors : required sensors that will be read by policy
        - required_actuators : required actuators that will be controlled by policy
        '''

        self._required_sensors = required_sensors or []
        self._required_actuators = required_actuators or []
        self.logger = logging.getLogger(self.__class__.__name__)

    def required_sensors(self):
        '''
        Return all required sensors that are necessary by a policy
        '''
        return self._required_sensors

    def required_actuators(self):
        '''
        Return all required actuators that are necessary by a policy
        '''
        return self._required_actuators

    def event(self, host, event, epoch):
        '''
        Method that will receive the event to be verified
        if the condition is met an action is performed

        Args:
        - host: the agent where the policy is hosted
        - event: event received by the agent
        - epoch: the moment when the event occurred

        Raise:
        - RuntimeError if action does not return a result
        '''

        self.logger.debug('event on host {}'.format(host.identifier))
        if self._condition(host, event, epoch):
            result = self._action(host, event, epoch)
            if not result:
                raise RuntimeError('action executed, but no result returned')

            return result

        return None

    def _condition(self, host, event, epoch) -> bool:
        '''
        Condition to be evaluated when a event is received

        Args:
        - host: the agent where the policy is hosted
        - event: event received by the agent
        - epoch: the moment when the event occurred
        '''
        return True

    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        '''
        Returns a tuple containing ActionType and the event or result

        Args:
        - host: the agent where the policy is hosted
        - event: event received by the agent
        - epoch: the moment when the event occurred
        '''
        return (ActionType.result, True)

    def __repr__(self):
        return f'{self.__class__.__name__}()'


class PeriodicPolicy(ReflexPolicy):

    def __init__(self, required_sensors: Optional[List[Sensor]] = None,
                 required_actuators: Optional[List[Actuator]] = None):
        self._period = None
        super().__init__(required_sensors, required_actuators)

    @property
    def period(self):
        if self._period is None:
            raise RuntimeError(f'Period not set in {str(self)}')
        return self._period

    @period.setter
    def period(self, period):
        self._period = period

    def _condition(self, host, event, epoch) -> bool:
        '''Condition to be evaluated when a periodic event is received

        Args:
        - host: the agent where the policy is hosted
        - event: event received by the agent
        - epoch: the moment when the event occurred

        '''
        is_periodic = event.type == PayloadType.periodic_action
        return is_periodic and event.content == id(self)
