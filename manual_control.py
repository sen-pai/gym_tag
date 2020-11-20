import gym
import gym_tag
import matplotlib.pyplot as plt
# from moviepy.editor import ImageSequenceClip

action_name = ["do_nothing", "left_forward", "right_forward", "forward"]


# my_config = {"map": "goal_map.txt", "env_type": "goal", "reward_type": "distance", "action type": "type2"}

my_config = {"map": "mob_2_map.txt", "env_type": "mob", "reward_type": "distance", "action type": "type2"}


def manual_control():

    plt.ion()
    env = gym.make("Tag-v0")
    env.set_config(my_config)
    obs = env.reset()
    print("reset done")

    fig1, ax1 = plt.subplots()
    obs_screen = ax1.imshow(obs)

    done = False
    while not done:
        action = int(input())
        new_obs, rew, done, _ = env.step(action)
        print("reward", rew)
        obs_screen.set_data(new_obs)
        fig1.canvas.flush_events()

if __name__ == "__main__":
    manual_control()
