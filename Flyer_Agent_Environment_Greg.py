
# coding: utf-8

# # Flyer Agent Environment

# ## NOTE: Graphics won't work with 'Run All' - must 'Shift+Enter' cell by cell!
# Also - need to 'Restart and Clear Output' Every Time! <br>
# Also - figure window will only show up near top and can't be moved.<br>
# Also - print statements won't work if Vpython is in use.<br>
# Vpython is heavily flawed.<br>

# Notes:
# state_prime is next state

# In[40]:


# !pip install tqdm
# ! pip install gym
# !pip install tensorflow


# In[41]:


import tensorflow as tf
import numpy as np
import random
import gym
import tqdm
slim = tf.contrib.slim


# In[80]:


# flyer environment

# Destination Goal of Flyer
goal_x = 0
goal_y = 0
# goal_z = 0
# INITIAL GOAL: Hovering

# coordinates are looking AT flyer:
# - standard x and y axes, polar axis 
# for angles is same direction as x axis, angles are more positive going
# counter-clockwise

max_displacement = 10
spatial_inc = 1
 # State
#             s[0] - x coord of flyer
#             s[1] - y coord of flyer
#             s[2] - right wing angle
#             s[3] - left wing angle
# Action
# call it 1-hot for now - 9 total - goes from 0 to 8
# 0 - no movement
# 1 - down
# 2 - up
# then combine that in 'trinary' for both wings - Left wing first, then Right
# e.g. 1,2 = Left Down, Right Up = Action # 3*1 + 2 = 5

class FlyerAgentEnv(object):

    def __init__(self):
        self.state = [0,0,0,180]
        self.action = np.zeros(9)
        self.action[0] = 1 # so initial action is no movement - action #0
        
    def reset(self):
        self.state = [0,0,0,180]
        return self.state
    
    
    def check_done(self):
        # done if flyer distance from origin exceeds max value (in square)
        if (abs(self.state[0] - goal_x) >= max_displacement) or              (abs(self.state[1] - goal_y) >= max_displacement):
            done_flag = True
        else:
            done_flag = False
        return done_flag
    
    def calc_reward(self):
        # define reward function that will get us to goal
        reward = 1 # reward for being alive 
        return reward
      
    def calc_next_state(self):
        s_prime = [0]*4 # python's empty list creation (ugh)
        DX = 1 # ie delta x
        DY = 2
        DA = 10 # delta angle (in degrees)
        G = -1 # gravity
        transition_matrix = np.array([[1,0,0,0,    0, -DX,   0,  DX,   0,  DX,   0, -DX,   0,  0],
                            [0,1,0,0,    0,  DY,   0,  DY,2*DY,  DY,   0,  DY,   0,  G],
                            [0,0,1,0,    0,   0,   0, -DA, -DA, -DA,  DA,  DA,  DA,  0],
                            [0,0,0,1,    0, -DA,  DA,   0, -DA,  DA,   0, -DA,  DA,  0]])
        state_action_grav_vec = []
        state_action_grav_vec.extend(self.state)
        state_action_grav_vec.extend(self.action)
        state_action_grav_vec.extend([1])
        state_action_grav_vec = np.transpose(np.asarray([state_action_grav_vec])) 
        # Note: []'s make it 2-d vector
        s_prime = np.squeeze(np.matmul(transition_matrix,state_action_grav_vec)).tolist()
        return s_prime
                
    def step(self, action):
        # need to convert to one-hot
        OH_action = [0]*9
        OH_action[action] = 1
        self.action = OH_action
        state_prime = self.calc_next_state()
        terminal = self.check_done()
        info = 0
        # update state!
        self.state = state_prime
        reward = self.calc_reward()
        return state_prime, reward, terminal, info    
    
    def render(self):
        # place holder for now   
        return None


# env = FlyerAgentEnv()
# print(env.state)
# print(env.action)
# new_action = env.action
# for n in range(9):
#     env.reset()
#     a = [0]*9
#     a[n] = 1
#     state_prime, reward, terminal, info = env.step(a)
#     print(state_prime)

# # Graphics Constants for Flyer
# f_length = 3
# f_radius = 0.7
# w_span = 5
# w_depth = f_length
# w_thickness = 0.2
# w_size = vector(w_span,w_thickness,w_depth)
# f_axis = vector(0,0,f_length)
# h_radius = f_radius

# def update_graphics(s,s_prime,flyer,r_wing,l_wing,head):
#     # translate model
#     f_center_new = vector(s_prime[0],s_prime[1],s_prime[2])
#     f_center_prev = vector(s[0],s[1],s[2])
#     transl_vec = f_center_new - f_center_prev
#     
#     flyer.pos += transl_vec
#     r_wing.pos += transl_vec
#     l_wing.pos += transl_vec
#     head.pos += transl_vec
#     # then rotate wings
#     r_delta = s_prime[3] - s[3]
#     l_delta = s_prime[4] - s[4]
#     r_wing.rotate(angle=r_delta*np.pi/180.0, axis=flyer.axis, origin=flyer.pos)
#     l_wing.rotate(angle=l_delta*np.pi/180.0, axis=flyer.axis, origin=flyer.pos)
#     
# #     print(r_wing.pos,l_wing.pos)
#     
#     

# def main():
# 
#     env = FlyerAgentEnv()
#     num_actions = 4
#     state_size = 5
#     terminal = False
#     num_steps = 0
# 
#     state = env.reset()
#     while not terminal:
#         rate(1) # Vpython does not work correctly here...
#         num_steps += 1
#         action = ??????????????
#         state_prime, reward, terminal, _ = env.step(action)
# 
#         update_graphics(state,state_prime,flyer,r_wing,l_wing,head)
# #         print(action,state,state_prime,reward,terminal)
# #         input('hit enter to continue...')
# 
#         state = state_prime       
# 

# # Background Graphics
# scene.background = color.gray(0.95)
# floor = box(pos=vector(0,-1,0), size=vector(12,0.2,12), color=color.green)
# g_center = vector(goal_x,goal_y,goal_z)
# goal_sphere = sphere(pos=g_center, radius=h_radius, color=color.blue)
# 
# # Show Initial Flyer Graphics
# f_center = vector(0,0,0)
# h_center = f_center + vector(0,0,f_length+1)
# r_w_center = f_center + vector(0,0,f_length/2) + vector(2*f_radius+w_span/2,0,0)
# l_w_center = f_center + vector(0,0,f_length/2) + vector(-1*(2*f_radius+w_span/2),0,0)
# flyer = cylinder(pos=f_center, radius=f_radius, axis=f_axis, color=color.red)
# r_wing = box(pos=r_w_center, size=w_size, color=color.red)
# l_wing = box(pos=l_w_center, size=w_size, color=color.red)
# head = sphere(pos=h_center, radius=h_radius, color=color.red)
# 
# main()

# tmp = []
# tmp.extend([1,2])
# tmp.extend([1])
# print(tmp)
# 
