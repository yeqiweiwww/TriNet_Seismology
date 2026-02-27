

'''
'''

import os
from copy import deepcopy


testset_type = 'staremove' # noiseadd/staadd/staremove/stamid

datafilepath = ''

mean_value_para = None
sigma_value_para = None
use_sta_num_para = None
testset_ref_seis_rebuild_data_dir = []
testset_fresh_seis_data_dir = []
if testset_type == 'noiseadd':
    testset_ref_seis_rebuild_data_dir = [os.path.dirname(datafilepath) + '/rebuild_seis_data' + '/seis_rebuild_data']
    testset_fresh_seis_data_dir = [os.path.dirname(datafilepath) + '/rebuild_seis_data' + '/seis_dat']
    # add noise
    mean_value_para = 0
    sigma_value_para = 0.15
if testset_type == 'staadd':
    testset_ref_seis_rebuild_data_dir = [os.path.dirname(datafilepath) + '/rebuild_seis_data' + '/seis_rebuild_data']
    testset_fresh_seis_data_dir = [os.path.dirname(datafilepath) + '/rebuild_seis_data' + '/seis_dat']
    # sta num
    use_sta_num_para = 39
if testset_type == 'staremove':
    testset_ref_seis_rebuild_data_dir = ['./seis_rebuild_data']
    # sta num
    use_sta_num_para = 31
if testset_type == 'stamid':# less/more
    testset_ref_seis_rebuild_data_dir = [os.path.dirname(datafilepath) + '/rebuild_seis_data' + '/seis_rebuild_data', os.path.dirname(datafilepath) + '/rebuild_seis_data_testset_more' + '/seis_rebuild_data']
    # sta num
    use_sta_num_para = 33

# path

path_para_info = {
    'modified_inputfile' : './modified_inputfile',
    'modified_modelfile' : './modified_modelfile',
    'tzfile_dic_path_dir' : './modify_tzfile',
    'seis_dat_dic_path' : './seis_dat_testset',
    'rebuild_seis_data_dir' : './seis_rebuild_data_testset',
    'show_dic_path' : './show_testset',
}




reduction_v_para = 10
draw_depth_para = [400,1000]




cut_time_start_time_para = 15
cut_time_windows_para = 40
rebuild_time_len_para = cut_time_windows_para*2+1
move_time_window_all_range_para = 0
move_time_window_each_range_para = 0


spe_sta_loc_para = []
for j in range(41):
    spe_sta_loc_para.append(j*0.5+9.75)