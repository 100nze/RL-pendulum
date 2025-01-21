
from stable_baselines3 import SAC
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
import os
from environment import PendulumEnAW
from typing import Callable
import results

def linear_schedule(initial_value: float) -> Callable[[float], float]:
    """
    Linear learning rate schedule.

    :param initial_value: Initial learning rate.
    :return: schedule that computes
      current learning rate depending on remaining progress
    """
 
    def func(progress_remaining: float) -> float:
        """
        Progress will decrease from 1 (beginning) to 0.

        :param progress_remaining:
        :return: current learning rate
        """
        return progress_remaining * initial_value

    return func


num_run = "5"
run_type = "e0_5"
results_dir = results.__path__[0]
dir = results_dir + f"/train_{run_type}/SAC_e0_{num_run}"
dir_log = results_dir + f"/train_{run_type}/log"

if not os.path.exists(dir):
    os.makedirs(dir)
if not os.path.exists(dir_log): 
    os.makedirs(dir_log)


# Create the environment
einf = 100000
e0 = 0.2
env = PendulumEnAW(energy_tank_init=e0,energy_tank_threshold=0, max_steps_x_episode=2500,log_EpEnergy_tf=True, run = num_run, run_type = run_type)
env = Monitor(env)  # Wrap the environment to monitor performance
env = DummyVecEnv([lambda: env])  # Wrap the environment to work with Stable Baselines
env.reset()
# Initialize the model
model = SAC("MlpPolicy", 
            env,
            #buffer_size= int(1e6),
            #learning_starts = 2500,  #start learning after 2500 steps
            #batch_size = 256,      #Minibatch size for each gradient update  
            #train_freq= (500,"step"), #Update the model every train_freq steps
            #learning_rate = linear_schedule(5e-3), 
            #tau = 3e-3, #the soft update coefficient
            #gamma=0.99, #the discount factort
            #use_sde_at_warmup = True , 
            use_sde = True, #esplorazione ottimizzata
            verbose=1,tensorboard_log = dir_log) 

# Train the model
i = 0
while True:
    i += 1
    model.learn(total_timesteps=10*2500, log_interval=1,tb_log_name = f"SAC_{run_type}_{num_run}",reset_num_timesteps=False) # reset_num_timesteps=False is important to continue training non azzerarlo mentre facciamo il training 30 volt
    model.save(f"{dir}/{1*i}") # save the model after each training lo slash non sta per divisione ma per directory