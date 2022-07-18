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