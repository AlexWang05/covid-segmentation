import os
import nibabel as nib
from tqdm import tqdm
import numpy as np

'''
Process raw data through max intensity projection
for each slice k, intensity is max(k-1, k, k+1)
'''
class MaxIntensityProjector:
    def __init__(self, data_folder='/home/claire/data/nifti/COVID_nifti', out_folder='/home/alex/MIP_out'):
        self.data_folder = data_folder
        self.out_folder = out_folder

    '''
    Set each slice's intensity k to max of (k-1, k, k+1) 
    '''
    def process(self):
        # loop through raw files
        for subject_id in tqdm(os.listdir(self.data_folder)):
            img = nib.load(os.path.join(self.data_folder, subject_id))
            data = img.get_fdata()

            # new shape = [num_slices, 512, 512]
            data = np.swapaxes(data, 0, 2)
            num_slices = data.shape[0]

            new_data = np.empty(np.shape(data))

            for slice_num in range(len(data)):
                for i in range(len(data[slice_num])):
                    for j in range(len(data[slice_num][i])):
                        before, after = -2000, -2000
                        if slice_num > 0:
                            before = data[slice_num-1][i][j]
                        if slice_num < num_slices-1:
                            after = data[slice_num+1][i][j]
                        
                        # set to max of 3 vals
                        new_data[slice_num][i][j] = max([before, after, data[slice_num][i][j]])

            # switch back to original form
            new_data = np.swapaxes(new_data, 0, 2)

            # save in new folder
            out_dir = os.path.join(self.out_folder, subject_id)

            save_img = nib.Nifti1Image(new_data, affine=np.eye(4))
            nib.save(save_img, out_dir)
            print('FILE WRITTEN at ' + out_dir)


    def process_two(self):
        # loop through raw files
        for subject_id in tqdm(os.listdir(self.data_folder)):
            img = nib.load(os.path.join(self.data_folder, subject_id))
            data = img.get_fdata()

            # new shape = [num_slices, 512, 512]
            data = np.swapaxes(data, 0, 2)
            num_slices = data.shape[0]

            for slice_num in range(len(data)):
                for i in range(len(data[slice_num])):
                    for j in range(len(data[slice_num][i])):
                        a, b, c, d = -2000, -2000, -2000, -2000
                        if slice_num > 1:
                            a = data[slice_num-1][i][j]
                            b = data[slice_num-2][i][j]
                        if slice_num < num_slices-2:
                            c = data[slice_num+1][i][j]
                            d = data[slice_num+2][i][j]
                            
                        # set to max of 3 vals
                        data[slice_num][i][j] = max([a, b, c, d, data[slice_num][i][j]])

            # switch back to original form
            data = np.swapaxes(data, 0, 2)

            # save in new folder
            out_dir = os.path.join(self.out_folder, subject_id)

            save_img = nib.Nifti1Image(data, affine=np.eye(4))
            nib.save(save_img, out_dir)
            print('FILE WRITTEN at ' + out_dir)



if __name__ == '__main__':
    # projector = MaxIntensityProjector('/home/claire/data/nifti/COVID_nifti', '/home/alex/MIP_out/COVID_nifti')
    # projector.process()

    # k-2, k-1, k, k+1, k+2
    projector = MaxIntensityProjector('/home/claire/data/nifti/COVID_nifti', '/home/alex/MIP_out/two_COVID_nifti')
    projector.process_two()