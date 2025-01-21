
from environment import PendulumEnAW

# Create the custom environment
env = PendulumEnAW(energy_tank_init=4000, max_steps_x_episode=400000, 
                   render_mode="human",
                   print_stat=True
                   )

# Reset the environment
for _ in range(10):
    observation = env.reset()

    # Run the simulation for a fixed number of steps
    for _ in range(400):

        #action = env.action_space.sample()
        action = 0

        observation, reward,terminated,truncated,info = env.step(action)

 
env.close()