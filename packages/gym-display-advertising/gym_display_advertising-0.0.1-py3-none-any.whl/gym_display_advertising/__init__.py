from gym.envs.registration import register

register(
    id="DisplayAdvertising-v0",
    entry_point="gym_display_advertising.envs:DisplayAdvertising",
)

register(
    id="StaticDisplayAdvertising-v0",
    entry_point="gym_display_advertising.envs:StaticDisplayAdvertising",
)
