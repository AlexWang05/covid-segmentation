## Introduction
- Saved models are saved in ```./runs``` (for U-Net) and ```./nnunet_runs``` (nnU-Net)
    - Subdirectories represent Epoch number for training
    - i.e. ```./nnunet_runs/500``` represents nnU-Net trained on 500 epochs
- Training and inference files are ```run_net.py``` (U-Net) and ```run_nnUNet.py``` (nnU-Net)
    - These models are based on MONAI and are tested with the Grand Challenge Dataset
    - Training: ```/home/s_shailja/Fall2020/COVID-19-20_v2/Train```
    - Testing: ```/home/s_shailja/Fall2020/COVID-19-20_v2/Validation```
- Evaluation & Inference scripts for Cottage Hospital Data are located in ```./CottageWork```
    - separate README located in ```./CottageWork/README.md```

## Running Instructions
- Command Line Usage
    - Modify **source file** (run_net.py / run_nnUNet.py), **data folder** (Train / Validation), **model folder** (APPEND EPOCH NUMBER; i.e. *--model_folder "runs/300"* 
    - Modify **train** or **infer**
    - ```python run_net.py train --data_folder "/home/s_shailja/Fall2020/COVID-19-20_v2/Train" --model_folder "runs"```
        - output segmentation files to ```./output```
    - GPU selection at start of script
