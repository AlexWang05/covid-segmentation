## Work Instructions
- Run *Infer_nnUNet.py* to segment data (provide path & segmentation model path)
    - ```python Infer_nnUNet.py infer --data_folder "/home/claire/data/nifti/COVID_nifti" --model_folder "/home/alex/nnunet_runs/500"```
- Run or make object of **ResultChecker.py** object to compare results, generate and print statistics

## File Descriptions
*DataParser.py*
- Reads annotated CSV & turns into Python data
- Format: dictionary --> key = subject ID, val = [all lesion slices]

*Infer_nnUNet.py*
- Segments provided data & saves result to *./segmented_output*

*SegmentationParser.py*
- Reads segmented results (from *./segmentation_output*) & turns into Python data
- Format: dictionary --> key = subject ID, val = [all lesion slices]

*Resultchecker.py*
- Generate statistics given segmented results in comparison with annotated CSV
- Use method print_stats()

*LungMask_nnUNet.py*
- Use lung mask segmentation to pass in lobe segmentation results to nnU-Net