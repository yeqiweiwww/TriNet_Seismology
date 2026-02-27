

import os
from gen_ini_para import paths_info_dic

def mkdir(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)


mkdir(paths_info_dic['modify_dic']['modify_inputfile_path_dir'])
mkdir(paths_info_dic['modify_dic']['modify_velocity_model_path_dir'])
mkdir(paths_info_dic['modify_dic']['modify_ttfile'])
mkdir(paths_info_dic['modify_dic']['modify_tzfile'])
mkdir(paths_info_dic['modify_dic']['modify_trfile'])
mkdir(paths_info_dic['modify_dic']['modify_otherdata'])
# mkdir(paths_info_dic['modify_dic']['modify_nd_file_path_dir'])
# mkdir(paths_info_dic['modify_dic']['modify_npz_file_path_dir'])

mkdir(paths_info_dic['log_dic']['log_path_dir'])
mkdir(paths_info_dic['log_dic']['log_file_path_dir'])
mkdir(paths_info_dic['log_dic']['log_gen_dir'])