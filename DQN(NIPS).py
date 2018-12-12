#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import tensorflow as tf
import random
import dqn
from collections import deque
import gym


# In[3]:


env = gym.make('CartPole-v0')
env._max_episode_steps = 10001


# In[4]:


#Constants defining our neural network
input_size = env.observation_space.shape[0]
output_size = env.action_space.n

dis = 0.9
REPLAY_MEMORY = 50000


# In[ ]:


def simple_replay_train(DQN, train_batch):
    x_stack = np.empty(0).reshape(0, DQN.input_size)
    y_stack = np.empty(0).reshape(0, DQN.output_size)

    #Get stored information from the buffer
    for state, action, reward, next_state, done in train_batch:
        Q = DQN.predict(state)

        #terminal?
        if done:
            Q[0, action] = reward
        else:
            #Obtain the Q' values by feeding the new state through our network
            Q[0, action] = reward + dis * np.max(DQN.predict(next_state))

        y_stack = np.vstack([y_stack, Q])
        x_stack = np.vstack([x_stack, state])

        #Train our network using target and predicted Q values on each episode
        return DQN.update(x_stack, y_stack)


# In[ ]:


def bot_play(mainDQN):
    #See our trained network in action
    s = env.reset()
    reward_sum = 0
    while True:
        env.render()
        a = np.argmax(mainDQN.predict(s))
        s, reward, done, _ = env.step(a)
        reward_sum += reward
        if done:
            print("Total score: {}".format(reward_sum))
            break


# In[ ]:


def main():
    max_episodes = 2000

    #store the previous observations in replay memory
    replay_buffer = deque()

    with tf.Session() as sess:
        mainDQN = dqn.DQN(sess, input_size, output_size)
        init = tf.global_variables_initializer()
        sess.run(init)

        for episode in range(max_episodes):
            e = 1. / ((episode / 10) + 1)
            done = False
            step_count = 0

            state = env.reset()

            while not done:
                if np.random.rand(1) < e:
                    action = env.action_space.sample()
                else:
                    #Choose an action by greedily form the Q-network
                    action = np.argmax(mainDQN.predict(state))

                #Get new state and reward from environment
                next_state, reward, done, _ = env.step(action)
                if done:
                    reward = -100

                #Save the experience to our buffer
                replay_buffer.append((state, action, reward, next_state, done))
                if len(replay_buffer) > REPLAY_MEMORY:
                    replay_buffer.popleft()

                state = next_state
                step_count += 1
                if step_count > 10000:
                    break

            print("Episode: {}        steps: {}".format(episode, step_count))
            if step_count > 10000:
                pass
                #break

            if episode % 10 == 1:
                #Get  a random batch of experiences.
                for _ in range(50):
                    #Minibatch works better
                    minibatch = random.sample(replay_buffer, 10)
                    loss, _ = simple_replay_train(mainDQN, minibatch)
                    print("Loss: ",loss)

        bot_play(mainDQN)


# In[ ]:


if __name__ == "__main__":
    main()
