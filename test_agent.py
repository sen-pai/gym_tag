import gym
import gym_tag
from moviepy.editor import ImageSequenceClip

action_name = ["do_nothing", "left_forward", "right_forward", "forward"]
my_config = {"map": "2_mob_map.txt"}


def random_agent():
    all_states = []
    for i in range(4):

        env = gym.make("EE-v0")
        env.set_config(my_config)
        # env.reset()
        for j in range(60):
            obs, _, _, _ = env.step(i)
            all_states.append(obs)

        clip = ImageSequenceClip(all_states, fps=60)
        clip.write_gif(str(i) + action_name[i] + ".gif", fps=60)
        all_states = []


if __name__ == "__main__":
    random_agent()
