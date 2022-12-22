from easymaze import EasyMaze

env = EasyMaze()
obs = env.reset()

for _ in range(10):
    action = env.action_space.sample()
    obs, re, done, info = env.step(action)

    print(obs)

    if done:
        env.reset()