"""This module contains the public api of the EasyAgents reinforcement learning library.

    It consist mainly of the class hierarchy of the available agents (algorithms), registrations and
    the management of the available backends. In their implementation the agents forward their calls
    to the chosen backend.
"""

from abc import ABC
from typing import Dict, List, Tuple, Optional, Union
from easyagents import core
from easyagents.callbacks import plot
from easyagents.backends import core as bcore
import easyagents.backends.default
import easyagents.backends.tfagents
import easyagents.backends.hk

_backends: Dict[str, bcore.BackendAgentFactory] = {
    easyagents.backends.default.BackendAgentFactory.name: easyagents.backends.default.BackendAgentFactory(),
    easyagents.backends.tfagents.BackendAgentFactory.name: easyagents.backends.tfagents.BackendAgentFactory(),
    easyagents.backends.hk.BackendAgentFactory.name: easyagents.backends.hk.BackendAgentFactory()
}


def get_backends():
    """returns a list of all registered backend identifiers."""
    return _backends.keys()


def register_backend(backend_name: str, backend: bcore.BackendAgentFactory):
    assert backend_name is not None, "backend_name not set"
    assert backend_name, "backend_name is empty"
    assert backend is not None, "backend not set"
    _backends[backend_name] = backend


class EasyAgent(ABC):
    """Abstract base class for all easy reinforcment learning agents.

        Implementations must set _backend_agent and _agent_config.

        Args:
            backend_name: the backend (implementation) to be used, if None the a default implementation is used
    """

    def __init__(self,
                 gym_env_name: str = None,
                 fc_layers: Tuple[int, ...] = None,
                 model_config: core.ModelConfig = None,
                 backend_name: str = None):

        if model_config is None:
            model_config = core.ModelConfig(gym_env_name=gym_env_name, fc_layers=fc_layers)
        if backend_name is None:
            backend_name = easyagents.backends.default.BackendAgentFactory.name

        assert model_config is not None, "model_config not set."
        assert backend_name in get_backends(), \
            f'{backend_name} is not admissible. The registered backends are {get_backends()}.'

        self._model_config: core.ModelConfig = model_config
        self._backend_agent_factory: bcore.BackendAgentFactory = _backends[backend_name]
        self._backend_agent: Optional[bcore._BackendAgent] = None
        return

    def _prepare_callbacks(self, callbacks: List[core.AgentCallback],
                           default_plots: Optional[bool],
                           default_plot_callbacks: List[plot._PlotCallback],
                           ) -> List[core.AgentCallback]:
        """Adds the default callbacks and sorts all callbacks in the order
            _PreProcessCallbacks, AgentCallbacks, _PostProcessCallbacks.

        Args:
            callbacks: existing callbacks to prepare
            default_plots: if set or if None and callbacks does not contain plots then the default plots are added
            default_plot_callbacks: plot callbacks to add.
        """
        pre_process: List[core.AgentCallback] = [plot._PreProcess()]
        agent: List[core.AgentCallback] = []
        post_process: List[core.AgentCallback] = [plot._PostProcess()]

        if default_plots is None:
            default_plots = True
            for c in callbacks:
                default_plots = default_plots and (not isinstance(c, plot._PlotCallback))
        if default_plots:
            agent = default_plot_callbacks

        for c in callbacks:
            if isinstance(c, core._PreProcessCallback):
                pre_process.append(c)
            else:
                if isinstance(c, core._PostProcessCallback):
                    post_process.append(c)
                else:
                    agent.append(c)
        result: List[core.AgentCallback] = pre_process + agent + post_process
        return result

    def play(self, play_context: core.PlayContext,
             callbacks: Union[List[core.AgentCallback], core.AgentCallback, None],
             default_plots: Optional[bool]):
        """Plays episodes with the current policy according to play_context.

        Hints:
        o updates rewards in play_context

        Args:
            play_context: specifies the num of episodes to play
            callbacks: list of callbacks called during the play of the episodes
            default_plots: if set adds a set of default callbacks (plot.State, plot.Rewards, plot.Loss,...).
                if None default callbacks are only added if the callbacks list is empty

        Returns:
            play_context containg the actions taken and the rewards received during training
        """
        assert play_context, "play_context not set."
        if callbacks is None:
            callbacks = []
        if not isinstance(callbacks, list):
            assert isinstance(callbacks, core.AgentCallback), "callback not an AgentCallback or a list thereof."
            callbacks = [callbacks]
        callbacks = self._prepare_callbacks(callbacks, default_plots, [plot.Steps(), plot.Rewards()])
        self._backend_agent.play(play_context=play_context, callbacks=callbacks)
        return play_context

    def train(self, train_context: core.TrainContext,
              callbacks: Union[List[core.AgentCallback], core.AgentCallback, None],
              default_plots: Optional[bool]):
        """Trains a new model using the gym environment passed during instantiation.

        Args:
            callbacks: list of callbacks called during the training and evaluation
            train_context: training configuration to be used (num_iterations,num_episodes_per_iteration,...)
            default_plots: if set adds a set of default callbacks (plot.State, plot.Rewards, plot.Loss,...).
                if None default callbacks are only added if the callbacks list is empty
        """
        assert train_context, "train_context not set."
        if callbacks is None:
            callbacks = []
        if not isinstance(callbacks, list):
            assert isinstance(callbacks, core.AgentCallback), "callback not a AgentCallback or a list thereof."
            callbacks = [callbacks]
        callbacks = self._prepare_callbacks(callbacks, default_plots, [plot.Loss(), plot.Steps(), plot.Rewards()])
        self._backend_agent.train(train_context=train_context, callbacks=callbacks)


class DqnAgent(EasyAgent):
    """creates a new agent based on the Dqn algorithm.

    From wikipedia:
    The DeepMind system used a deep convolutional neural network, with layers of tiled convolutional filters to mimic
    the effects of receptive fields. Reinforcement learning is unstable or divergent when a nonlinear function
    approximator such as a neural network is used to represent Q.
    This instability comes from the correlations present in the sequence of observations, the fact that small updates
    to Q may significantly change the policy and the data distribution, and the correlations between Q and the
    target values.

    The technique used experience replay, a biologically inspired mechanism that uses a random sample of prior actions
    instead of the most recent action to proceed.[2] This removes correlations in the observation sequence and smooths
    changes in the data distribution. Iterative update adjusts Q towards target values that are only periodically
    updated, further reducing correlations with the target.[17]

    see also: https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning

    Args:
        gym_env_name: name of an OpenAI gym environment to be used for training and evaluation
        fc_layers: defines the neural network to be used, a sequence of fully connected
            layers of the given size. Eg (75,40) yields a neural network consisting
            out of 2 hidden layers, the first one containing 75 and the second layer
            containing 40 neurons.
        backend=the backend to be used (eg 'tfagents'), if None a default implementation is used.
            call get_backends() to get a list of the available backends.
    """

    def __init__(self,
                 gym_env_name: str,
                 fc_layers: Optional[Tuple[int, ...]] = None,
                 backend: str = None):
        super().__init__(gym_env_name=gym_env_name, fc_layers=fc_layers, backend_name=backend)
        self._backend_agent = self._backend_agent_factory.create_dqn_agent(self._model_config)
        return

    def play(self,
             callbacks: Union[List[core.AgentCallback], core.AgentCallback, None] = None,
             num_episodes: int = 1,
             max_steps_per_episode: int = 1000,
             play_context: core.PlayContext = None,
             default_plots: bool = None):
        """Plays num_episodes with the current policy.

        Args:
            callbacks: list of callbacks called during each episode play
            num_episodes: number of episodes to play
            max_steps_per_episode: max steps per episode
            play_context: play configuration to be used. If set override all other play context arguments
            default_plots: if set addes a set of default callbacks (plot.State, plot.Rewards, ...)

        Returns:
            play_context containg the actions taken and the rewards received during training
        """
        if play_context is None:
            play_context = core.PlayContext()
            play_context.max_steps_per_episode = max_steps_per_episode
            play_context.num_episodes = num_episodes
        super().play(play_context=play_context, callbacks=callbacks, default_plots=default_plots)
        return play_context

    def train(self,
              callbacks: Union[List[core.AgentCallback], core.AgentCallback, None] = None,
              num_iterations: int = 20000,
              max_steps_per_episode: int = 500,
              num_steps_per_iteration: int = 1,
              num_steps_buffer_preload=1000,
              num_steps_sampled_from_buffer=64,
              num_iterations_between_log=200,
              num_iterations_between_eval: int = 1000,
              num_episodes_per_eval: int = 10,
              learning_rate: float = 0.001,
              train_context: core.DqnTrainContext = None,
              default_plots: bool = None):
        """Trains a new model using the gym environment passed during instantiation.

        Args:
            callbacks: list of callbacks called during training and evaluation
            num_iterations: number of times the training is repeated (with additional data)
            max_steps_per_episode: maximum number of steps per episode
            num_steps_per_iteration: number of steps played per training iteration
            num_steps_buffer_preload: number of initial collect steps to preload the buffer
            num_steps_sampled_from_buffer: the number of steps sampled from buffer for each iteration training
            num_iterations_between_log: number of training iterations before an iteration based log / plot is updated.
            num_iterations_between_eval: number of training iterations before the current policy is evaluated.
                if 0 no evaluation is performed.
            num_episodes_per_eval: number of episodes played to estimate the average return and steps
            learning_rate: the learning rate used in the next iteration's policy training (0,1]
            train_context: training configuration to be used. if set overrides all other training context arguments.
            default_plots: if set adds a set of default callbacks (plot.State, plot.Rewards, plot.Loss,...).
                if None default callbacks are only added if the callbacks list is empty

        Returns:
            train_context: the training configuration containing the loss and sum of rewards encountered
                during training
        """
        if train_context is None:
            train_context = core.DqnTrainContext()
            train_context.num_iterations = num_iterations
            train_context.max_steps_per_episode = max_steps_per_episode
            train_context.num_steps_per_iteration = num_steps_per_iteration
            train_context.num_steps_buffer_preload = num_steps_buffer_preload
            train_context.num_steps_sampled_from_buffer = num_steps_sampled_from_buffer
            train_context.num_iterations_between_log = num_iterations_between_log
            train_context.num_iterations_between_eval = num_iterations_between_eval
            train_context.num_episodes_per_eval = num_episodes_per_eval
            train_context.learning_rate = learning_rate

        super().train(train_context=train_context, callbacks=callbacks, default_plots=default_plots)
        return train_context


class PpoAgent(EasyAgent):
    """creates a new agent based on the PPO algorithm.

        PPO is an actor-critic algorithm using 2 neural networks. The actor network
        to predict the next action to be taken and the critic network to estimate
        the value of the game state we are currently in (the expected, discounted
        sum of future rewards when following the current actor network).

        see also: https://spinningup.openai.com/en/latest/algorithms/ppo.html

        Args:
            gym_env_name: name of an OpenAI gym environment to be used for training and evaluation
            fc_layers: defines the neural network to be used, a sequence of fully connected
                layers of the given size. Eg (75,40) yields a neural network consisting
                out of 2 hidden layers, the first one containing 75 and the second layer
                containing 40 neurons.
            backend=the backend to be used (eg 'tfagents'), if None a default implementation is used.
                call get_backends() to get a list of the available backends.
    """

    def __init__(self,
                 gym_env_name: str,
                 fc_layers: Optional[Tuple[int, ...]] = None,

                 backend: str = None):
        super().__init__(gym_env_name=gym_env_name, fc_layers=fc_layers, backend_name=backend)
        self._backend_agent = self._backend_agent_factory.create_ppo_agent(self._model_config)
        return

    def play(self,
             callbacks: Union[List[core.AgentCallback], core.AgentCallback, None] = None,
             num_episodes: int = 1,
             max_steps_per_episode: int = 1000,
             play_context: core.PlayContext = None,
             default_plots: bool = None):
        """Plays num_episodes with the current policy.

        Args:
            callbacks: list of callbacks called during each episode play
            num_episodes: number of episodes to play
            max_steps_per_episode: max steps per episode
            play_context: play configuration to be used. If set override all other play context arguments
            default_plots: if set adds a set of default callbacks (plot.State, plot.Rewards, ...).
                if None default callbacks are only added if the callbacks list is empty

        Returns:
            play_context containg the actions taken and the rewards received during training
        """
        if play_context is None:
            play_context = core.PlayContext()
            play_context.max_steps_per_episode = max_steps_per_episode
            play_context.num_episodes = num_episodes
        super().play(play_context=play_context, callbacks=callbacks, default_plots=default_plots)
        return play_context

    def train(self,
              callbacks: Union[List[core.AgentCallback], core.AgentCallback, None] = None,
              num_iterations: int = 100,
              num_episodes_per_iteration: int = 10,
              max_steps_per_episode: int = 500,
              num_epochs_per_iteration: int = 10,
              num_iterations_between_eval: int = 5,
              num_episodes_per_eval: int = 10,
              learning_rate: float = 0.001,
              train_context: core.ActorCriticTrainContext = None,
              default_plots: bool = None):
        """Trains a new model using the gym environment passed during instantiation.

        Args:
            callbacks: list of callbacks called during training and evaluation
            num_iterations: number of times the training is repeated (with additional data)
            num_episodes_per_iteration: number of episodes played per training iteration
            max_steps_per_episode: maximum number of steps per episode
            num_epochs_per_iteration: number of times the data collected for the current iteration
                is used to retrain the current policy
            num_iterations_between_eval: number of training iterations before the current policy is evaluated.
                if 0 no evaluation is performed.
            num_episodes_per_eval: number of episodes played to estimate the average return and steps
            learning_rate: the learning rate used in the next iteration's policy training (0,1]
            train_context: training configuration to be used. if set overrides all other training context arguments.
            default_plots: if set adds a set of default callbacks (plot.State, plot.Rewards, plot.Loss,...).
                if None default callbacks are only added if the callbacks list is empty

        Returns:
            train_context: the training configuration containing the loss and sum of rewards encountered
                during training
        """
        if train_context is None:
            train_context = core.ActorCriticTrainContext()
            train_context.num_iterations = num_iterations
            train_context.num_episodes_per_iteration = num_episodes_per_iteration
            train_context.max_steps_per_episode = max_steps_per_episode
            train_context.num_epochs_per_iteration = num_epochs_per_iteration
            train_context.num_iterations_between_eval = num_iterations_between_eval
            train_context.num_episodes_per_eval = num_episodes_per_eval
            train_context.learning_rate = learning_rate

        super().train(train_context=train_context, callbacks=callbacks, default_plots=default_plots)
        return train_context


class RandomAgent(EasyAgent):
    """creates a new agent which always chooses uniform random actions.

        Args:
            gym_env_name: name of an OpenAI gym environment to be used for training and evaluation
            backend=the backend to be used (eg 'tfagents'), if None a default implementation is used.
                call get_backends() to get a list of the available backends.

        Returns:
            play_context containg the actions taken and the rewards received during training
    """

    def __init__(self, gym_env_name: str, backend: str = None):
        super().__init__(gym_env_name=gym_env_name, fc_layers=None, backend_name=backend)
        self._backend_agent = self._backend_agent_factory.create_random_agent(self._model_config)
        return

    def play(self,
             callbacks: Union[List[core.AgentCallback], core.AgentCallback, None] = None,
             num_episodes: int = 1,
             max_steps_per_episode: int = 1000,
             play_context: core.PlayContext = None,
             default_plots: bool = None):
        """Plays num_episodes with the current policy.

        Args:
            callbacks: list of callbacks called during each episode play
            num_episodes: number of episodes to play
            max_steps_per_episode: max steps per episode
            play_context: play configuration to be used. If set override all other play context arguments
            default_plots: if set adds a set of default callbacks (plot.State, plot.Rewards, ...).
                if None default callbacks are only added if the callbacks list is empty
        """
        if play_context is None:
            play_context = core.PlayContext()
            play_context.max_steps_per_episode = max_steps_per_episode
            play_context.num_episodes = num_episodes
        super().play(play_context=play_context, callbacks=callbacks, default_plots=default_plots)
        return play_context

    def train(self,
              callbacks: Union[List[core.AgentCallback], core.AgentCallback, None] = None,
              num_iterations: int = 10,
              max_steps_per_episode: int = 1000,
              num_episodes_per_eval: int = 10,
              train_context: core.ActorCriticTrainContext = None,
              default_plots: bool = None):
        """Evaluates the environment using a uniform random policy.

        The evaluation is performed in batches of num_episodes_per_eval episodes.

        Args:
            callbacks: list of callbacks called during training and evaluation
            num_iterations: number of times a batch of num_episodes_per_eval episodes is evaluated.
            max_steps_per_episode: maximum number of steps per episode
            num_episodes_per_eval: number of episodes played to estimate the average return and steps
            train_context: training configuration to be used. if set overrides all other training context arguments.
            default_plots: if set adds a set of default callbacks (plot.State, plot.Rewards, plot.Loss,...)

        Returns:
            train_context: the training configuration containing the loss and sum of rewards encountered
                during training
        """
        if train_context is None:
            train_context = core.TrainContext()
            train_context.num_iterations = num_iterations
            train_context.max_steps_per_episode = max_steps_per_episode
            train_context.num_epochs_per_iteration = 0
            train_context.num_episodes_per_iteration = 1
            train_context.num_iterations_between_eval = 1
            train_context.num_episodes_per_eval = num_episodes_per_eval
            train_context.learning_rate = 1

        super().train(train_context=train_context, callbacks=callbacks, default_plots=default_plots)
        return train_context



class ReinforceAgent(EasyAgent):
    """creates a new agent based on the Reinforce algorithm.

        Reinforce is a vanilla policy gradient algorithm using a single actor network.

        see also: www-anw.cs.umass.edu/~barto/courses/cs687/williams92simple.pdf

        Args:
            gym_env_name: name of an OpenAI gym environment to be used for training and evaluation
            fc_layers: defines the neural network to be used, a sequence of fully connected
                layers of the given size. Eg (75,40) yields a neural network consisting
                out of 2 hidden layers, the first one containing 75 and the second layer
                containing 40 neurons.
            backend=the backend to be used (eg 'tfagents'), if None a default implementation is used.
                call get_backends() to get a list of the available backends.
    """

    def __init__(self,
                 gym_env_name: str,
                 fc_layers: Optional[Tuple[int, ...]] = None,

                 backend: str = None):
        super().__init__(gym_env_name=gym_env_name, fc_layers=fc_layers, backend_name=backend)
        self._backend_agent = self._backend_agent_factory.create_reinforce_agent(self._model_config)
        return

    def play(self,
             callbacks: Union[List[core.AgentCallback], core.AgentCallback, None] = None,
             num_episodes: int = 1,
             max_steps_per_episode: int = 1000,
             play_context: core.PlayContext = None,
             default_plots: bool = None):
        """Plays num_episodes with the current policy.

        Args:
            callbacks: list of callbacks called during each episode play
            num_episodes: number of episodes to play
            max_steps_per_episode: max steps per episode
            play_context: play configuration to be used. If set override all other play context arguments
            default_plots: if set adds a set of default callbacks (plot.State, plot.Rewards, ...).
                if None default callbacks are only added if the callbacks list is empty

        Returns:
            play_context containg the actions taken and the rewards received during training
        """
        if play_context is None:
            play_context = core.PlayContext()
            play_context.max_steps_per_episode = max_steps_per_episode
            play_context.num_episodes = num_episodes
        super().play(play_context=play_context, callbacks=callbacks, default_plots=default_plots)
        return play_context

    def train(self,
              callbacks: Union[List[core.AgentCallback], core.AgentCallback, None] = None,
              num_iterations: int = 100,
              num_episodes_per_iteration: int = 10,
              max_steps_per_episode: int = 500,
              num_epochs_per_iteration: int = 10,
              num_iterations_between_eval: int = 5,
              num_episodes_per_eval: int = 10,
              learning_rate: float = 0.001,
              train_context: core.EpisodesTrainContext = None,
              default_plots: bool = None):
        """Trains a new model using the gym environment passed during instantiation.

        Args:
            callbacks: list of callbacks called during training and evaluation
            num_iterations: number of times the training is repeated (with additional data)
            num_episodes_per_iteration: number of episodes played per training iteration
            max_steps_per_episode: maximum number of steps per episode
            num_epochs_per_iteration: number of times the data collected for the current iteration
                is used to retrain the current policy
            num_iterations_between_eval: number of training iterations before the current policy is evaluated.
                if 0 no evaluation is performed.
            num_episodes_per_eval: number of episodes played to estimate the average return and steps
            learning_rate: the learning rate used in the next iteration's policy training (0,1]
            train_context: training configuration to be used. if set overrides all other training context arguments.
            default_plots: if set adds a set of default callbacks (plot.State, plot.Rewards, plot.Loss,...).
                if None default callbacks are only added if the callbacks list is empty

        Returns:
            train_context: the training configuration containing the loss and sum of rewards encountered
                during training
        """
        if train_context is None:
            train_context = core.EpisodesTrainContext()
            train_context.num_iterations = num_iterations
            train_context.num_episodes_per_iteration = num_episodes_per_iteration
            train_context.max_steps_per_episode = max_steps_per_episode
            train_context.num_epochs_per_iteration = num_epochs_per_iteration
            train_context.num_iterations_between_eval = num_iterations_between_eval
            train_context.num_episodes_per_eval = num_episodes_per_eval
            train_context.learning_rate = learning_rate

        super().train(train_context=train_context, callbacks=callbacks, default_plots=default_plots)
        return train_context
