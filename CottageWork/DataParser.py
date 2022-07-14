import csv
from tqdm import tqdm

'''
Read CSV of subjects with annotated data
Can get data in form of dictionary (key=ID, val=[all checked slices])
'''
class DataParser:
    def __init__(self, file_name='annotated.csv'):
        self.file_name = file_name

    '''
    Gets the first row of the CSV (containing IDs as strings)
    '''
    def get_first_row(self):
        with open(self.file_name, 'r') as file:
            reader = csv.reader(file)
            return next(reader)

    '''
    Read CSV data and append all checked slices to subject dictionary
    Dictionary: key=subjectIDs (str), val=[all checked nums] (1D list)
    '''
    def get_slice_data(self):
        subject_dict = {}
        first_row = self.get_first_row()

        with open(self.file_name, 'r') as file:
            reader = csv.reader(file)
            
            # skip first row
            next(reader)
        
            # loop through the rest of the cells
            for row in tqdm(reader):
                for counter, cell in enumerate(row):
                    # if cell checked --> append to list
                    if cell == 'X':
                        slice_num = row[0]
                        
                        # get subject ID
                        subject_id = first_row[counter]

                        # add if not in dict
                        if subject_id not in subject_dict:
                            subject_dict[subject_id] = []
                        
                        # append slice num
                        subject_dict[subject_id].append(int(slice_num))
                    
        return subject_dict

if __name__ == '__main__':
    print('running DataParser.py')
    # parser = DataParser()
    # print(parser.get_slice_data())