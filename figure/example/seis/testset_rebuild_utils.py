
'''
'''


import os
from copy import deepcopy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import random
from pandas.core.frame import DataFrame
from obspy.signal.filter import bandpass
from obspy.taup import TauPyModel
from scipy import signal


def mkdir(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)


def read_seis_file(path):
    file = open(path, 'r')
    file_content = file.readlines()
    file.close()

    pro_time = []
    pro_vp_data = []
    for i in range(len(file_content)-1):
        if i%2 == 0:
            pro_time.append([])
            for j in range(len(file_content[i].split())-1):
                pro_time[int(i/2)].append(float(file_content[i].split()[j+1]))
        else:
            pro_vp_data.append([])
            for j in range(len(file_content[i].split())-1):
                pro_vp_data[int(i/2-0.5)].append(float(file_content[i].split()[j+1]))

    reduction_v = float(file_content[-1].split(':')[1])

    return pro_time, pro_vp_data, reduction_v


def vel_base(path):
    file = open(path,'r')
    file_content = file.readlines()
    file.close

    data_content = file_content[1:]
    vel_base_model_temp = []
    for i in range(len(data_content)):
        vel_base_model_temp.append([])
        temp = data_content[i].split()
        for j in range(len(temp)):
            vel_base_model_temp[i].append(float(temp[j]))
    
    vel_base_model_need = DataFrame(vel_base_model_temp)

    no_vel_base_model = []; depth_vel_base_model = []; vp_vel_base_model = []; vs_vel_base_model = []; ro_vel_base_model = []; qp_vel_base_model = []; qs_vel_base_model = []
    for i in range(len(vel_base_model_need)):
        no_vel_base_model.append(int(vel_base_model_need[0][i]))
        depth_vel_base_model.append(float(vel_base_model_need[1][i]))
        vp_vel_base_model.append(float(vel_base_model_need[2][i]))
        vs_vel_base_model.append(float(vel_base_model_need[3][i]))
        ro_vel_base_model.append(float(vel_base_model_need[4][i]))
        qp_vel_base_model.append(float(vel_base_model_need[5][i]))
        qs_vel_base_model.append(float(vel_base_model_need[6][i]))

    vel_base_model_dic={
        'no' : no_vel_base_model,
        'depth' : depth_vel_base_model,
        'vp' : vp_vel_base_model,
        'vs' : vs_vel_base_model,
        'ro' : ro_vel_base_model,
        'qp' : qp_vel_base_model,
        'qs' : qs_vel_base_model,
    }

    return vel_base_model_dic


def get_modify_model_data(modify_model_path):
    file = open(modify_model_path,'r')
    file_content = file.readlines()
    file.close

    techo = os.path.basename(modify_model_path).replace('modify_model','').replace('.dat','')

    temp = file_content[-5].split(':')[1].split(',')[:-1]
    changed_layer = []
    for i in range(len(temp)):
        changed_layer.append(int(temp[i]))

    temp = file_content[-4].split(':')[1]
    changed_660 = float(temp)

    temp = file_content[-3].split(':')[1]
    thickness = float(temp)

    temp = file_content[-2].split(':')[1].split(',')[:-1]
    vp_change = []
    for i in range(len(temp)):
        vp_change.append(float(temp[i]))
    
    temp = file_content[-1].split(':')[1].split(',')[:-1]
    vs_change = []
    for i in range(len(temp)):
        vs_change.append(float(temp[i]))

    data_content = file_content[1:-6]
    modify_model_temp = []
    for i in range(len(data_content)):
        modify_model_temp.append([])
        temp = data_content[i].split()
        for j in range(len(temp)):
            modify_model_temp[i].append(float(temp[j]))
    
    modify_model_need = DataFrame(modify_model_temp)

    no_modify_model = []; depth_modify_model = []; vp_modify_model = []; vs_modify_model = []; ro_modify_model = []; qp_modify_model = []; qs_modify_model = []
    for i in range(len(modify_model_need)):
        no_modify_model.append(int(modify_model_need[0][i]))
        depth_modify_model.append(float(modify_model_need[1][i]))
        vp_modify_model.append(float(modify_model_need[2][i]))
        vs_modify_model.append(float(modify_model_need[3][i]))
        ro_modify_model.append(float(modify_model_need[4][i]))
        qp_modify_model.append(float(modify_model_need[5][i]))
        qs_modify_model.append(float(modify_model_need[6][i]))

    modify_model_dic = {
        'no' : no_modify_model,
        'depth' : depth_modify_model,
        'vp' : vp_modify_model,
        'vs' : vs_modify_model,
        'ro' : ro_modify_model,
        'qp' : qp_modify_model,
        'qs' : qs_modify_model,
        'changed_layer' : changed_layer,
        'changed_layer_num' : len(changed_layer),
        'changed_660' : changed_660,
        'thickness' : thickness,
        'vp_change' : vp_change,
        'vs_change' : vs_change,
        't_echo' : techo

    }
    
    return modify_model_dic


#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################



def rebuild_seis_time_data(processed_time, processed_seis_data, cut_time_start_time, cut_time_windows, time_len, move_time_window_all_range, move_time_window_each_range):

    rebuild_seis_data = []
    rebuild_time_data = []
    rebuild_index = []
    move_time_window_each = []
    move_time_window_all = random.uniform(-move_time_window_all_range,move_time_window_all_range)

    for i in range(len(processed_seis_data)):
        move_time_window_each.append(random.uniform(-move_time_window_each_range,move_time_window_each_range))

        time_seq_begin = cut_time_start_time + move_time_window_all + move_time_window_each[-1]
        time_seq_end = time_seq_begin + cut_time_windows

        time_seq = list(np.linspace(time_seq_begin, time_seq_end, time_len))

        rebuild_time_data.append(time_seq)
        x = processed_time[i]
        y = processed_seis_data[i]
        f = interp1d(x, y, kind='linear')
        rebuild_seis_data.append(list(f(time_seq)))
        rebuild_index.append(i)

    return rebuild_seis_data, rebuild_time_data, rebuild_index, move_time_window_each, move_time_window_all


def rebuild_seis_data_norm(rebuild_seis_data):
    nor_rebuild_seis_data = []
    for i in range(len(rebuild_seis_data)):
        nor_rebuild_seis_data.append([])
        rebuild_seis_data_abs = [ abs(number) for number in rebuild_seis_data[i] ]
        loc_max = max(rebuild_seis_data_abs)
        for j in range(len(rebuild_seis_data[i])):
            nor_rebuild_seis_data[i].append(rebuild_seis_data[i][j] / loc_max)
    return nor_rebuild_seis_data

def rebuild_seis_data_norm_useindex(rebuild_seis_data,use_index):
    nor_rebuild_seis_data = []
    for i in range(len(rebuild_seis_data)):
        if i in use_index:
            nor_rebuild_seis_data.append([])
            rebuild_seis_data_abs = [ abs(number) for number in rebuild_seis_data[i] ]
            loc_max = max(rebuild_seis_data_abs)
            for j in range(len(rebuild_seis_data[i])):
                nor_rebuild_seis_data[i].append(rebuild_seis_data[i][j] / loc_max)
        else:
            nor_rebuild_seis_data.append(rebuild_seis_data[i])
    return nor_rebuild_seis_data

#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################

def get_rebuild_all_data(path):
    file = open(path, 'r')
    file_content = file.readlines()
    file.close()

    pro_time = []
    pro_vp_data = []
    for i in range(len(file_content)-9):
        if i%2 == 0:
            pro_time.append([])
            for j in range(len(file_content[i].split())-1):
                pro_time[int(i/2)].append(float(file_content[i].split()[j+1]))
        else:
            pro_vp_data.append([])
            for j in range(len(file_content[i].split())-1):
                pro_vp_data[int(i/2-0.5)].append(float(file_content[i].split()[j+1]))

    temp = file_content[-9]
    temp_t = temp.split(':')[1].split(',')[:-1]
    sta_location = []
    for i in range(len(temp_t)):
        sta_location.append(float(temp_t[i]))

    temp = file_content[-8]
    temp_t = temp.split(':')[1].split(',')[:-1]
    rebuild_index = []
    for i in range(len(temp_t)):
        rebuild_index.append(int(temp_t[i]))

    temp = file_content[-7]
    temp_t = temp.split(':')[1].split(',')[:-1]
    use_index = []
    for i in range(len(temp_t)):
        use_index.append(int(temp_t[i]))

    temp = file_content[-6]
    temp_t = temp.split(':')[1].split(',')[:-1]
    rebuild_locdata = []
    for i in range(len(temp_t)):
        rebuild_locdata.append(float(temp_t[i]))

    temp = file_content[-5]
    temp_t = temp.split('---')
    cut_start_time = float(temp_t[0].split(':')[1])
    cut_windows = float(temp_t[1].split(':')[1])
    reduction_v = float(temp_t[2].split(':')[1])
    move_time_window_all = float(temp_t[3].split(':')[1].replace('\n',''))

    temp = file_content[-4]
    temp_t = temp.split(':')[1].split(',')[:-1]
    move_time_window = []
    for i in range(len(temp_t)):
        move_time_window.append(float(temp_t[i]))

    temp = file_content[-3]
    temp_t = temp.split(':')[1].split(',')[:-1]
    sta_noise_mean = []
    for i in range(len(temp_t)):
        sta_noise_mean.append(float(temp_t[i]))

    temp = file_content[-2]
    temp_t = temp.split(':')[1].split(',')[:-1]
    sta_noise_sigma = []
    for i in range(len(temp_t)):
        sta_noise_sigma.append(float(temp_t[i]))

    temp = file_content[-1]
    temp_t = temp.split(':')[1].split(',')[:-1]
    add_noise_region_move_range = []
    for i in range(len(temp_t)):
        add_noise_region_move_range.append(float(temp_t[i]))

    return {
        'pro_time':pro_time,
        'pro_vp_data':pro_vp_data,
        'sta_location':sta_location,
        'rebuild_index':rebuild_index,
        'use_index':use_index,
        'rebuild_locdata':rebuild_locdata,
        'cut_start_time':cut_start_time,
        'cut_windows':cut_windows,
        'reduction_v':reduction_v,
        'move_time_window_all':move_time_window_all,
        'move_time_window':move_time_window,
        'sta_noise_mean':sta_noise_mean,
        'sta_noise_sigma':sta_noise_sigma,
        'add_noise_region_move_range':add_noise_region_move_range
    }

def testset_add_noise(use_index, fresh_rebuild_seis_data, sigma_value, mean_value=0):

    rebuild_seis_data_noise = []

    for i in range(len(fresh_rebuild_seis_data)):
        rebuild_seis_data_noise.append([])
        for j in range(len(fresh_rebuild_seis_data[i])):
            if i in use_index:
                rebuild_seis_data_noise[i].append(fresh_rebuild_seis_data[i][j]+random.gauss(mean_value,sigma_value))
            else:
                rebuild_seis_data_noise[i].append(0)

    rebuild_seis_data_noise = rebuild_seis_data_norm_useindex(rebuild_seis_data_noise, use_index)

    sta_noise_mean = []
    sta_noise_sigma = []
    add_noise_region_move_range_each = []
    for i in range(len(fresh_rebuild_seis_data)):
        sta_noise_mean.append(mean_value)
        sta_noise_sigma.append(sigma_value)
        add_noise_region_move_range_each.append(0)

    return rebuild_seis_data_noise, sta_noise_mean, sta_noise_sigma, add_noise_region_move_range_each


def testset_sta_add(fresh_rebuild_seis_data, ref_rebuild_seis_data, ref_use_index, ref_sta_noise_mean, ref_sta_noise_sigma, use_sta_num, locdata, spe_sta):
    # 只增加台站，使用该函数

    if use_sta_num <= len(ref_use_index):
        raise ValueError(f"n({use_sta_num})({len(ref_use_index)})")

    add_index_num = use_sta_num - len(ref_use_index)
    add_index_range = []

    for i in range(len(ref_rebuild_seis_data)):
        if i in ref_use_index:
            continue
        else:
            add_index_range.append(i)

    add_index = random.sample(add_index_range, add_index_num)

    rebuild_seis_data_random_sta = []

    for i in range(len(ref_rebuild_seis_data)):
        if i in ref_use_index:
            rebuild_seis_data_random_sta.append(ref_rebuild_seis_data[i])
        elif i in add_index:
            rebuild_seis_data_random_sta.append([])
            for j in range(len(ref_rebuild_seis_data[i])):
                rebuild_seis_data_random_sta[-1].append(fresh_rebuild_seis_data[i][j]+random.gauss(ref_sta_noise_mean[i],ref_sta_noise_sigma[i]))
        else:
            rebuild_seis_data_random_sta.append([0 for _ in range(len(ref_rebuild_seis_data[i]))])

    use_index = deepcopy(ref_use_index)
    use_index.extend(add_index)
    use_index.sort()

    rebuild_loc = []
    for i in range(len(locdata)):
        if i in use_index:
            rebuild_loc.append(locdata[i])
        else:
            rebuild_loc.append(spe_sta[i])

    return rebuild_seis_data_random_sta, use_index, rebuild_loc

def testset_sta_remove(ref_rebuild_seis_data, ref_use_index, use_sta_num, locdata, spe_sta):

    if use_sta_num >= len(ref_use_index):
        raise ValueError(f"n({use_sta_num})({len(ref_use_index)})")

    remove_index = random.sample(ref_use_index, use_sta_num)
    remove_index.sort()

    rebuild_seis_data_random_sta = []
    for i in range(len(ref_rebuild_seis_data)):
        if i in remove_index:
            rebuild_seis_data_random_sta.append(deepcopy(ref_rebuild_seis_data[i]))
        else:
            rebuild_seis_data_random_sta.append([0 for _ in range(len(ref_rebuild_seis_data[i]))])

    rebuild_loc = []
    for i in range(len(locdata)):
        if i in remove_index:
            rebuild_loc.append(locdata[i])
        else:
            rebuild_loc.append(spe_sta[i])

    return rebuild_seis_data_random_sta, remove_index, rebuild_loc

def testset_sta_mid(ref_rebuild_seis_data_more, ref_use_index_less, ref_use_index_more, use_sta_num, locdata, spe_sta):

    if use_sta_num >= len(ref_use_index_more):
        raise ValueError(f"n({use_sta_num})({len(ref_use_index_more)})")
    if use_sta_num <= len(ref_use_index_less):
        raise ValueError(f"n({use_sta_num})({len(ref_use_index_less)})")

    mid_index_num = use_sta_num - len(ref_use_index_less)
    mid_index_range = []

    for i in ref_use_index_more:
        if i in ref_use_index_less:
            continue
        else:
            mid_index_range.append(i)

    mid_index = random.sample(mid_index_range, mid_index_num)

    use_index = deepcopy(ref_use_index_less)
    use_index.extend(mid_index)
    use_index.sort()

    rebuild_seis_data_random_sta = []
    for i in range(len(ref_rebuild_seis_data_more)):
        if i in use_index:
            rebuild_seis_data_random_sta.append(deepcopy(ref_rebuild_seis_data_more[i]))
        else:
            rebuild_seis_data_random_sta.append([0 for _ in range(len(ref_rebuild_seis_data_more[i]))])

    rebuild_loc = []
    for i in range(len(locdata)):
        if i in use_index:
            rebuild_loc.append(locdata[i])
        else:
            rebuild_loc.append(spe_sta[i])

    return rebuild_seis_data_random_sta, use_index, rebuild_loc

def write_rebuild_data(
        opapsd_path,
        rebuild_seis_data, 
        rebuild_time_data, 
        sta_location, 
        rebuild_index, 
        use_index, 
        rebuild_locdata, 
        cut_start_time, 
        cut_windows, 
        move_time_window_each,
        move_time_window_all,
        reduction_v,
        sta_noise_mean,
        sta_noise_sigma,
        add_noise_region_move_range_each,
    ):

    opapsd_path = opapsd_path
    opapsd_file = open(opapsd_path, 'w')
    
    for j in range(len(rebuild_time_data)):
        opapsd_file.write('T_sec   ')
        for k in range(len(rebuild_time_data[j])):
            opapsd_file.write(str(rebuild_time_data[j][k])+'   ')
        opapsd_file.write('\n')
        opapsd_file.write('U'+str(j)+'   ')
        for k in range(len(rebuild_seis_data[j])):
            opapsd_file.write(str(rebuild_seis_data[j][k])+'   ')
        opapsd_file.write('\n')
    sta_location_str = ''
    for j in range(len(sta_location)):
        sta_location_str = sta_location_str + str(sta_location[j]) + ','
    opapsd_file.write('sta_location:'+sta_location_str)
    opapsd_file.write('\n')
    rebuild_index_str = ''
    for j in range(len(rebuild_index)):
        rebuild_index_str = rebuild_index_str + str(rebuild_index[j]) + ','
    opapsd_file.write('rebuild_index:'+rebuild_index_str)
    opapsd_file.write('\n')
    use_index_str = ''
    for j in range(len(use_index)):
        use_index_str = use_index_str + str(use_index[j]) + ','
    opapsd_file.write('use_index:'+use_index_str)
    opapsd_file.write('\n')
    rebuild_locdata_str = ''
    for j in range(len(rebuild_locdata)):
        rebuild_locdata_str = rebuild_locdata_str + str(rebuild_locdata[j]) + ','
    opapsd_file.write('rebuild_locdata:'+rebuild_locdata_str)
    opapsd_file.write('\n')
    opapsd_file.write('cut_start_time:'+str(cut_start_time))
    opapsd_file.write('---cut_windows:'+str(cut_windows))
    opapsd_file.write('---reduction_v:'+str(reduction_v))
    opapsd_file.write('---move_time_window_all:'+str(move_time_window_all))
    opapsd_file.write('\n')
    move_time_window_str = ''
    for j in range(len(move_time_window_each)):
        move_time_window_str = move_time_window_str + str(move_time_window_each[j]) + ','
    opapsd_file.write('move_time_window:'+move_time_window_str)
    opapsd_file.write('\n')
    sta_noise_mean_str = ''
    for j in range(len(sta_noise_mean)):
        sta_noise_mean_str = sta_noise_mean_str + str(sta_noise_mean[j]) + ','
    opapsd_file.write('sta_noise_mean:'+sta_noise_mean_str)
    opapsd_file.write('\n')
    sta_noise_sigma_str = ''
    for j in range(len(sta_noise_sigma)):
        sta_noise_sigma_str = sta_noise_sigma_str + str(sta_noise_sigma[j]) + ','
    opapsd_file.write('sta_noise_sigma:'+sta_noise_sigma_str)
    opapsd_file.write('\n')
    add_noise_region_move_range_str = ''
    for j in range(len(add_noise_region_move_range_each)):
        add_noise_region_move_range_str = add_noise_region_move_range_str + str(add_noise_region_move_range_each[j]) + ','
    opapsd_file.write('add_noise_region_move_range:'+add_noise_region_move_range_str)


    opapsd_file.close()

def draw_rebuild_data(
    vel_base_dic,
    modify_model_dic,
    locdata,
    rebuild_seis_data,
    rebuild_time_data,
    use_index,
    cut_time_start_time,
    cut_time_windows,
    show_pic_dic_path,
    draw_depth_para,
    reduction_v,
):
    depth_modify = modify_model_dic['depth']
    vp_modify = modify_model_dic['vp']
    depth_vel_base = vel_base_dic['depth']
    vp_vel_base = vel_base_dic['vp']
    
    draw_vel_base_layer_num = 0
    for i in range(len(depth_vel_base)):
        if depth_vel_base[i]>draw_depth_para[0] and depth_vel_base[i]<draw_depth_para[1]:
            draw_vel_base_layer_num = draw_vel_base_layer_num +1
    begin_vel_base_draw_num = 0
    for i in range(len(depth_vel_base)):
        if depth_vel_base[i]<=draw_depth_para[0]:
            begin_vel_base_draw_num = begin_vel_base_draw_num +1

    draw_modify_layer_num = 0
    for i in range(len(depth_modify)):
        if depth_modify[i]>draw_depth_para[0] and depth_modify[i]<draw_depth_para[1]:
            draw_modify_layer_num = draw_modify_layer_num +1
    begin_modify_draw_num = 0
    for i in range(len(depth_modify)):
        if depth_modify[i]<=draw_depth_para[0]:
            begin_modify_draw_num = begin_modify_draw_num +1

    for i in range(len(locdata)):
        locrv = locdata[i]
        for j in range(len(rebuild_seis_data[i])):
            rebuild_seis_data[i][j] = rebuild_seis_data[i][j]/2 + locrv

    fig1 = plt.figure()
    grid = plt.GridSpec(3,4)
    ax1 = fig1.add_subplot(grid[0:3,0])
    ax1.plot(vp_vel_base[begin_vel_base_draw_num:begin_vel_base_draw_num+draw_vel_base_layer_num], depth_vel_base[begin_vel_base_draw_num:begin_vel_base_draw_num+draw_vel_base_layer_num], 'xkcd:blue', linewidth=1, label ='vel_base')
    ax1.plot(vp_modify[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num], depth_modify[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num], 'xkcd:green', linewidth=1, label ='modified')
    ax1.legend(loc='lower left', prop={'size':6})
    ax1.set_xticks([min(vp_modify[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num])-0.5,max(vp_modify[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num])+0.5])
    ax1.invert_yaxis()
    ax1.set_ylabel('Depth(km)')
    ax1.set_xlabel('Velocity(km/s)')
    ax1.set_title('Velocity model')

    ax2 = fig1.add_subplot(grid[0:3,1:4])
    for j in range(len(locdata)):
        if j in use_index:
            ax2.plot(rebuild_time_data[j], rebuild_seis_data[j], 'k')
    ax2.set_xlim(cut_time_start_time, cut_time_start_time+cut_time_windows)
    ax2.set_ylim(9,31)
    ax2.set_ylabel('Distance(deg)')
    ax2.set_xlabel('t-'+str(reduction_v)+'*distance(s))')
    
    locdata_pic = [10.0,20.0,30.0]
    locdata_str=[]

    for i in range(len(locdata_pic)):
        locdata_str.append(str(locdata_pic[i]))
    
    ax2.set_yticks(locdata_pic)
    ax2.set_yticklabels(locdata_str)
    ax2.yaxis.tick_right ()
    ax2.yaxis.set_label_position('right')
    ax2.set_title('Seismic wave')
    
    fig1.tight_layout()
    fig1.savefig(show_pic_dic_path)
    fig1.clf()
    plt.close(fig=fig1)


