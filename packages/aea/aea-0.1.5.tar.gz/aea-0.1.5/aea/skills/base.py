# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the base classes for the skills."""

import importlib.util
import inspect
import logging
import os
import re
import sys
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, cast

from aea.configurations.base import BehaviourConfig, HandlerConfig, TaskConfig, SkillConfig, ProtocolId, DEFAULT_SKILL_CONFIG_FILE
from aea.configurations.loader import ConfigLoader
from aea.mail.base import OutBox, Envelope

logger = logging.getLogger(__name__)


class AgentContext:
    """Save relevant data for the agent."""

    def __init__(self, agent_name: str, public_key: str, outbox: OutBox):
        """
        Initialize a skill context.

        :param agent_name: the agent's name
        :param outbox: the outbox
        """
        self._agent_name = agent_name
        self._public_key = public_key
        self._outbox = outbox
        self.skill_loader = ConfigLoader("skill-config_schema.json", SkillConfig)

    @property
    def agent_name(self) -> str:
        """Get agent name."""
        return self._agent_name

    @property
    def public_key(self) -> str:
        """Get public key."""
        return self._public_key

    @property
    def outbox(self) -> OutBox:
        """Get outbox."""
        return self._outbox


class SkillContext:
    """This class implements the context of a skill."""

    def __init__(self, agent_context: AgentContext):
        """
        Initialize a skill context.

        :param agent_context: the agent's context
        """
        self._agent_context = agent_context
        self._skill = None  # type: Optional[Skill]

    @property
    def agent_name(self) -> str:
        """Get agent name."""
        return self._agent_context.agent_name

    @property
    def agent_public_key(self) -> str:
        """Get public key."""
        return self._agent_context.public_key

    @property
    def outbox(self) -> OutBox:
        """Get outbox."""
        return self._agent_context.outbox

    @property
    def handler(self) -> Optional['Handler']:
        """Get handler of the skill."""
        assert self._skill is not None, "Skill not initialized."
        return self._skill.handler

    @property
    def behaviours(self) -> Optional[List['Behaviour']]:
        """Get behaviours of the skill."""
        assert self._skill is not None, "Skill not initialized."
        return self._skill.behaviours

    @property
    def tasks(self) -> Optional[List['Task']]:
        """Get tasks of the skill."""
        assert self._skill is not None, "Skill not initialized."
        return self._skill.tasks


class Behaviour(ABC):
    """This class implements an abstract behaviour."""

    def __init__(self, **kwargs):
        """
        Initialize a behaviour.

        :param skill_context: the skill context
        :param kwargs: keyword arguments
        """
        self._context = kwargs.pop('skill_context')  # type: SkillContext
        self._config = kwargs

    @property
    def context(self) -> SkillContext:
        """Get the context of the behaviour."""
        return self._context

    @property
    def config(self) -> Dict[Any, Any]:
        """Get the config of the behaviour."""
        return self._config

    @abstractmethod
    def act(self) -> None:
        """
        Implement the behaviour.

        :return: None
        """

    @abstractmethod
    def teardown(self) -> None:
        """
        Implement the behaviour teardown.

        :return: None
        """

    @classmethod
    def parse_module(cls, path: str, behaviours_configs: List[BehaviourConfig], skill_context: SkillContext) -> List['Behaviour']:
        """
        Parse the behaviours module.

        :param path: path to the Python module containing the Behaviour classes.
        :param behaviours_configs: a list of behaviour configurations.
        :param skill_context: the skill context
        :return: a list of Behaviour.
        """
        behaviours = []
        behaviours_spec = importlib.util.spec_from_file_location("behaviours", location=path)
        behaviour_module = importlib.util.module_from_spec(behaviours_spec)
        behaviours_spec.loader.exec_module(behaviour_module)  # type: ignore
        classes = inspect.getmembers(behaviour_module, inspect.isclass)
        behaviours_classes = list(filter(lambda x: re.match("\\w+Behaviour", x[0]), classes))

        name_to_class = dict(behaviours_classes)
        for behaviour_config in behaviours_configs:
            behaviour_class_name = cast(str, behaviour_config.class_name)
            logger.debug("Processing behaviour {}".format(behaviour_class_name))
            behaviour_class = name_to_class.get(behaviour_class_name, None)
            if behaviour_class is None:
                logger.warning("Behaviour '{}' cannot be found.".format(behaviour_class))
            else:
                args = behaviour_config.args
                assert 'skill_context' not in args.keys(), "'skill_context' is a reserved key. Please rename your arguments!"
                args['skill_context'] = skill_context
                behaviour = behaviour_class(**args)
                behaviours.append(behaviour)

        return behaviours


class Handler(ABC):
    """This class implements an abstract behaviour."""

    SUPPORTED_PROTOCOL = None  # type: Optional[ProtocolId]

    def __init__(self, **kwargs):
        """
        Initialize a handler object.

        :param skill_context: the skill context
        :param kwargs: keyword arguments
        """
        self._context = kwargs.pop('skill_context')  # type: SkillContext
        self._config = kwargs

    @property
    def context(self) -> SkillContext:
        """Get the context of the handler."""
        return self._context

    @property
    def config(self) -> Dict[Any, Any]:
        """Get the config of the handler."""
        return self._config

    @abstractmethod
    def handle_envelope(self, envelope: Envelope) -> None:
        """
        Implement the reaction to an envelope.

        :param envelope: the envelope
        :return: None
        """

    @abstractmethod
    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """

    @classmethod
    def parse_module(cls, path: str, handler_config: HandlerConfig, skill_context: SkillContext) -> Optional['Handler']:
        """
        Parse the handler module.

        :param path: path to the Python module containing the Handler class.
        :param handler_config: the handler configuration.
        :param skill_context: the skill context
        :return: an handler, or None if the parsing fails.
        """
        handler_spec = importlib.util.spec_from_file_location("handler", location=path)
        handler_module = importlib.util.module_from_spec(handler_spec)
        handler_spec.loader.exec_module(handler_module)  # type: ignore
        classes = inspect.getmembers(handler_module, inspect.isclass)
        handler_classes = list(filter(lambda x: re.match("\\w+Handler", x[0]), classes))

        name_to_class = dict(handler_classes)
        handler_class_name = cast(str, handler_config.class_name)
        logger.debug("Processing handler {}".format(handler_class_name))
        handler_class = name_to_class.get(handler_class_name, None)
        if handler_class is None:
            logger.warning("Handler '{}' cannot be found.".format(handler_class_name))
            return None
        else:
            args = handler_config.args
            assert 'skill_context' not in args.keys(), "'skill_context' is a reserved key. Please rename your arguments!"
            args['skill_context'] = skill_context
            handler = handler_class(**args)
            return handler


class Task(ABC):
    """This class implements an abstract task."""

    def __init__(self, *args, **kwargs):
        """
        Initialize a task.

        :param skill_context: the skill context
        :param kwargs: keyword arguments.
        """
        self._context = kwargs.pop('skill_context')  # type: SkillContext
        self._config = kwargs

    @property
    def context(self) -> SkillContext:
        """Get the context of the task."""
        return self._context

    @property
    def config(self) -> Dict[Any, Any]:
        """Get the config of the task."""
        return self._config

    @abstractmethod
    def execute(self) -> None:
        """
        Run the task logic.

        :return: None
        """

    @abstractmethod
    def teardown(self) -> None:
        """
        Teardown the task.

        :return: None
        """

    @classmethod
    def parse_module(cls, path: str, tasks_configs: List[TaskConfig], skill_context: SkillContext) -> List['Task']:
        """
        Parse the tasks module.

        :param path: path to the Python module containing the Task classes.
        :param tasks_configs: a list of tasks configurations.
        :param skill_context: the skill context
        :return: a list of Tasks.
        """
        tasks = []
        tasks_spec = importlib.util.spec_from_file_location("tasks", location=path)
        task_module = importlib.util.module_from_spec(tasks_spec)
        tasks_spec.loader.exec_module(task_module)  # type: ignore
        classes = inspect.getmembers(task_module, inspect.isclass)
        tasks_classes = list(filter(lambda x: re.match("\\w+Task", x[0]), classes))

        name_to_class = dict(tasks_classes)
        for task_config in tasks_configs:
            task_class_name = task_config.class_name
            logger.debug("Processing task {}".format(task_class_name))
            task_class = name_to_class.get(task_class_name, None)
            if task_class is None:
                logger.warning("Task '{}' cannot be found.".format(task_class))
            else:
                args = task_config.args
                assert 'skill_context' not in args.keys(), "'skill_context' is a reserved key. Please rename your arguments!"
                args['skill_context'] = skill_context
                task = task_class(**args)
                tasks.append(task)

        return tasks


class Skill:
    """This class implements a skill."""

    def __init__(self, config: SkillConfig,
                 skill_context: SkillContext,
                 handler: Optional[Handler],
                 behaviours: Optional[List[Behaviour]],
                 tasks: Optional[List[Task]]):
        """
        Initialize a skill.

        :param config: the skill configuration.
        :param handler: the handler to handle incoming envelopes.
        :param behaviours: the list of behaviours that defines the proactive component of the agent.
        :param tasks: the list of tasks executed at every iteration of the main loop.
        """
        self.config = config
        self.skill_context = skill_context
        self.handler = handler
        self.behaviours = behaviours
        self.tasks = tasks

    @classmethod
    def from_dir(cls, directory: str, agent_context: AgentContext) -> Optional['Skill']:
        """
        Load a skill from a directory.

        :param directory: the skill
        :param agent_context: the agent's context
        :return: the Skill object. None if the parsing failed.
        """
        # check if there is the config file. If not, then return None.
        skill_config = agent_context.skill_loader.load(open(os.path.join(directory, DEFAULT_SKILL_CONFIG_FILE)))
        if skill_config is None:
            return None

        skills_spec = importlib.util.spec_from_file_location(skill_config.name, os.path.join(directory, "__init__.py"))
        if skills_spec is None:
            logger.warning("No skill found.")
            return None

        skill_module = importlib.util.module_from_spec(skills_spec)
        sys.modules[skills_spec.name + "_skill"] = skill_module
        skills_packages = list(filter(lambda x: not x.startswith("__"), skills_spec.loader.contents()))  # type: ignore
        logger.debug("Processing the following skill package: {}".format(skills_packages))

        skill_context = SkillContext(agent_context)

        handler = Handler.parse_module(os.path.join(directory, "handler.py"), skill_config.handler, skill_context)
        behaviours_configurations = list(dict(skill_config.behaviours.read_all()).values())
        behaviours = Behaviour.parse_module(os.path.join(directory, "behaviours.py"), behaviours_configurations, skill_context)
        tasks_configurations = list(dict(skill_config.tasks.read_all()).values())
        tasks = Task.parse_module(os.path.join(directory, "tasks.py"), tasks_configurations, skill_context)

        skill = Skill(skill_config, skill_context, handler, behaviours, tasks)
        skill_context._skill = skill

        return skill
