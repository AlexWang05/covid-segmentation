from DataParser import DataParser
from SegmentationParser import SegmentationParser
from tqdm import tqdm
import os
import nibabel as nib

'''
Generate statistics given segmented results in comparison with annotated CSV
'''
class ResultChecker:
    def __init__(self, annotated_file_name='annotated.csv', raw_data_path='/home/claire/data/nifti/COVID_nifti', segmentation_folder='./segmented_output'):
        self.file_name = annotated_file_name
        self.raw_data_path = raw_data_path
        self.input_folder = segmentation_folder

    def generate_stats(self):
        # RAW_DATA_PATH = '/home/claire/data/nifti/COVID_nifti'
        # RAW_DATA_PATH = '/home/alex/MIP_out/two_COVID_nifti'

        data_parser = DataParser(self.file_name)
        segmentation_parser = SegmentationParser(self.input_folder)

        print('Began getting CSV slice data')
        csv_data = data_parser.get_slice_data()
        print('Finished getting CSV slice data')

        print('Began getting segmented slice data')
        segmented_data = segmentation_parser.get_slice_data()
        print('Finished getting segmented slice data')
        
        accuracy = []  # total correct / all
        precision = []  # true positive / (true positive + false positive)
        sensitivity_recall = []  # true positive / (true positive + false negative) , also sensitivity
        specificity = []  # true negative / (true negative + false positive)

        print('Computing Statistics')
        for subject_id in tqdm(csv_data):
            # TEST
            # subject_id = '5M9RRKD5'
            # print('BEFORE: ', subject_id)
            # subject_id = subject_id.strip('.nii.gz')
            # print('AFTER: ', subject_id)

            true_positive = 0
            false_positive = 0
            false_negative = 0
            # print(csv_data[subject_id])
            # print('\n\nSEGMENTED: ' + str(segmented_data[subject_id]))
            
            # get true negative (raw segmentation slice num)

            # raw_img = nib.load(os.path.join(RAW_DATA_PATH, subject_id, subject_id + '.nii.gz')) # covid data
            raw_img = nib.load(os.path.join(self.raw_data_path, subject_id + '.nii.gz'))
            data = raw_img.get_fdata()
            ct_count = data.shape[2]

            print("\n\nSEGMENTED DATA KEYS: ", segmented_data.keys())
            print('SUBJECT ID: ', subject_id)

            # iterate through subject's slices
            for slice_num in csv_data[subject_id]:
                # only necessary for cottage PNA
                subject_full = subject_id + '.nii.gz'

                # check if slice num also present in segmented output (true positive)
                # if slice_num in segmented_data[subject_id + '.nii.gz']:
                if slice_num in segmented_data[subject_full]:
                    true_positive += 1
                else:  # false negative
                    false_negative += 1

            # check for false positive
            # for slice_num in segmented_data[subject_id]:
            for slice_num in segmented_data[subject_full]:
                if slice_num not in csv_data[subject_id]:
                    false_positive += 1

            true_negative = ct_count - (true_positive + false_positive + false_negative)

            accuracy.append((true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative))
            precision.append(true_positive / (true_positive + false_positive))
            sensitivity_recall.append(true_positive / (true_positive + false_negative))
            specificity.append(true_negative / (true_negative + false_positive))

            # DELETE THIS LATER
            # print('\n\nSUBJECT ID: ', subject_id)
            # print('1 ACCURACY: ', accuracy[0])
            # print('1 PRECISION: ', precision[0])
            # print('1 SENSITIVITY: ', sensitivity_recall[0])
            # print('1 SPECIFICITY: ', specificity[0])
            
            # print(f'CT Count: {ct_count}, TP: {true_positive}, TN: {true_negative}, FP: {false_positive}, FN: {false_negative}')

            # print('\n\nCSV: ', csv_data[subject_id])
            # print('\n\nMODEL: ', segmented_data[subject_id])
            # return
            
        return accuracy, precision, sensitivity_recall, specificity

    
    def print_stats(self):
        accuracy, precision, sensitivity_recall, specificity = self.generate_stats()
        avg_accuracy = self.get_average(accuracy)
        avg_precision = self.get_average(precision)
        avg_sensitivity_recall = self.get_average(sensitivity_recall)
        avg_specificity = self.get_average(specificity)

        print('AVERAGE ACCURACY: ', avg_accuracy)
        print('AVERAGE PRECISION: ', avg_precision)
        print('AVERAGE SENSITIVITY/RECALL: ', avg_sensitivity_recall)
        print('AVERAGE SPECIFICITY: ', avg_specificity)


    def get_average(self, list):
        return sum(list) / len(list)


if __name__ == '__main__':
    # checker = ResultChecker()  # check raw segmentation
    # checker = ResultChecker('annotated.csv', '/home/alex/MIP_out/COVID_nifti')  # check lung mask postprocessing
    # checker = ResultChecker('annotated.csv', '/home/alex/CottageWork/two_segmented_MIP')
    # checker = ResultChecker('annotated.csv', './unet_segmented_output')

    # check PNA
    checker = ResultChecker('annotated_pna.csv', '/home/claire/data/nifti/PNA_nifti', '/home/alex/CottageWork/PNA_postprocessing')

    checker.print_stats()