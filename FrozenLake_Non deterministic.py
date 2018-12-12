#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gym
import readchar


# In[2]:



#MACROS
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

#Key mapping
arrow_keys = {
    '\x1b[A' : UP,
    '\x1b[B' : DOWN,
    '\x1b[C' : RIGHT,
    '\x1b[D' : LEFT
}


# In[3]:




#Register FrozenLake with is_slippery False
env = gym.make('FrozenLake-v0')
env.reset()
env.render() #Show the initial board


# In[4]:


while True:
    #Choose an action from keyboard
    key = readchar.readkey()
    
    if key not in arrow_keys.keys():
        print("Game aborted!")
        break
    
    action = arrow_keys[key]
    state, reward, done, info = env.step(action)
    env.render() # Show the board after action
    print("State: ", state, "Action", action, "Reward: ", reward, "Info: ", info)
    
    if done:
        print("Finished with reward ", reward)
        break

