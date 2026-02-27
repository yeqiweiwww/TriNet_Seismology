
import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import random
import sys
from copy import deepcopy

from testset_rebuild_utils import read_seis_file, rebuild_seis_time_data, rebuild_seis_data_norm, get_rebuild_all_data, testset_add_noise, testset_sta_add, testset_sta_remove, testset_sta_mid, write_rebuild_data, vel_base, get_modify_model_data, draw_rebuild_data
from testset_rebuild_paraconfig import testset_type, testset_fresh_seis_data_dir, testset_ref_seis_rebuild_data_dir, path_para_info, reduction_v_para, rebuild_time_len_para, cut_time_start_time_para, cut_time_windows_para, move_time_window_all_range_para, move_time_window_each_range_para, draw_depth_para, sigma_value_para, mean_value_para, use_sta_num_para, spe_sta_loc_para


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



    print(i)


    if testset_type == 'noiseadd':


        testset_fresh_seis_data_path = testset_fresh_seis_data_dir[0] + '/vp_seis' + t_echo + '.dat'

        fresh_seis_time, fresh_seis_data, _ = read_seis_file(testset_fresh_seis_data_path)



        rebuild_time_len = deepcopy(rebuild_time_len_para)
        cut_time_start_time = deepcopy(cut_time_start_time_para)
        cut_time_windows = deepcopy(cut_time_windows_para)    
        move_time_window_all_range = deepcopy(move_time_window_all_range_para)
        move_time_window_each_range = deepcopy(move_time_window_each_range_para)
        processed_time = deepcopy(fresh_seis_time)
        processed_seis_data = deepcopy(fresh_seis_data)

        fresh_rebuild_seis_data, fresh_rebuild_time_data, rebuild_index, move_time_window_each, move_time_window_all = rebuild_seis_time_data(processed_time, processed_seis_data, cut_time_start_time, cut_time_windows, rebuild_time_len, move_time_window_all_range, move_time_window_each_range)

        fresh_rebuild_seis_data = rebuild_seis_data_norm(fresh_rebuild_seis_data)



        testset_ref_seis_rebuild_data_path = testset_ref_seis_rebuild_data_dir[0] + '/rebuild_vp_seis' + t_echo + '.dat'

        testset_ref_dic = get_rebuild_all_data(testset_ref_seis_rebuild_data_path)

        sigma_value = deepcopy(sigma_value_para)
        mean_value = deepcopy(mean_value_para)

        rebuild_seis_data, sta_noise_mean, sta_noise_sigma, add_noise_region_move_range_each = testset_add_noise(testset_ref_dic['use_index'], fresh_rebuild_seis_data, sigma_value, mean_value)

        rebuild_seis_data = deepcopy(rebuild_seis_data)
        rebuild_time_data = deepcopy(testset_ref_dic['pro_time'])
        locdata = deepcopy(testset_ref_dic['sta_location'])
        rebuild_index = deepcopy(testset_ref_dic['rebuild_index'])
        use_index = deepcopy(testset_ref_dic['use_index'])
        rebuild_locdata = deepcopy(testset_ref_dic['rebuild_locdata'])
        cut_time_start_time = deepcopy(testset_ref_dic['cut_start_time'])
        cut_time_windows = deepcopy(testset_ref_dic['cut_windows'])
        move_time_window_each = deepcopy(testset_ref_dic['move_time_window'])
        move_time_window_all = deepcopy(testset_ref_dic['move_time_window_all'])
        reduction_v_para = deepcopy(testset_ref_dic['reduction_v'])
        sta_noise_mean = deepcopy(sta_noise_mean)
        sta_noise_sigma = deepcopy(sta_noise_sigma)
        add_noise_region_move_range_each = deepcopy(add_noise_region_move_range_each)



    if testset_type == 'staadd':


        testset_fresh_seis_data_path = testset_fresh_seis_data_dir[0] + '/vp_seis' + t_echo + '.dat'

        fresh_seis_time, fresh_seis_data, _ = read_seis_file(testset_fresh_seis_data_path)



        rebuild_time_len = deepcopy(rebuild_time_len_para)
        cut_time_start_time = deepcopy(cut_time_start_time_para)
        cut_time_windows = deepcopy(cut_time_windows_para)    
        move_time_window_all_range = deepcopy(move_time_window_all_range_para)
        move_time_window_each_range = deepcopy(move_time_window_each_range_para)
        processed_time = deepcopy(fresh_seis_time)
        processed_seis_data = deepcopy(fresh_seis_data)

        fresh_rebuild_seis_data, fresh_rebuild_time_data, rebuild_index, move_time_window_each, move_time_window_all = rebuild_seis_time_data(processed_time, processed_seis_data, cut_time_start_time, cut_time_windows, rebuild_time_len, move_time_window_all_range, move_time_window_each_range)

        fresh_rebuild_seis_data = rebuild_seis_data_norm(fresh_rebuild_seis_data)



        testset_ref_seis_rebuild_data_path = testset_ref_seis_rebuild_data_dir[0] + '/rebuild_vp_seis' + t_echo + '.dat'

        testset_ref_dic = get_rebuild_all_data(testset_ref_seis_rebuild_data_path)

        use_sta_num = deepcopy(use_sta_num_para)
        spe_sta_loc = deepcopy(spe_sta_loc_para)

        rebuild_seis_data, use_index, rebuild_locdata = testset_sta_add(fresh_rebuild_seis_data,testset_ref_dic['pro_vp_data'],testset_ref_dic['use_index'],testset_ref_dic['sta_noise_mean'],testset_ref_dic['sta_noise_sigma'],use_sta_num,testset_ref_dic['sta_location'],spe_sta_loc)

        rebuild_seis_data = deepcopy(rebuild_seis_data)
        rebuild_time_data = deepcopy(testset_ref_dic['pro_time'])
        locdata = deepcopy(testset_ref_dic['sta_location'])
        rebuild_index = deepcopy(testset_ref_dic['rebuild_index'])
        use_index = deepcopy(use_index)
        rebuild_locdata = deepcopy(rebuild_locdata)
        cut_time_start_time = deepcopy(testset_ref_dic['cut_start_time'])
        cut_time_windows = deepcopy(testset_ref_dic['cut_windows'])
        move_time_window_each = deepcopy(testset_ref_dic['move_time_window'])
        move_time_window_all = deepcopy(testset_ref_dic['move_time_window_all'])
        reduction_v_para = deepcopy(testset_ref_dic['reduction_v'])
        sta_noise_mean = deepcopy(testset_ref_dic['sta_noise_mean'])
        sta_noise_sigma = deepcopy(testset_ref_dic['sta_noise_sigma'])
        add_noise_region_move_range_each = deepcopy(testset_ref_dic['add_noise_region_move_range'])

    if testset_type == 'staremove':
        testset_ref_seis_rebuild_data_path = testset_ref_seis_rebuild_data_dir[0] + '/rebuild_vp_seis' + t_echo + '.dat'

        testset_ref_dic = get_rebuild_all_data(testset_ref_seis_rebuild_data_path)

        use_sta_num = deepcopy(use_sta_num_para)
        spe_sta_loc = deepcopy(spe_sta_loc_para)

        rebuild_seis_data, use_index, rebuild_locdata = testset_sta_remove(testset_ref_dic['pro_vp_data'],testset_ref_dic['use_index'],use_sta_num,testset_ref_dic['sta_location'],spe_sta_loc)

        rebuild_seis_data = deepcopy(rebuild_seis_data)
        rebuild_time_data = deepcopy(testset_ref_dic['pro_time'])
        locdata = deepcopy(testset_ref_dic['sta_location'])
        rebuild_index = deepcopy(testset_ref_dic['rebuild_index'])
        use_index = deepcopy(use_index)
        rebuild_locdata = deepcopy(rebuild_locdata)
        cut_time_start_time = deepcopy(testset_ref_dic['cut_start_time'])
        cut_time_windows = deepcopy(testset_ref_dic['cut_windows'])
        move_time_window_each = deepcopy(testset_ref_dic['move_time_window'])
        move_time_window_all = deepcopy(testset_ref_dic['move_time_window_all'])
        reduction_v_para = deepcopy(testset_ref_dic['reduction_v'])
        sta_noise_mean = deepcopy(testset_ref_dic['sta_noise_mean'])
        sta_noise_sigma = deepcopy(testset_ref_dic['sta_noise_sigma'])
        add_noise_region_move_range_each = deepcopy(testset_ref_dic['add_noise_region_move_range'])

    if testset_type == 'stamid':
        testset_ref_rebuild_data_path_less = testset_ref_seis_rebuild_data_dir[0] + '/rebuild_vp_seis' + t_echo + '.dat'
        testset_ref_rebuild_data_path_more = testset_ref_seis_rebuild_data_dir[1] + '/rebuild_vp_seis' + t_echo + '.dat'

        testset_ref_dic_less = get_rebuild_all_data(testset_ref_rebuild_data_path_less)
        testset_ref_dic_more = get_rebuild_all_data(testset_ref_rebuild_data_path_more)

        use_sta_num = deepcopy(use_sta_num_para)
        spe_sta_loc = deepcopy(spe_sta_loc_para)

        rebuild_seis_data, use_index, rebuild_locdata = testset_sta_mid(testset_ref_dic_more['pro_vp_data'],testset_ref_dic_less['use_index'],testset_ref_dic_more['use_index'],use_sta_num,testset_ref_dic_more['sta_location'],spe_sta_loc)

        rebuild_seis_data = deepcopy(rebuild_seis_data)
        rebuild_time_data = deepcopy(testset_ref_dic_more['pro_time'])
        locdata = deepcopy(testset_ref_dic_more['sta_location'])
        rebuild_index = deepcopy(testset_ref_dic_more['rebuild_index'])
        use_index = deepcopy(use_index)
        rebuild_locdata = deepcopy(rebuild_locdata)
        cut_time_start_time = deepcopy(testset_ref_dic_more['cut_start_time'])
        cut_time_windows = deepcopy(testset_ref_dic_more['cut_windows'])
        move_time_window_each = deepcopy(testset_ref_dic_more['move_time_window'])
        move_time_window_all = deepcopy(testset_ref_dic_more['move_time_window_all'])
        reduction_v_para = deepcopy(testset_ref_dic_more['reduction_v'])
        sta_noise_mean = deepcopy(testset_ref_dic_more['sta_noise_mean'])
        sta_noise_sigma = deepcopy(testset_ref_dic_more['sta_noise_sigma'])
        add_noise_region_move_range_each = deepcopy(testset_ref_dic_more['add_noise_region_move_range'])


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
    modify_model_path = path_para_info['modified_modelfile']+'/modify_model'+t_echo+'.dat'
    modify_model_dic = vel_base(modify_model_path)


    pic_path = path_para_info['show_dic_path'] + '/show_vp_seis' + t_echo + '.svg'
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
