

'''
'''

import os
from copy import deepcopy

from rebuild_utils import read_inputfile

# path


path_para_info = {
    'modified_inputfile' : './modified_inputfile',
    'tzfile_dic_path_dir' : './modify_tzfile',
    # 'modify_npz_file_path_dir' : os.path.dirname(datafilepath)+'/modify_npz_file',
    'seis_dat_dic_path' : './seis_dat',
    'rebuild_seis_data_dir' : './seis_rebuild_data',
    'show_dic_path' : './show',
}



input_para_dic = {
    'locnum_lin' : 12,
    'locdata_lin' : 13,
    'source_depth_lin' : 5,
}

input_content = read_inputfile(deepcopy(path_para_info['modified_inputfile']) + '/' + os.listdir(deepcopy(path_para_info['modified_inputfile']))[0])

locnum_lin = deepcopy(input_para_dic['locnum_lin'])
locdata_lin = deepcopy(input_para_dic['locdata_lin'])

locnum = int(input_content[locnum_lin].split()[0])



reduction_v_para = 10
draw_depth_para = [400,1000]




cut_time_start_time_para = 15
cut_time_windows_para = 40
rebuild_time_len_para = cut_time_windows_para*2+1
move_time_window_all_range_para = 0
move_time_window_each_range_para = 0



add_noise_or_not_para = False

mean_value_para = 0
sigma_value_para = 0.15


random_sta_or_not_para = False
use_sta_num_para = 31



spe_sta_loc_para = []
for j in range(41):
    spe_sta_loc_para.append(j*0.5+9.75)