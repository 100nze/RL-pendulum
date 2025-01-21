import gymnasium as gym
from gymnasium import spaces
from os import path
from typing import Optional
import numpy as np
import pygame
from pygame import gfxdraw
from torch.utils.tensorboard import SummaryWriter
import results
class PendulumEnAW(gym.Env):
    """

    The starting state is a random angle in *[-pi, pi]* and a random angular velocity in *[-1,1]*.


    """

    metadata = {
        "render_modes": ["human"],
        "render_fps": 24,
    }

    def __init__(self, 
                 render_mode: Optional[str] = None, 
                 energy_tank_init = None,
                 energy_tank_threshold = 0.0,
                 max_steps_x_episode = 500,
                 print_stat = False,
                 log_EpEnergy_tf = None,
                 run = 0,
                 run_type = None
                  ):
        self.run_type = run_type
        self.print_stat = print_stat
        self.DEFAULT_X = np.pi
        self.DEFAULT_Y = 1.0
        self.max_steps = max_steps_x_episode    # numero massimo di step per episodio
        self.steps = 0          # contatore step 
        self.dt = 0.0005 #1ms tempo di integrazione delle equazioni differenziali 
        self.control_period = 50 #ms
        self.current = 0 #corrente iniziale
        self.energy_tank_init = energy_tank_init
        self.energy_tank = self.energy_tank_init
        self.energy_tank_threshold = energy_tank_threshold
        self.render_mode = render_mode
        self.energyEx = 0
        self.epcount = -1
        self.total_reward = 0
        self.screen_dim = 500
        self.screen = None
        self.clock = None
        self.isopen = True
        self.empty = False

        results_dir = results.__path__[0]
        #self.writer = SummaryWriter(log_dir=results_dir + f"/train_{run_type}/log/energy_{run}")
        self.writer = SummaryWriter(log_dir=results_dir + f"/train_e0_5/log/train_energy_{run}")
        self.log_EpEnergy_tf = log_EpEnergy_tf

        high = np.array([1.0, 1.0, 1], dtype=np.float32)
        low = np.array([-1.0, -1.0, -1], dtype=np.float32)

        self.action_space = spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        self.surf = None
    def updateTank(self, torque, th, newth):
        if self.energy_tank <= self.energy_tank_threshold:
            self.energyEx = 0
            energy_available = False
        else:
            self.energyEx = torque * (newth - th)
            if self.energyEx > 0:
                self.energy_tank -= self.energyEx

            if self.energy_tank < self.energy_tank_threshold:
                self.energy_tank = 0
                energy_available = False
            else:
                energy_available = True
        return energy_available



    def step(self, V):
        th, thdot = self.state  # th := theta
        b = 0.001 #attrito viscoso
        g = 9.81 ##m/s^2
        m_1 = 0.009 #kg massa asta
        d = 0.19 #m lunghezza asta
        s = 0.02 #m spessore asta
        m_3 = 0.005 #kg massa primo pesetto
        d_3 = 0.12 #m distanza primo pesetto
        m_4 = 0.007 #kg massa secondo pesetto
        d_4 = 0.16
        dt = self.dt
        k_t = 0.07
        k_e = 0.07
        r = 32 #ohm resistenza di armatura
        m_2 = 0.0015 #kg massa cerchio
        rc = 0.02 #m raggio cerchio
        tau_att = 0.07 
        self.current = (V * 12 - k_e * thdot) / r
        if V != 0:
            u = k_t * self.current
        else:
            u = 0        

        old_th = np.array([th]).flatten()
        substeps = self.control_period *2  #60*0.001 = 0.06s = 1/60 = 16.666Hz

        for _ in range(substeps):
          
            th_normalized = ((th + np.pi) % (2 * np.pi)) - np.pi

            if th_normalized >= 0.157:
                pos_err = 0.335*th_normalized - 0.0526
            elif th_normalized <= -0.096:
                pos_err = -0.329*th_normalized + 0.0316
            else:
                pos_err = 0

            #print(th_normalized, pos_err)
            i = (3*m_2*rc**2)/4 + m_1*((d**2)/3 + (s**2/12) + d*rc + rc**2)+ m_3*d_3**2 + m_4*d_4**2
            grav_term = m_1*((d/2) + rc) + m_3*d_3 + m_4*d_4
            thdot += ((u - b*thdot + g*grav_term*np.sin(th))/i)*dt
            # if abs(thdot) <= 0.01 and ((pos_err <= 0.05 and pos_err>=0) or (pos_err >=-0.0306 and pos_err<=0)) and (abs(u)<=0.07):
            #     thdot = 0
            if abs(thdot) <= 0.01 and pos_err<0.0001  and (abs(u)<=0.07):
                thdot = 0
            th += thdot * dt
            self.state = np.array([th, thdot])
        # if np.abs(pos_err)<0.4:
        #     reward = 1/(1 + np.abs(pos_err) + 0.5*np.abs(thdot) + 0.3*np.abs(u))
        # else:
        #     reward = 0
        # if self.print_stat == True:
        reward = 1/(1 + np.abs(pos_err) + 0.1*np.abs(thdot) + 0.01*np.abs(V))

        #print(f"pos_err: {pos_err},current:{self.current}, torque: {u}, energy: {self.energy_tank}") 

        self.steps += 1  # Increment the step counter
        terminated = not self.updateTank(u, old_th, th)
        truncated = self.steps >= self.max_steps  # Check if maximum steps per episode reached
        #####################################################################################################################
        if self.log_EpEnergy_tf and (terminated or truncated):
            self.energy_tank = self.energy_tank.item() if isinstance(self.energy_tank, np.ndarray) else self.energy_tank
            print(f"Tensorboard write ,epcount {self.epcount}, {self.energy_tank_init-self.energy_tank}")
            
            self.writer.add_scalar(f"train/energy_per_ep", self.energy_tank_init-self.energy_tank, self.epcount)
        ##########################################################################################################


        if self.render_mode == "human":
            self.render()

        return self._get_obs(), reward, terminated, truncated, {}

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        #reset bounds
        self.state = np.array([0.0,0.0])
        high = np.array([self.DEFAULT_X, self.DEFAULT_Y])
        low = -high
        self.state = self.np_random.uniform(low=low, high=high)
        #self.state = np.array([6.19, 0.0])
        self.last_u = None
        self.empty = False
        self.epcount += 1
        if self.epcount > 10000:
            self.writer.close()
        self.energy_tank = self.energy_tank_init
        self.energyEx = 0
        self.steps = 0
  
        self.surf = None

        if self.render_mode == "human":
            self.render()

        return self._get_obs(), {}

    def _get_obs(self):
        theta, thetadot = self.state
        return np.array([np.cos(theta), np.sin(theta), np.tanh(thetadot)]).flatten()

    def render(self):
        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode((self.screen_dim, self.screen_dim))

        if self.clock is None:
            self.clock = pygame.time.Clock()

        if self.surf is None:
            self.surf = pygame.Surface((self.screen_dim, self.screen_dim))
        self.surf.fill((255, 255, 255))

        bound = 2.2
        scale = self.screen_dim / (bound * 2)
        offset = self.screen_dim // 2

        rod_length = 1 * scale
        rod_width = 0.2 * scale
        if not hasattr(self, 'rod_coords'):
            l, r, t, b = 0, rod_length, rod_width / 2, -rod_width / 2
            self.rod_coords = [(l, b), (l, t), (r, t), (r, b)]

        transformed_coords = []
        for c in self.rod_coords:
            c = pygame.math.Vector2(c).rotate_rad(self.state[0] + np.pi / 2)
            c = (c[0] + offset, c[1] + offset)
            transformed_coords.append(c)
        #disegno asta
        pygame.draw.polygon(self.surf, (204, 77, 77), transformed_coords)
        pygame.draw.circle(self.surf, (204, 77, 77), (offset, offset), int(rod_width / 2))
        rod_end = pygame.math.Vector2(rod_length, 0).rotate_rad(self.state[0] + np.pi / 2)
        rod_end = (int(rod_end[0] + offset), int(rod_end[1] + offset))
        pygame.draw.circle(self.surf, (204, 77, 77), rod_end, int(rod_width / 2))
        pygame.draw.circle(self.surf, (0, 0, 0), (offset, offset), int(0.05 * scale))
        self.surf = pygame.transform.flip(self.surf, False, True)
        self.screen.blit(self.surf, (0, 0))
        pygame.event.pump()
        self.clock.tick(self.metadata["render_fps"])
        pygame.display.update()


    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()
            self.isopen = False



