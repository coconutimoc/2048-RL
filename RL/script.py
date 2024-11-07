import dqn
import dqn_config as config

if __name__ == "__main__":
    #initialize the agent
    agent = dqn.agent()
    #load q_network, or the q network will be trained from scratch
    #agent.q_network.load("path/to/q_network")
    #test if the q network is can be saved
    #agent.q_network.save(config.save_path(0))

    #initialize the environment
    environment = dqn.env(dimension=config.matrix_dimension)

    #start training
    for e in range(config.episodes):
        #reset the environment when the game is over
        environment.reset()
        #start the game
        while True:
            # generate experience according to the current state
            experience, map = environment.deliver_experience()
            # get a priority of action according to the current state
            action_priority = agent.act(environment.processed_matrix_view())
            # try to update the environment with action according to the priority
            for action in action_priority:
                if environment.step(action):
                    break
            # if the game is over break the loop and update the target network if needed
            if environment.gameover():
                if (e+1) % config.update_step == 0:
                    agent.update_target_network()
                print(f"Episode: {e+1}/{config.episodes}, Score: {environment.score}, Time: {environment.time} Epsilon: {agent.epsilon:.4f}")
                break
            # if the game is not over, remember the experience and replay
            agent.remember(experience, map)
            if agent.memory.size > config.start_replay:
                agent.replay()

        #save the model
        if (e+1) % config.save_step == 0:
            agent.q_network.save(config.save_path(e+1))
            print(f"Episode: {e+1}/{config.episodes}, model saved at {config.save_path(e+1)}")
        
