import gym
import gym_tag
from moviepy.editor import ImageSequenceClip

action_name = ["do_nothing", "left_forward", "right_forward", "forward"]


my_config = {
    "map": "mob_2_obstacle_map.txt",
    "env_type": "mob",
    "reward_type": "distance",
    "action type": "type2",
}

my_config = {
    "map": "goal_map.txt",
    "env_type": "goal",
    "reward_type": "distance",
    "action type": "type2",
}


def random_agent():
    all_states = []
    for i in range(1):

        env = gym.make("Tag-v0")
        env.set_config(my_config)
        for j in range(360):
            obs, rew, _, _ = env.step(3)
            all_states.append(obs)
            print(rew)

        clip = ImageSequenceClip(all_states, fps=60)
        clip.write_gif(action_name[i] + str(my_config["map"]) + ".gif", fps=60)
        all_states = []


if __name__ == "__main__":
    random_agent()
