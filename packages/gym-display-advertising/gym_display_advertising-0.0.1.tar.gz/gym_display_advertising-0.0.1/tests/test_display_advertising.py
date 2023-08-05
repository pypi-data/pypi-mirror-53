import gym_display_advertising
from gym_display_advertising.data import ProcessedIPinYouData
import gym
import numpy as np
import pathlib


def test_registration():
    env = gym.make("DisplayAdvertising-v0")
    assert env != None


def test_correct_num_episodes():
    env = gym.make("DisplayAdvertising-v0")
    episode_over = False
    buffer = []
    while not episode_over:
        _, reward, episode_over, _ = env.step(env.action_space.sample())
        buffer.append(reward)
    assert hasattr(env, "batch_size")
    assert len(buffer) == env.batch_size


def test_state_is_not_empty():
    env = gym.make("DisplayAdvertising-v0")
    state, _, _, _ = env.step(env.action_space.sample())
    assert isinstance(state, np.ndarray)


def test_env_within_observation_space():
    env = gym.make("DisplayAdvertising-v0")
    assert hasattr(env, "observation_space")
    assert env.observation_space != None
    state, _, _, _ = env.step(env.action_space.sample())
    np.testing.assert_array_equal(env.observation_space.shape, state.shape)
    assert env.observation_space.contains(state)


def test_with_real_data():
    current_directory = pathlib.Path(__file__).parent
    ipinyou = ProcessedIPinYouData(
        directory=current_directory / ".." / "data" / "processed_ipinyou"
    )
    training_data, _ = ipinyou.get_merchant_data(2997)
    env = gym.make("DisplayAdvertising-v0", data=training_data)
    state, _, _, _ = env.step(env.action_space.sample())
    assert isinstance(state, np.ndarray)
