import os
from models.throw import Throw
from datetime import  datetime



class Data_Writer:
    def __init__(self):
        self.data_folder = None
        self.data_file = None

    def create_data_file(self, data_folder_name, file_name=None, header=None):
        self.data_folder = os.getcwd() + "//data//" + data_folder_name + '// '

        if file_name is None:
            file_name = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
        self.data_file = file_name + ".csv"

        if not os.path.exists(self.data_folder + self.data_file):
            # Write the header for the incoming data
            self.write_data(header if header is not None else Throw.get_data_format())

    def write_data(self, to_write):
        with open(self.data_folder + self.data_file, 'a') as data:
            data.write(to_write + "\n")
