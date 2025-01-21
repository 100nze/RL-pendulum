import torch as th
import os
from stable_baselines3 import SAC
import onnx
import logging
from environment import PendulumEnAW
import results

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OnnxablePolicy(th.nn.Module):
    def __init__(self, extractor, latent_pi, mu):
        super(OnnxablePolicy, self).__init__()
        self.extractor = extractor
        self.latent_pi = latent_pi
        self.mu = mu

    def forward(self, observation):
        extracted_features = self.extractor(observation)
        latent_pi_out = self.latent_pi(extracted_features)
        mu_output = self.mu(latent_pi_out)
        # Normalizzazione
        # Stampa delle caratteristiche
        print("mu_output before tanh:", mu_output)

        return mu_output

# Carica l'ambiente e il modello
env = PendulumEnAW(energy_tank_init=5, max_steps_x_episode=500)
base_path = results.__path__[0]
model_path = os.path.join(base_path, "train_inf_5", "SAC_inf_2", "13.zip")
onnx_path = os.path.join(base_path, "train_inf_5", "SAC_actor_inf_2.onnx")
model = SAC.load(model_path, env)


# Crea il modello ONNX con solo la parte dell'attore
onnxable_model = OnnxablePolicy(
    model.policy.actor.features_extractor,
    model.policy.actor.latent_pi,
    model.policy.actor.mu
)

# Prepara un input fittizio per l'esportazione
observation_size = model.observation_space.shape
dummy_input = th.tensor([0,1,1], dtype=th.float32).reshape((1, observation_size[0]))
print(dummy_input)




# Esporta il modello in formato ONNX
th.onnx.export(
        onnxable_model.to('cpu'),
        dummy_input,
        onnx_path,
        export_params=True,
        opset_version=16,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output']
    )
    # Verifica il modello ONNX esportato
onnx_model = onnx.load(onnx_path)
onnx.checker.check_model(onnx_model)
print(f"ONNX model exported to {onnx_path}")