import os
from lungmask import mask
import SimpleITK as sitk
import nibabel as nib
from tqdm import tqdm
import numpy as np

'''
Add lobe segmentation to 3D NIFTI raw data in form of one-hot encoding
'''
class LungLobeProcessing:
    def __init__(self, raw_folder='/home/claire/data/nifti/COVID_nifti', out_folder='/home/alex/CottageWork/lobe_output'):
        self.raw_folder = raw_folder
        self.out_folder = out_folder
    
    '''
    Gets the lung lobe mask given the subject ID
    '''
    def get_lung_mask(self, subject_id):
        image_dir = os.path.join(self.raw_folder, subject_id)
        img = sitk.ReadImage(image_dir, imageIO='NiftiImageIO')
        model = mask.get_model('unet', 'LTRCLobes')

        segmentation = mask.apply(img, model)

        return segmentation
    
    '''
    Apply lung lobe segmentation processing to generate output
    '''
    def apply(self):
        # loop through raw files
        for subject_id in tqdm(os.listdir(self.raw_folder)):
            img = nib.load(os.path.join(self.raw_folder, subject_id))
            data = img.get_fdata()

            # shape for both = [num_slices, 512, 512]
            data = np.swapaxes(data, 0, 2)  # num slices first, values are intensity
            lung_mask = self.get_lung_mask(subject_id)  # values [0, 1, ..., 5], 0 background, 1-5 lobes

            # new approach - build empty new data and add values
            shape = list(data.shape)
            shape.append(7)
            new_data = np.empty(shape)  # (num_slices, 512, 512, 7)

            for slice_num in range(len(lung_mask)):
                for i in range(len(lung_mask[slice_num])):
                    for j in range(len(lung_mask[slice_num][i])):
                        # each voxel
                        one_hot = self.to_one_hot(lung_mask[slice_num][i][j])
                        voxel_val = [data[slice_num][i][j]] + one_hot  # [orignal_intensity, one-hot vector]

                        # set val to voxel
                        new_data[slice_num][i][j] = voxel_val
            
            # swap back to original form
            new_data = np.swapaxes(new_data, 0, 2)

            # save in new folder
            out_dir = os.path.join(self.out_folder, subject_id)

            save_img = nib.Nifti1Image(new_data, affine=np.eye(4))
            nib.save(save_img, out_dir)
            print("FILE WRITTEN at " + out_dir)

    '''
    Given lobe number (0-5), return one-hot encoded list
    ex. 5 --> [0, 0, 0, 0, 0, 1], 0 --> [1, 0, 0, 0, 0, 0]
    '''
    def to_one_hot(self, lobe_num):
        vect = [0, 0, 0, 0, 0, 0]
        
        try:
            vect[lobe_num] = 1
        except IndexError:
            raise Exception('Lobe index too large. Could not process in to_one_hot()')
            
        return vect


if __name__ == '__main__':
    processor = LungLobeProcessing()    
    processor.apply()