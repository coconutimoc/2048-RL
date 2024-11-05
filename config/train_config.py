import re

session_id = 1

agent = 'DQN'


#if agent path empty, config new training session and agent
if agent == "DQN":
    # training
    agent_id = agent+str(session_id)
    episodes = 1500
    save_path = f"agent/{agent_id}.pkl"

    #env
    matrix_dimension = 4
    state_shape = (matrix_dimension ** 2,)
    action_size = 4
    action_space = ["up", "down", "left", "right"]

    #agent
    buffer_max_size = 100000
    start_replay = 2000
    buffer_batch_size = 32
    epsilon_decay = 0.0001
    epsilon_min = 0.01
    dqn_gamma = 0.9
    learning_rate = 0.00025

