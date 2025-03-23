## Synopsis
This repo stores partial artifacts of training nnU-Net and U-Net-based models for the robust segmentation of COVID-19 lesions in lung CT scans. The repo contains training scripts, checkpoints, and additional scripts for maximum intensity projection, lung lobe segmentation extraction, and result checking using a dataset from the Santa Barbara Cottage Hospital.

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

# Cottage Scripts, Lung Lobe Processing, and Post Processing
Located in ```./CottageWork```
Documentation below can also be found as a README.md in ```./CottageWork```

## Work Instructions
- Use *LungLobeProcessing.py* to add lung lobe segmentation results to raw data
    - Input raw data dimensions: (x, y, num_slices)
    - Output NIFTI file dimensions: (x, y, num_slices, 7) 
- Run *Infer_nnUNet.py* to segment data (provide path & segmentation model path)
    - ```python Infer_nnUNet.py infer --data_folder "/home/claire/data/nifti/COVID_nifti" --model_folder "/home/alex/nnunet_runs/500"```
- Compare segmentation results with CSV-saved data, generate and print statistics
    - Complete with ```ResultChecker.py```, which uses *SegmentationParser.py* and *DataParser.py*
- Postprocessing with ```PostProcessing.py``` - improve accuracy and metrics by applying Lung Mask
    - Make *PostProcessing* object with desired segmentation folder, raw unsegmented data folder, and postprocessing output folder, or run ```PostProcessing.py``` for default parameters

Note: most scripts include GPU selection code; please modify accordingly.

## File Descriptions
*DataParser.py*
- Reads annotated CSV & turns into Python data
- Format: dictionary --> key = subject ID, val = [all lesion slices]

*Infer_unet.py*
- Segments provided data & saves result to *./unet_segmented_output*
- Default parameters uses 300 epoch U-Net model

*Infer_nnUNet.py*
- Segments provided data with 500 epoch nnU-Net model

*SegmentationParser.py*
- Reads segmented results (from *./segmentation_output*) & turns into Python data
- Format: dictionary --> key = subject ID, val = [all lesion slices]

*Resultchecker.py*
- Generate statistics given segmented results in comparison with annotated CSV
- Use method print_stats()

*LungLobeProcessing.py*
- Adds lobe segmentation to 3D NIFTI raw data in form of one-hot encoding
- Output dimension: (x, y, num_slices, 7)
- Provide raw data folder and output folder; defaults in script


*PostProcessing.py*
- Iterate through input files and generates output of processed files in the same format
- If facing errors --> copy segmented results into output folder and let the script override the initial files
