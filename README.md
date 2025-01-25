# RL-pendulum: Passive Control Policy for Simple Pendulum

This repository contains the implementation of a passively learned policy for controlling a simple pendulum using a microcontroller. The project combines reinforcement learning techniques with the concept of virtual energy tanks to ensure system passivity.

## Project Overview

This research investigates the implementation of a passively learned policy for controlling a simple pendulum on a microcontroller. The policy was trained within a reinforcement learning framework and then implemented on a physical device to evaluate its real-world performance.

### Key Features

- Two-stage reinforcement learning training process
- Implementation of virtual energy tanks for passivity
- Microcontroller-based physical implementation
- Comparison between simulation and real-world results

## Methodology

for this section take a look to the report

### Training Process

1. **Initial Training**: The system was trained with unlimited energy to determine the energy required for the control task.
2. **Limited Energy Training**: A second training phase was performed with limited energy using the concept of a virtual energy tank to ensure the system's passivity.

### Physical Implementation

- Developed a physical device based on a microcontroller
- Configured to control a permanent magnet DC motor
- Implemented encoder reading functionality
- Integrated the learned policy inference

## Installation

To set up this project, follow these steps:

1. Clone the repository: git clone https://github.com/100nze/RL-pendulum.git
2. Navigate to the project directory: cd RL-pendulum/simulation and training
2. Run: pip install -e .
3. Install the required dependencies: use "pip install -r requirements.txt" or "conda env create -f environment.yml"
## Usage
#### Training of the model
   Inside simulation and training/files/ you will find the following python scripts:
   - Environment.py : This script defines the environment used for training, following the Gymnasium framework. It models the pendulum's dynamics and energy constraints. When initializing the class, we can specify the energy limit to initialize the system, the number of steps per episode, and the threshold for terminating the episode.
   - Load.py : allows the user to load some trained and saved models seeing graphically how they perform. It gives also the possibility to acqure data of the inference on Tensorboard.
   - Train.py :  does the training of the model using SAC in its default configuration giving the possibility to monitor some resultso on Tensorboard. 
   - OnnxConv3.py : is used, once the model has been trained, to export it in .onnx format for the following steps.

If you want to know more about the implementation of the environment watch the report pdf.
##### Inference on microcontroller
   The ESP_implementation directory contains code for deploying the trained models on a microcontroller. It includes two subfolders for models trained with unlimited and limited energy. Both subfolders share the same structure with folders such as tflite-model/, model-parameters/ andedge-impulse-sdk/ all obtained by uploading the .onnx model into Edge impulse site.
    The main folder contains custom code for integrating the models with the microcontroller's hardware. Modify only this folder to avoid disrupting configurations. 
    Python scripts are also provided for collecting sensor data via the serial port and plotting them.
## Contact

For any questions or feedback, please open an issue in the GitHub repository or write to the e-mail in the first page of the report.


## Acknowledgements

This work has received funding from the European Union’s Horizon Europe Framework Programme under grant agreement No 101070596 (euROBIN).
