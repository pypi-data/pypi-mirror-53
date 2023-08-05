import logging
import asyncio
import abc
from functools import wraps
from typing import Dict, Any, List, Union, Optional

from arps import __version__ as arps_version

from arps.core.agent_id_manager import AgentIDManager, AgentID
from arps.core.payload_factory import PayloadType


_AVAILABLE_COMMANDS = []

JSONType = Union[Dict[str, Any], str, int, List[Any]]


def _register_command(command_description):
    def _inner_regiser_command(command):
        '''Register function and first line of docstring to be listed as
        available command

        '''

        _AVAILABLE_COMMANDS.append('{:<30}: {}'.format(command.__name__,
                                                       command_description))

        @wraps(command)
        def inner(*args, **kwargs):
            return command(*args, **kwargs)
        return inner
    return _inner_regiser_command


class AgentManagerCreationError(Exception):
    '''This exception class is to capture any error related to the
    process of creating an Agent Manager

    '''


class AgentManagerRequestError(Exception):
    '''This exception class is to capture any error related to a
    AgentManager method call

    '''


class AgentManager(metaclass=abc.ABCMeta):
    '''Class responsible for manage agents.

    Coroutines here need to be used using an event loop.

    See integration tests for examples.

    '''

    def __init__(self, identifier):
        self.running_agents = {}
        self.identifier = identifier
        self.agent_id_manager = AgentIDManager(self.identifier)
        self.message_id = 0

        self.logger = logging.getLogger(self.__class__.__name__)

    def index(self) -> JSONType:
        return {'available_commands': _AVAILABLE_COMMANDS}

    @_register_command('Return information about the agent manager')
    def about(self) -> JSONType:
        '''Returns agent manager root ID with the current version

        '''

        return {'identifier': self.identifier, 'version': arps_version}

    @_register_command('Spawn agent according to the specified policies')
    @abc.abstractmethod
    async def spawn_agent(self, *, policies: Dict[str, Optional[int]]) -> JSONType:
        '''Creates an agent assinging to it the next unique ID

        Param:
        - policies: dictionary of policies and their periods (when required)

        Returns:
        - Message about agent creation status

        Raises:
        - AgentManagerRequestError when request has problems and agent
          couldn't be created

        '''

    @_register_command('List spawned agents')
    @abc.abstractmethod
    def list_agents(self) -> JSONType:
        '''
        List all the spawned agents ids
        '''

    @_register_command('Terminate agent manager')
    @abc.abstractmethod
    async def terminate_agent(self, *, agent_id: AgentID) -> JSONType:
        '''Remove the agent from the system. Its ID will be lost and will not be reused

        Param:
        - agent_id: unique agent id

        '''

    @_register_command('Add or remove relationship between agent')
    @abc.abstractmethod
    async def update_agents_relationship(self, *, from_agent: AgentID,
                                         to_agent: str,
                                         operation: str):
        '''Update agents relationship by create or removing the link between agents.

        It is unidirectional. If A has a relationship with B and B has
        a relationship with A, removing parenting from A to B will not
        remove pareting from B to A

        Param:
        - from_agent: agent that will be able to send a message to the
          other agent
        - to_agent: agent that will be able to receive a message from
          the other agent
        - operation: add or remove agent relationship
        '''

    @_register_command('Return information about agent(s) or the state of its monitored resources')
    async def agents_status(self,
                            request_type: PayloadType,
                            provider: AgentID) -> JSONType:
        '''Return the current status of agents

        Keyword args:
        - request_type: info, sensors, or actuators
        - provider: agent that will respond the request

        '''
        agents = self.list_agents()['agents']
        if not agents:
            self.logger.info(f'No agent is running')
            raise AgentManagerRequestError(f'No agent is running')

        if str(provider) not in agents:
            self.logger.info(f'Agent {provider} not found in {agents}')
            raise AgentManagerRequestError(f'Agent {provider} not found')

        return await self._agent_status(request_type, provider)

    def generate_message_id(self):
        self.message_id += 1
        return self.message_id

    @_register_command('Show available policies (local and remote)')
    @abc.abstractmethod
    async def policy_repository(self) -> JSONType:
        '''List available policies in the repository used to set agents' behaviour

        '''

    @_register_command('Show available touchpoints')
    @abc.abstractmethod
    async def loaded_touchpoints(self) -> JSONType:
        '''Returns loaded sensors and actuators

        '''

    @_register_command('Retrieve monitor log')
    async def monitor_logs(self) -> List[str]:
        '''Return path to the monitor logs containing states of the touchpoints

        '''
        monitor_providers = await self.filter_agents_with_monitor_policy()

        async def monitor_log_path(monitor_provider):
            awaitable_status = self.agents_status(request_type=PayloadType.action,
                                                  provider=monitor_provider)
            result = await asyncio.wait_for(awaitable_status, 10.0)
            return result.content.status

        monitor_logs_path = [await monitor_log_path(provider) for provider in monitor_providers]
        self.logger.info(f'Providers monitor logs: {monitor_logs_path}')

        return monitor_logs_path

    async def filter_agents_with_monitor_policy(self):
        def is_a_monitor_agent(policies):
            return any(policy.endswith('MonitorPolicy') for policy in policies)

        monitor_providers = list()
        for agent in self.list_agents()['agents']:
            awaitable_status = self.agents_status(request_type=PayloadType.info,
                                                  provider=AgentID.from_str(agent))
            result = await asyncio.wait_for(awaitable_status, 10.0)
            self.logger.debug(f'Info from agent {agent}: {result}')
            if is_a_monitor_agent(result.content.policies):
                monitor_providers.append(AgentID.from_str(result.sender_id))

        self.logger.info(f'Providers monitoring: {monitor_providers}')
        return monitor_providers

    @abc.abstractmethod
    def cleanup(self):
        '''Stop all agents that was created by the manager.

        Doesn't reset the identifiers.

        '''
