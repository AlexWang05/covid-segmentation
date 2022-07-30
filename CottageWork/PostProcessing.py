import os
from lungmask import mask
import SimpleITK as sitk  # currently running 2.0.2
import numpy as np
import nibabel as nib
from tqdm import tqdm
# clear cache, prevent memory error
import torch
import gc
torch.cuda.empty_cache()

'''
Take segmented output and post-process to include only results in lung mask
'''
class PostProcessing:
    def __init__(self, seg_folder='./segmented_output', raw_folder='/home/claire/data/nifti/COVID_nifti', out_folder='/home/alex/CottageWork/postprocessing_output'):
        self.seg_folder = seg_folder
        self.raw_folder = raw_folder
        self.out_folder = out_folder

    '''
    Gets the lung mask given subject ID
    '''
    def get_lung_mask(self, subject_id):
        image_dir = os.path.join(self.raw_folder, subject_id + '.nii.gz')
        img = sitk.ReadImage(image_dir, imageIO='NiftiImageIO')

        segmentation = mask.apply(img)

        # [0, 1, 2] - background, left, right
        # print(np.unique(segmentation))
        return segmentation

    '''
    Apply post processing lung mask to generate masked output
    '''
    def apply(self):
        # loop through segmented files
        for subject_id in tqdm(os.listdir(self.seg_folder)):
            img = nib.load(os.path.join(self.seg_folder, subject_id, subject_id + '_seg.nii.gz'))
            data = img.get_fdata()

            # shape for both = [num_slices, 512, 512]
            data = np.swapaxes(data, 0, 2)  # num slices first
            lung_mask = self.get_lung_mask(subject_id)

            # iterate through both --> check if voxel is within lung mask
            for counter, (segmented, mask) in enumerate(zip(data, lung_mask)):
                # print(segmented.shape, mask.shape)
                # (512, 512)  (512, 512)

                # loop thru each pixel in data
                # if not within mask --> set to 0
                for i in range(len(segmented)):
                    for j in range(len(segmented[i])):
                        if (segmented[i][j] == 1 and mask[i][j] == 0):
                            data[counter][i][j] = 0

            data = np.swapaxes(data, 0, 2)  # back in original shape

            # save in new folder
            out_dir = os.path.join(self.out_folder, subject_id, subject_id + '_seg.nii.gz')
            out_dir = os.path.join(self.out_folder, subject_id + '.nii.gz')

            save_img = nib.Nifti1Image(data, affine=np.eye(4))
            nib.save(save_img, out_dir)
            print("FILE WRITTEN at " + out_dir)

            torch.cuda.empty_cache()
            gc.collect()

if __name__ == '__main__':
    # processor = PostProcessing()
    # processor = PostProcessing('../inference_outputs/nnUNet_500', "/home/s_shailja/Fall2020/COVID-19-20_v2/Validation", '/home/alex/inference_postprocessing')
    processor = PostProcessing('/home/claire/data/segmented2/PNA', '/home/claire/data/nifti/PNA_nifti', './PNA_postprocessing')
    processor.apply()