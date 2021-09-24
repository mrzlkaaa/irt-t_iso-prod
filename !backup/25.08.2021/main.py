import os
import datetime


class PrepCals:

    def __init__(self):
        self.direc = os.getcwd()
        self.pth_burn = os.path.join(self.direc, 'input_mcu_file', 'burn')
        self.output_folder = os.path.join(self.direc, 'output_mcu')
        self.towrite_data = list()

    def open(self, path):
        with open(path, 'r', encoding='latin-1') as fl:
            return fl.readlines()
    
    def output(self, file_name):
        # print(self.towrite_data)
        set_path = os.path.join(
            self.output_folder, f'{self.inp_comp}_{datetime.date.today()}')
        if not os.path.exists(set_path):
            make_folder = os.makedirs(set_path)
        # *change working directory
        # os.chdir(set_path)
        to_save_path = os.path.join(set_path, file_name)
        print(to_save_path)
        with open(to_save_path, 'w',  encoding='latin-1') as out_matr:
            out_matr.writelines(self.towrite_data)


# if __name__ == '__main__':
#     print(help(PrepCals()))
