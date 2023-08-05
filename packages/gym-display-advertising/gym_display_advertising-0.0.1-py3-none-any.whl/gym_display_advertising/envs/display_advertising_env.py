import gym
import numpy as np
import pandas as pd


class DisplayAdvertising(gym.Env):
    """
    A simple display advertising environment using iPinYou data.

    In this form the goal is to provide realistic bid data but still keep the problem
    simple enough for simple RL algorithms to solve.

    The state of the environment is represented by the bidding only. No information
    about the user is return (e.g. the estimated ctr). Hence the optimal solution is to provide the best average bid. Although the actual bid is dynamic.
    """

    metadata = {"render.modes": [""]}

    def __init__(self, data: pd.DataFrame = None, initial_budget: float = 100.0):
        if data is None:
            data = get_test_data()
        self.campaign_data = data
        self.initial_bid = 100
        self.batch_size = 100
        self.initial_budget = initial_budget
        self.actions = np.array([-0.5, -0.1, -0.05, 0, 0.05, 0.1, 0.5])
        self.action_space = gym.spaces.Discrete(len(self.actions))
        self.clip_high = 1.0
        self.max_bid = 500
        self._file_ptr = 0
        self.reset()
        n_obs = len(self._get_observation())
        self.observation_space = gym.spaces.Box(
            0.0, self.clip_high, shape=(n_obs,), dtype=np.float32
        )

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (
            action,
            type(action),
        )

        # Perform bid
        self.bid *= 1 + self.actions[action]

        _, winning_bid = self.get_campaign_data()

        # Get reward
        reward = 0
        if self.bid > winning_bid and self.remaining_budget > self.bid:
            self.remaining_budget -= self.bid
            reward = 1

        self._counter += 1
        self._file_ptr += 1

        # Check if this is the end of the batch
        done = bool(self._counter >= self.batch_size)

        # Get next observation
        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        normalised_bid = self.bid / self.max_bid
        fractional_budget_remaining = self.remaining_budget / self.initial_budget
        fractional_time_left = (self.batch_size - self._counter) / self.batch_size
        return np.clip(
            [normalised_bid, fractional_budget_remaining, fractional_time_left],
            a_min=0,
            a_max=self.clip_high,
        )

    def reset(self):
        self.remaining_budget = self.initial_budget
        self._counter = 0
        self.bid = self.initial_bid + np.random.normal(0, 50)
        return self._get_observation()

    def render(self, mode="human"):
        pass

    def close(self):
        pass

    def get_campaign_data(self):
        index = self._file_ptr % len(self.campaign_data)
        winning_bid = self.campaign_data["winprice"].iloc[index]
        clicks = self.campaign_data["click"].iloc[index]
        return (clicks, winning_bid)


def get_test_data():
    import pathlib
    from gym_display_advertising.data import ProcessedIPinYouData

    current_directory = pathlib.Path(__file__).parent
    ipinyou = ProcessedIPinYouData(
        directory=current_directory / ".." / ".." / "data" / "processed_ipinyou"
    )
    training_data, _ = ipinyou.get_merchant_data(2997)
    return training_data
