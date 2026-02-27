

import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import random
import sys

from rebuild_utils import *
from rebuild_paraconfig import *

# mkdir(path_para_info['rebuild_seis_data_dir'])
# mkdir(path_para_info['seis_dat_dic_path'])
# mkdir(path_para_info['show_dic_path'])


# tzfiles = os.listdir(path_para_info['tzfile_dic_path_dir'])
files_list_f = open(sys.argv[1],'r')
tzfiles_temp = files_list_f.readlines()
files_list_f.close()

tzfiles = tzfiles_temp[0].replace('\n','').split(',')[:-1]
print(len(tzfiles))
print(tzfiles)

ttt = sys.argv[2]+'_'

for i in range(len(tzfiles)):
    t_echo = tzfiles[i].replace('seis_','_').split('.')[0]
    modified_inputfile_path = deepcopy(path_para_info['modified_inputfile']) + '/modify_inputfile' + t_echo + '.inp'

    # model_path = deepcopy(path_para_info['modify_npz_file_path_dir']) + '/modify_nd_file' + t_echo + '.npz'

    pro_seis = process_seismic_data(modified_inputfile_path, reduction_v=reduction_v_para, input_para_dic=input_para_dic)
    pro_seis.read_file(deepcopy(path_para_info['tzfile_dic_path_dir']) + '/' + tzfiles[i])
    pro_seis.get_data()
    pro_seis.reduction_velocity()
    # pro_seis.align_phase_wave(model_path = model_path, phase_list = ['p','pP','P','sP','SP','PcP','ScP'])
    p_apsd = pro_seis.opapsd(deepcopy(path_para_info['seis_dat_dic_path']) + '/vp_seis' + t_echo + '.dat')

    print(i)



    input_content = read_inputfile(deepcopy(path_para_info['modified_inputfile']) + '/modify_inputfile' + t_echo + '.inp')

    locnum_lin = deepcopy(input_para_dic['locnum_lin'])
    locdata_lin = deepcopy(input_para_dic['locdata_lin'])

    locnum = int(input_content[locnum_lin].split()[0])
    locdata = []
    for j in range(locnum):
        locdata.append(float(input_content[locdata_lin].split()[j]))


    rebuild_time_len = deepcopy(rebuild_time_len_para)
    cut_time_start_time = deepcopy(cut_time_start_time_para)
    cut_time_windows = deepcopy(cut_time_windows_para)    
    move_time_window_all_range = deepcopy(move_time_window_all_range_para)
    move_time_window_each_range = deepcopy(move_time_window_each_range_para)
    processed_time, processed_seis_data = deepcopy(p_apsd['reduction_time_data']), deepcopy(p_apsd['seis_data'])
    rebuild_seis_data, rebuild_time_data, rebuild_index, move_time_window_each, move_time_window_all = rebuild_seis_time_data(processed_time, processed_seis_data, cut_time_start_time, cut_time_windows, rebuild_time_len, move_time_window_all_range, move_time_window_each_range)



    rebuild_seis_data = rebuild_seis_data_norm(rebuild_seis_data)


    add_noise_or_not = deepcopy(add_noise_or_not_para)
    mean_value = deepcopy(mean_value_para)
    sigma_value = deepcopy(sigma_value_para)

    rebuild_seis_data, sta_noise_mean, sta_noise_sigma, add_noise_region_move_range_each = add_noise_v2(rebuild_seis_data, sigma_value, mean_value, add_noise_or_not)

    if add_noise_or_not: 

        rebuild_seis_data = rebuild_seis_data_norm(rebuild_seis_data)


    random_sta_or_not = deepcopy(random_sta_or_not_para)
    use_sta_num = deepcopy(use_sta_num_para)

    rebuild_seis_data, use_index = change_use_index_v2(rebuild_seis_data, use_sta_num, use_or_not=random_sta_or_not)


    spe_sta = deepcopy(spe_sta_loc_para)

    rebuild_locdata = rebuild_sta_location(locdata, spe_sta, use_index, random_sta_or_not)



    rebuild_data_path = path_para_info['rebuild_seis_data_dir'] + '/rebuild_vp_seis'+t_echo+'.dat'
    write_rebuild_data(
        rebuild_data_path,
        rebuild_seis_data, 
        rebuild_time_data, 
        locdata, 
        rebuild_index, 
        use_index, 
        rebuild_locdata,
        cut_time_start_time, 
        cut_time_windows, 
        move_time_window_each,
        move_time_window_all,
        reduction_v_para,
        sta_noise_mean,
        sta_noise_sigma,
        add_noise_region_move_range_each,
    )

    vel_base_dic = vel_base('./vel_base_model.dat')
    modify_model_path = './modified_modelfile/modify_model'+t_echo+'.dat'
    modify_model_dic = vel_base(modify_model_path)


    pic_path = path_para_info['show_dic_path'] + '/show_vp_seis' + t_echo
    draw_rebuild_data(
    vel_base_dic,
    modify_model_dic,
    locdata,
    rebuild_seis_data,
    rebuild_time_data,
    use_index,
    cut_time_start_time,
    cut_time_windows,
    pic_path,
    draw_depth_para=draw_depth_para,
    reduction_v=reduction_v_para,
    )

f = open('./logging.dat','a')
f.write(ttt+'done\n')
f.close()
