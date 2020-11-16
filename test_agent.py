import gym
import gym_tag
import matplotlib.pyplot as plt
from array2gif import write_gif


def random_agent(episodes=10):

    all_states = []
    for i in range(10):
        env = gym.make("EE-v0")
        all_states.append(env.reset())

        write_gif(all_states,  str(i) + "staryt.gif", fps=1)
        all_states = []
        # env.close()

if __name__ == "__main__":
    random_agent()
