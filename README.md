 
# RL-pendulum: Passive Control Policy for Simple Pendulum

Robotics is increasingly focusing on control frameworks that enable the transition from industrial cages to unstructured environments. In this context, the role of energy transfers between the robot, the controller, and its surroundings is crucial for assessing important system-theoretic properties (e.g., stability, passivity), safety metrics, and the behavioral patterns of the controlled robot. 

This repository implements a passively learned control policy for a simple pendulum, utilizing reinforcement learning (RL) techniques and microcontroller-based deployment. The project integrates the concept of virtual energy tanks to ensure system passivity during training and real-world application.

## Project Overview

This work explores the implementation of a passively learned policy for controlling a simple pendulum, using a microcontroller for physical deployment. The policy is trained within a reinforcement learning framework and then implemented on a real device to assess its performance.

### Key Features

- Two-stage reinforcement learning training process
- Passivity ensured through the use of virtual energy tanks
- Physical implementation on a microcontroller
- Comparative analysis between simulation and real-world results

## Methodology

For detailed methodology and results, please refer to the full [report](https://github.com/100nze/RL-pendulum/blob/main/DOCUMENTATION.pdf).

### Training Process

1. **Initial Training**: The system is first trained with unlimited energy to determine the required energy profile for the control task.
2. **Limited Energy Training**: A second phase of training is conducted with limited energy, employing virtual energy tanks to ensure system passivity.

### Physical Implementation

- Developed a microcontroller-based physical system
- Controlled a permanent magnet DC motor for pendulum movement
- Incorporated encoder reading functionality
- Integrated learned policy for real-time inference

## Installation

To set up this project locally, follow these steps:

1. Clone the repository:
   ``` 
   git clone https://github.com/100nze/RL-pendulum.git
   ```
2. Navigate to the project directory:
   ``` 
   cd RL-pendulum/simulation_and_training
   ```
3. Install the project in editable mode:
   ``` 
   pip install -e .
   ```
4. Install the required dependencies via conda:
   ``` 
   conda env create -f environment.yml
   ```

## Usage

### Training the Model

Inside the `simulation_and_training/files/` directory, you'll find the following Python scripts:

- **`Environment.py`**: Defines the training environment, modeled after the Gymnasium framework. This script simulates the pendulum’s dynamics and energy constraints, with configurable parameters such as energy limits, steps per episode, and episode termination thresholds.
  
- **`Load.py`**: Allows loading and evaluating previously trained models. The script visualizes the model’s performance and logs inference data to TensorBoard.

- **`Train.py`**: Trains the model using the Soft Actor-Critic (SAC) algorithm in its default configuration. Results are monitored via TensorBoard.

- **`OnnxConv3.py`**: After training, this script exports the model in ONNX format for further deployment steps.

For more details about the environment implementation, please refer to the [documentation](https://github.com/100nze/RL-pendulum/blob/main/DOCUMENTATION.pdf).

### Inference on Microcontroller

The `ESP_implementation/` directory contains code for deploying trained models onto a microcontroller. It includes two subfolders for models trained with unlimited and limited energy. Both subfolders share the following structure:

- `tflite-model/`: Contains the TensorFlow Lite model file.
- `model-parameters/`: Stores model-specific parameters.
- `edge-impulse-sdk/`: Contains necessary files for Edge Impulse integration.

The main folder includes custom code to integrate the models with the microcontroller hardware. **Do not modify the subfolders**, as they are automatically generated from Edge Impulse.

Python scripts are also provided for collecting sensor data through the serial port and visualizing it in plots.

## Contact

For questions or feedback, please open an issue on the GitHub repository or contact us via the email provided in the first page of the [report](https://github.com/100nze/RL-pendulum/blob/main/DOCUMENTATION.pdf).

## Acknowledgements

This work was conducted within the European Union’s Horizon Europe Framework Programme under grant agreement No 101070596 (euROBIN). 

## References

Zanella, R., Palli, G., Stramigioli, S., and Califano, F., 2024. Learning passive policies with virtual energy tanks in robotics. *IET Control Theory & Applications*, 18(5), pp.541-550.  
