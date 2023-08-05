from typing import Dict, Optional

from arps.core.policy import (ReflexPolicy,
                              PeriodicPolicy)
from arps.core.remove_logger_files import remove_logger_files


class Environment:

    def __init__(self, sensors=None, actuators=None):
        '''
        Receives instances that will be used during application execution lifetime
        and need to be accessible by other classes

        Keyword parameters:
        - sensors : a dict containing sensor id and instance
        - actuators : a dict containing actuator id and instance

        See that sensors and actuator are global while policies will be created local required,
        that why sensor and actuator are instances while policies are just a class

        Raises:
        - TypeError if sensors or actuators are not a dict instance
        '''
        sensors = sensors or {}
        actuators = actuators or {}

        if not isinstance(sensors, dict):
            raise TypeError(
                'Wrong parameter type on sensors: {}'.format(sensors))

        if not isinstance(actuators, dict):
            raise TypeError(
                'Wrong parameter type on actuators: {}'.format(actuators))

        self._sensors = sensors
        self._actuators = actuators
        self._registered_policies: Dict[str, ReflexPolicy] = {}

    @property
    def sensors(self):
        return self._sensors

    @property
    def actuators(self):
        return self._actuators

    def sensor(self, sensor_id):
        '''
        Return sensor global instance based on id

        Parameters:
        - sensor_id : sensor identifier

        Raises KeyError when an invalid sensor id is supplied
        '''
        return self._sensors[sensor_id]

    def actuator(self, actuator_id):
        '''
        Return actuator instance based on id

        Parameters:
        - actuator_id : actuator identifier

        Raises KeyError when an invalid actuator id is supplied
        '''
        return self._actuators[actuator_id]

    # Resources
    def resources(self):
        '''
        Return a dictionary containing touchpoint category as key and touchpoint resource as value
        '''
        sensors_resources = {
            sensor_category: sensor.resource for sensor_category,
            sensor in self._sensors.items()}
        actuators_resources = {
            actuator_category: actuator.resource for actuator_category,
            actuator in self._actuators.items()}

        return {**sensors_resources, **actuators_resources}


    # Policy
    def list_registered_policies(self):
        '''
        List registered policies

        '''
        return list(self._registered_policies.keys())


    def register_policy(self, policy_id: str, policy_class: ReflexPolicy):
        '''
        Register policy class to be available globally

        Args:
        - policy_id : policy unique identification
        - policy_class : policy class
        '''
        self._registered_policies[policy_id] = policy_class


    def unregister_policy(self, policy_id: str):
        '''
        Removes policy class from the policy repository

        Args:
        - policy_id : policy unique identification
        '''

        del self._registered_policies[policy_id]


    def load_policy(self, policy_id: str, period: Optional[int] = None) -> ReflexPolicy:
        '''
        Returns a new instance of policy associated with policy id

        Args:
        - policy_id : policy unique identification
        - period: for periodic policies

        Raises:
        - ValueError when no policy in agent_manager is found, or no
        period is provided when using periodic policy
        '''
        try:
            policy_instance = self._registered_policies[policy_id]()
        except KeyError:
            raise ValueError(f'Policy {policy_id} not registered')

        valid_period = isinstance(period, int) and period > 0
        if isinstance(policy_instance, PeriodicPolicy) and not valid_period:
            remove_logger_files(policy_instance.logger)
            raise ValueError(f'Expected positive int period when creating periodic policy {policy_id}')

        if not isinstance(policy_instance, PeriodicPolicy) and period is not None:
            remove_logger_files(policy_instance.logger)
            raise ValueError(f'Trying to use period with a non periodic policy {policy_id}')

        if isinstance(policy_instance, PeriodicPolicy):
            policy_instance.period = period

        return policy_instance

    def is_policy_registered(self, policy_id: str) -> bool:
        '''
        Returns True if policy was previously registered, False otherwise

        Args:
        - policy_id : policy identifier
        '''
        return policy_id in self._registered_policies
