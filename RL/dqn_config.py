episodes = 6000
update_step = 80
save_step = 100
def save_path(e):
    return f"models/dqn_config01_episode{e}"


#env
matrix_dimension = 4
state_shape = (16,)
action_size = 4
action_space = ["up", "down", "left", "right"]

#config01
buffer_max_size = 50000
start_replay = 2000
buffer_batch_size = 64
epsilon_decay = 0.000001
epsilon_min = 0.01
dqn_gamma = 0.99
learning_rate = 0.0001
max_reward = 0.01
min_reward = - 1