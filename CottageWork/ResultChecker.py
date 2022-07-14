from DataParser import DataParser
from SegmentationParser import SegmentationParser
from tqdm import tqdm

'''
Generate statistics given segmented results in comparison with annotated CSV
'''
class ResultChecker:
    def __init__(self, annotated_file_name='annotated.csv', segmentation_folder='./segmented_output'):
        self.file_name = annotated_file_name
        self.input_folder = segmentation_folder

    def generate_stats(self):
        data_parser = DataParser(self.file_name)
        segmentation_parser = SegmentationParser(self.input_folder)

        print('Began getting CSV slice data')
        csv_data = data_parser.get_slice_data()
        print('Finished getting CSV slice data')

        print('Began getting segmented slice data')
        segmented_data = segmentation_parser.get_slice_data()
        print('Finished getting segmented slice data')
        precision = []  # true positive / (true positive + false positive)
        sensitivity_recall = []  # true positive / (true positive + false negative) , also sensitivity

        print('Computing Statistics')
        for subject_id in tqdm(csv_data):
            true_positive = 0
            false_positive = 0
            false_negative = 0
            # print(csv_data[subject_id])
            # print('\n\nSEGMENTED: ' + str(segmented_data[subject_id]))
            
            # iterate through subject's slices
            for slice_num in csv_data[subject_id]:
                # check if slice num also present in segmented output (true positive)
                if slice_num in segmented_data[subject_id]:
                    true_positive += 1
                else:  # false negative
                    false_negative += 1

            # check for false positive
            for slice_num in segmented_data[subject_id]:
                if slice_num not in csv_data[subject_id]:
                    false_positive += 1

            precision.append(true_positive / (true_positive + false_positive))
            sensitivity_recall.append(true_positive / (true_positive + false_negative))
            
        return precision, sensitivity_recall

    
    def print_stats(self):
        precision, sensitivity_recall = self.generate_stats()
        avg_precision = self.get_average(precision)
        avg_sensitivity_recall = self.get_average(sensitivity_recall)

        print('AVERAGE PRECISION: ', avg_precision)
        print('AVERAGE SENSITIVITY/RECALL: ', avg_sensitivity_recall)


    def get_average(self, list):
        return sum(list) / len(list)
    

if __name__ == '__main__':
    checker = ResultChecker()
    checker.print_stats()