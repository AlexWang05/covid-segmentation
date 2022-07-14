import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from tqdm import tqdm

'''
Reads segmented results, convert to Python format
Format: dictionary (key=subject ID, val=[all lesion slices])
'''
class SegmentationParser:
    def __init__(self, input_folder='./segmented_output'):
        self.input_folder = input_folder

    '''
    get dictionary of all subject results from segmentation
    '''
    def get_slice_data(self):
        subject_dict = {}
        
        # open segmentation folder, loop through all subjects
        for subject_id in tqdm(os.listdir(self.input_folder)):
            lesions = []
            
            # load segmented mask
            img = nib.load(os.path.join(self.input_folder, subject_id, subject_id + '_seg.nii.gz'))
            data = img.get_fdata()
            
            # print('SUBJECT ID: ', subject_id)
            # print('MASK SHAPE: ', data.shape)  # shape=(512, 512, x)
            # print(np.unique(data))  # [0, 1]

            data = np.swapaxes(data, 0, 2)  # 3rd dim first for iteration
            # print('NEW SHAPE: ', data.shape)  # shape=(x, 512, 512)
            
            num_slices = data.shape[0]

            # iterate through all slices, slice.shape = (512, 512)
            for counter, slice in enumerate(data):
                has_lesion = self.check_lesion(slice)

                # add present lesion nums
                if (has_lesion):
                    # 3rd dimension in shape STARTS at first nonempty
                    # MAKE SURE --> start at nonempty and decreases in num
                    lesions.append(counter + 1)

            subject_dict[subject_id] = lesions
    
        return subject_dict

    
    '''
    Loops through a 2D slice and checks if lesion is present
    '''
    def check_lesion(self, slice):
        for i in slice:
            for j in i:
                if (j == 1):
                    return True

        return False


if __name__ == '__main__':
    parser = SegmentationParser()
    print(parser.get_slice_data())