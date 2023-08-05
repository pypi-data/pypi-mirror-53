import gym
import numpy as np


class StaticDisplayAdvertising(gym.Env):
    """
    A test display advertising bidding environment where the winning bid and reward is fixed. The initial campaign budget fixed at 10,000 and there are 100 steps per episode. Hence, the optimal bid should be 100 for an optimal reward of 100. The winning bid is set to 99.99.
    The actions affect the current bid. The agent can either increase or decrease the bid.
    The observations are representations of the current state. They are normalised to be between 0 and 1.
    """

    metadata = {"render.modes": []}

    def __init__(self):
        self.initial_bid = 100
        self.batch_size = 100
        self.initial_budget = self.initial_bid * self.batch_size
        self.winning_bid = 99.99
        self.actions = np.array([-0.5, -0.1, -0.05, 0, 0.05, 0.1, 0.5])
        self.action_space = gym.spaces.Discrete(len(self.actions))
        self.clip_high = 1.0
        self.max_bid = 500
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

        # Get reward
        reward = 0
        if self.bid > self.winning_bid and self.remaining_budget > self.bid:
            self.remaining_budget -= self.bid
            reward = +1

        self._counter += 1

        # Check if this is the end of the batch
        done = bool(self._counter >= self.batch_size)

        return self._get_observation(), reward, done, {}

    def reset(self):
        self.remaining_budget = self.initial_budget
        self._counter = 0
        self.bid = self.initial_bid + np.random.normal(0, 50)
        return self._get_observation()

    def _get_observation(self):
        normalised_bid = self.bid / self.max_bid
        fractional_budget_remaining = self.remaining_budget / self.initial_budget
        fractional_time_left = (self.batch_size - self._counter) / self.batch_size

        return np.clip(
            [normalised_bid, fractional_budget_remaining, fractional_time_left],
            a_min=0,
            a_max=self.clip_high,
        )

    def render(self, mode="human"):
        pass

    def close(self):
        pass
