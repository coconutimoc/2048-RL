from config.train_config import *
from kernal import game2048
import numpy as np
import random
from collections import deque
import pickle
import tensorflow as tf
from tensorflow.keras import layers, models

class environment(game2048):
    def __init__(self, dimension):
        super().__init__(dimension)
        self.cm2 = self.matrix.copy()

    def step(self, action):
        changed = super().update(action_space[action])
        return changed

    def reset(self):
        super().reset()
        return self.matrix.reshape([1, state_shape[0]])

    def deliver_experience(self):
        #record current state
        for line in range(self.dimension):
            for col in range(self.dimension):
                self.cm2[line][col] = self.matrix[line][col]
        cscore = self.score
        #calculate the experience tree
        experience = [self.matrix.copy().reshape([1, state_shape[0]]),-1]#-1 to be updated by real action
        for action in range(4):
            branch = [action,0]
            #if invalid action, skip
            changed = self.move(action_space[action])
            if not changed:
                experience.append(branch)
                continue
            #if valid action, record reward and states after the action
            branch[1]+=np.log2(self.score - self.last_score+1)/20.0
            empty_cells_num = 0
            for line in range(self.dimension):
                for col in range(self.dimension):
                    if self.matrix[line][col] != 0:
                        continue
                    empty_cells_num += 1
                    self.matrix[line][col] = 2
                    branch.append([self.matrix.copy().reshape([1, state_shape[0]]), self.gameover()])
                    self.matrix[line][col] = 4
                    branch.append([self.matrix.copy().reshape([1, state_shape[0]]), self.gameover()])
                    self.matrix[line][col] = 0
            branch[1]+=empty_cells_num/16.0
            experience.append(branch)
            for line in range(self.dimension):
                for col in range(self.dimension):
                    self.matrix[line][col] = self.cm2[line][col]
            self.score = cscore
        return experience

# replay buffer
class ReplayBuffer:
    def __init__(self, max_size, batch_size):
        # the oldest data will be freed when the buffer is full
        self.buffer = deque(maxlen=max_size)
        self.batch_size = batch_size

    @property
    def size(self):
        return len(self.buffer)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self):
        return random.sample(range(self.size), self.batch_size)


def build_q_network(state_shape, action_size, learning_rate):
    """initialize the Q network"""
    model = models.Sequential()
    model.add(layers.Dense(12, input_shape=state_shape, activation='relu'))
    model.add(layers.Dense(8, activation='relu'))
    model.add(layers.Dense(action_size, activation='linear'))
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')
    model.summary()
    return model

# DQN Agent
class DQNAgent:
    def __init__(self):
        self.memory = ReplayBuffer(max_size=buffer_max_size,batch_size=buffer_batch_size)
        self.gamma = dqn_gamma
        self.epsilon = 1.0
        self.q_network = build_q_network(state_shape, action_size,learning_rate)
        self.target_network = build_q_network(state_shape, action_size,learning_rate)
        self.update_target_network()
        self.batch_states = np.zeros((buffer_batch_size, state_shape[0]))
        self.target_qs = np.zeros((buffer_batch_size, action_size))
        self.action_priorty = np.array([0,1,2,3])

    def update_target_network(self):
        self.target_network.set_weights(self.q_network.get_weights())

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            random.shuffle(self.action_priorty)
        q_values = self.q_network.predict_on_batch(state)
        for i in range(4):
            for j in range(i,4):
                if q_values[0][self.action_priorty[i]] < q_values[0][self.action_priorty[j]]:
                    self.action_priorty[i], self.action_priorty[j] = self.action_priorty[j], self.action_priorty[i]
        return self.action_priorty

    def remember(self, experience):
        self.memory.add(experience)

    def replay(self):
        for i in range(buffer_batch_size):
            for action in range(action_size):
                self.target_qs[i][action] = 0
        if self.memory.size < start_replay:
            return
        indices = self.memory.sample()
        for n in range(buffer_batch_size):
            i = indices[n]
            for action in range(action_size):
                if len(self.memory.buffer[i][action+2]) == 2:
                    self.target_qs[n][action] = 0
                    continue
                p = 2
                while p < len(self.memory.buffer[i][action+2]):
                    if self.memory.buffer[i][action+2][p][1]:
                        self.target_qs[n][action] += -1
                    self.target_qs[n][action] += np.mean(self.q_network.predict_on_batch(self.memory.buffer[i][action+2][p][0])) * self.gamma
                    p += 1
                self.target_qs[n][action] = self.target_qs[n][action] / (p - 2) + self.memory.buffer[i][action+2][1]
        for batch in range(buffer_batch_size):
            for i in range(state_shape[0]):
                self.batch_states[batch][i] = self.memory.buffer[indices[batch]][0][0][i]
        self.q_network.fit(self.batch_states, self.target_qs, epochs=1, verbose=0)
        if self.epsilon > epsilon_min:
            self.epsilon -= epsilon_decay


if __name__ == "__main__":
    with open("log/train_log.csv", "a+", encoding="utf-8") as log:
        log.write(f"\nTraining session {session_id} start!\n")
        log.write(f" Agent:{agent}, training episodes:{episodes}\n")

    if agent == "DQN":
        agent = DQNAgent()

    env = environment(dimension=matrix_dimension)

    for e in range(episodes):
        state = env.reset()
        while True:
            experience = env.deliver_experience()
            action_priority = agent.act(state)
            i = 0
            for action in action_priority:
                if env.step(action):
                    i+=1
                    break
            if env.gameover():
                for i in range(min(30,env.time-1)):
                    action = agent.memory.buffer[agent.memory.size-1-i][1]
                    agent.memory.buffer[agent.memory.size-1-i][action+2][1] = -1
                agent.update_target_network()
                print(f"Episode: {e+1}/{episodes}, Score: {env.score}, Time: {env.time} Epsilon: {agent.epsilon:.2}")
                with open("log/train_log.csv", "a+", encoding="utf-8") as log:
                    log.write(f"Episode: {e+1}/{episodes}, Score: {env.score}, Epsilon: {agent.epsilon:.2}\n")
                break
            state = env.matrix.reshape([1, state_shape[0]])
            experience[1] = action_priority[i]
            agent.remember(experience)
            if agent.memory.size > start_replay:
                agent.replay()
                print(f"replay done for time {env.time}, episode {e+1}")

    with open(save_path, "wb") as f:
        pickle.dump(agent, f)
    print(f"Training session {session_id} finished!")
    print(f"Agent saved to {save_path}")
    with open("log/train_log.csv", "a+", encoding="utf-8") as log:
        log.write(f"Training session {session_id} finished!\n")
        log.write(f"Agent saved to {save_path}\n")
        
