"""
Classes that are used to train the model.
"""

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
father_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(father_dir,"GUI"))
from kernal import game2048
import dqn_config as config
import numpy as np
import random
from collections import deque
import pickle
import gc
import tensorflow as tf
from tensorflow.keras import layers, models


"""
The class env create the environment that the agent will interact with.
It inherits the APIs of superclass game2048 and several more are added:
    - step: take an integer in range(4) that represent the action and update the game state(time, score, matrix)
    - processed_matrix_view: return the view of self.matrix in the shape of np.array[16]
    - processed_matrix_copy: return a copy of self.matrix in the shape of np.array[16]
    - deliver_experience: return the experience and map that fits the replay buffer
"""
class env(game2048):
    def __init__(self,dimension):
        super().__init__(dimension)
        # convert the matrix to float32
        self.matrix.astype(np.float32)
    
    def step(self, action:int)->bool:
        changed = super().update(config.action_space[action])
        return changed
    
    def processed_matrix_view(self)->np.array:
        return self.matrix.reshape([1,config.state_shape[0]])
    
    def processed_matrix_copy(self)->np.array:
        return self.matrix.copy().reshape([1,config.state_shape[0]])
    
    def deliver_experience(self):
        """
        return the experience(nparray,list of nparray) and map(llist[np.float32,int,bool]) that fits the replay buffer
        """
        # initialize a game to record current state
        cg = env(self.dimension)
        #initialize the next_states and map
        next_states = []
        map = []
        for action in range(config.action_size):
            # record current state and score
            cg.clone(self)
            changed = cg.move(config.action_space[action])
            # if invalid action, skip
            if not changed:
                map.append((np.float32(0),0,False))
                continue
            # else record the reward and the next states
            ecn = 0
            for cell in range(self.dimension**2):
                if cell == 0:
                    ecn += 1
            necn = 0
            done = False
            for line in range(self.dimension):
                for col in range(self.dimension):
                    if cg.matrix[line][col] != 0:
                        continue
                    necn += 1
                    cg.matrix[line][col] = 2
                    next_states.append(cg.processed_matrix_copy())
                    if cg.gameover():
                        done = True
                    cg.matrix[line][col] = 4
                    next_states.append(cg.processed_matrix_copy())
                    if cg.gameover():
                        done = True
                    cg.matrix[line][col] = 0
            reward = (np.log2(cg.score - self.score+1)/20.0+(ecn-necn)/8.0)/2.0 * config.max_reward
            map.append((np.float32(reward),int(necn*2),done))
        return (self.processed_matrix_copy(),next_states),map


"""
The class ReplayBuffer is used to store the experiences.
It provides the following APIs:
    - add: add an experience to the buffer
    - sample: sample a batch of experiences(np.array of states, list of next_states, list of maps)
    - size: return the size of the buffer
Its data structure is show below:
buffer:[..., (state, next_states), ...]      map:[..., [map], ...]
 
       |<--  0 ~ 16  -->|                   

s      +----------------+                    [

       +----------------+                        [r_0, 4, done],
    0  |       0        |
    1  |                |
    2  |                |
    3  |                |
       +----------------+                        [r_1, 3, done],
    4  |       1        |
ns  5  |                |
    6  |                |
       +----------------+                        [r_2, 0, done],
               2         
       +----------------+                        [r_3, 2, done],
    7  |       3        |
    8  |                |
    9  |                |
       +----------------+                                          ]
    
"""
class ReplayBuffer:
    def __init__(self, max_size, batch_size):
        # constant
        self.batch_size = batch_size
        # buffer and map
        self.buffer = deque(maxlen=max_size)
        self.map = deque(maxlen=max_size)

    @property
    def size(self):
        return len(self.buffer)

    def add(self, experience,map):
        self.buffer.append(experience)
        self.map.append(map)

    def sample(self):
        indices = np.random.choice(len(self.buffer), self.batch_size, replace=False)
        states = np.array([self.buffer[i][0][0] for i in indices])
        next_states = [self.buffer[i][1] for i in indices]
        maps = [self.map[i] for i in indices]
        return states, next_states, maps

    def load(self, path):
        with open(path, "rb") as f:
            self.buffer, self.map = pickle.load(f)
    
    def save_and_clear(self, path):
        with open(path, "wb") as f:
            pickle.dump((self.buffer, self.map), f)
            self.buffer.clear()
            self.map.clear()


"""
The class q_network is used to create and operate the Q-network.
It provides the following APIs:
    - calculate_target_qs: calculate the target q(s,a) for the loss function
    - fit: fit the model with states and target_qs
    - load: load the model from path
    - save: save the model to path
    - model.get_weights: get the weights of the model
    - model.set_weights: set the weights of the model
"""
class q_network:
    def __init__(self):
        self.model = models.Sequential()
        self.model.add(layers.Dense(12, input_shape=config.state_shape, activation='relu'))
        self.model.add(layers.Dense(8, activation='relu'))
        self.model.add(layers.Dense(config.action_size, activation='linear'))
        self.model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=config.learning_rate), loss='mse')
        self.model.summary()

        self.target_qs = np.zeros((config.buffer_batch_size, config.action_size),dtype=np.float32)

    def calculate_target_qs(self,next_states,maps)->np.array:
        """
        q(s,a) = r + gamma * E( max( q(s',a') ) ) if not done
        q(s,a) = -1                        if done
        """

        for i in range(config.buffer_batch_size):
            next_qs_i = [self.model.predict_on_batch(next_states[i][j]) for j in range(len(next_states[i]))]
            head = 0
            for action in range(config.action_size):
                if maps[i][action][2]:
                    self.target_qs[i][action] = config.min_reward
                elif maps[i][action][1] == 0:
                    self.target_qs[i][action] = 0
                else:
                    self.target_qs[i][action] = np.mean([max(next_qs_i[p]) for p in range(head,head + maps[i][action][1])]) * config.dqn_gamma + maps[i][action][0]
                head += maps[i][action][1]
            del next_qs_i
        del next_states
        del maps
        gc.collect()
        return self.target_qs
    
    def fit(self,states:np.ndarray,target_qs:np.ndarray):
        self.model.fit(states, target_qs, epochs=1, verbose=1)
        del states
        del target_qs
        gc.collect()

    def load (self,path:str):
        model = models.load_model(path)
        self.model.set_weights(model.get_weights())
        del model
        gc.collect()

    def save(self,path:str):
        self.model.save(path)


"""
The class dqn_agent is used to create and operate the DQN agent.
It provides the following APIs:
    - update_target_network: update the target network with the q network
    - act: return the action priority
    - remember: add the experience to the replay buffer
    - replay: train the model with replay buffer
"""
class agent:
    def __init__(self):
        self.epsilon = 1.0
        self.memory = ReplayBuffer(max_size=config.buffer_max_size,batch_size=config.buffer_batch_size)
        self.q_network = q_network()
        self.target_network = q_network()
        self.update_target_network()
        self.action_priorty = [0,1,2,3]

    def update_target_network(self):
        self.target_network.model.set_weights(self.q_network.model.get_weights())
    
    def act(self,state:np.array):
        if np.random.rand() <= self.epsilon:
            random.shuffle(self.action_priorty)
            return self.action_priorty
        q_values = self.q_network.model.predict_on_batch(state)
        for i in range(4):
            for j in range(i,4):
                if q_values[0][self.action_priorty[i]] < q_values[0][self.action_priorty[j]]:
                    self.action_priorty[i], self.action_priorty[j] = self.action_priorty[j], self.action_priorty[i]
        return self.action_priorty
    
    def remember(self,experience,map):
        self.memory.add(experience,map)

    def replay(self):
        if self.memory.size < config.start_replay:
            return
        states, next_states, maps = self.memory.sample()
        target_qs = self.target_network.calculate_target_qs(next_states,maps)
        self.q_network.fit(states,target_qs)
        if self.epsilon > config.epsilon_min:
            self.epsilon -= config.epsilon_decay
