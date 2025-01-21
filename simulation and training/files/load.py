from environment import PendulumEnAW
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
import torch as th
from torch.utils.tensorboard import SummaryWriter  
import os
import results

# Create the environment
#num_stepxepisodes = 500
num_stepxepisodes = 500
einf = 100000
run_type = "inf_5"
num_run = "inf_2"

e0 = 0.2
init = einf
env = PendulumEnAW(energy_tank_init=init, max_steps_x_episode= num_stepxepisodes,
                   #log_EpEnergy_tf=True
                    #render_mode="human"
                   #print_stat=True
                   )

env = Monitor(env)  # Wrap the environment to monitor performance
env = DummyVecEnv([lambda: env])  # Wrap the environment to work with Stable Baselines
env.reset()
results_dir = results.__path__[0]
# Initialize the model/
train_inf_path = os.path.join(results_dir, f"train_{run_type}",f"SAC_{num_run}") 
modelpath = f"{train_inf_path}/13"
#episodes = 300
episodes = 200
TB = 3 # 1 for energy per episode, 2 for energy per step, 3 for position error
Energy_perEp = np.zeros(episodes) 
mean_energy = th.zeros(num_stepxepisodes)
mean_error = th.zeros(num_stepxepisodes)
error_ep = th.zeros(num_stepxepisodes)
model = SAC.load(modelpath, env=env)

a = 0
sum = 0
# Evaluate the trained model
if TB == 2 or TB == 3 or TB == 4:
    value = np.zeros(num_stepxepisodes*episodes)
    stepps = 0


obs = env.reset()
for ep in range(episodes):
    done = False
    if TB == 1:
        value = 0
        stepps = 0
    while not done:
        env.render()
        action,_state = model.predict(obs, deterministic=True)
        #print(f"action: {action}")
        
        if TB == 1 or TB == 2:  
            value[stepps] = init-env.envs[0].energy_tank
            #print(f"int: {init}, tank: {env.envs[0].energy_tank}, diff: {init-env.envs[0].energy_tank}, value:{value}")

        if TB == 3:
            th_normalized = ((env.envs[0].state[0] + np.pi) % (2 * np.pi)) - np.pi
            if th_normalized >= 0.157:
                pos_err = 0.335*th_normalized - 0.0526
            elif th_normalized <= -0.096:
                pos_err = -0.329*th_normalized + 0.0316
            else:
                pos_err = 0
            value[stepps] = pos_err
        if TB == 4:
            th_normalized = ((env.envs[0].state[0] + np.pi) % (2 * np.pi)) - np.pi
            error = th_normalized / np.pi
            error_ep[stepps] = np.abs(error)
        if TB != 0: 
            stepps +=1
        a +=1
        print(a/num_stepxepisodes)
        obs, reward, done, info = env.step(action)
        
    if TB == 1:
        #print(f"{value}")
        Energy_perEp[ep] = value
        print( Energy_perEp[ep])

if TB == 1:
    for i in range(episodes):
        sum += Energy_perEp[i]
    total_mean_energy = sum/episodes
    writer = SummaryWriter(log_dir=results_dir + f"/train_{run_type}/log/task_energy_inference")
    for i in range(episodes):
        #writer.add_scalar('Energy/Mean_per_episode2', Energy_perEp[i], i+1)
        writer.add_scalar('Energy/Mean_task2', total_mean_energy, i+1)
    writer.close()

if TB == 2:
    writer = SummaryWriter(log_dir=results_dir + f"/train_{run_type}/log/task_energy")
    for i in range(num_stepxepisodes):
        sum = 0
        for j in range(episodes):
            sum += value[i+j*num_stepxepisodes]
        mean_energy[i] = sum/episodes
        writer.add_scalar('Energy/Mean_task_energy_inference', mean_energy[i], i)
        print(f'{mean_energy[i]}')
    writer.close()

if TB == 3:
    writer = SummaryWriter(log_dir=results_dir + f"/train_{run_type}/log/position_error")
    for i in range(num_stepxepisodes):
        sum = 0
        for j in range(episodes):
            sum += value[i+j*num_stepxepisodes]
        mean_error[i] = sum/episodes
        writer.add_scalar('Error/Mean_task_error', mean_error[i], i)
    
    writer.close()


env.close()
