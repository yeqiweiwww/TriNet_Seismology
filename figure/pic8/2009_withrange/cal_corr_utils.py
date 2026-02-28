
import random
import numpy as np
from scipy.interpolate import interp1d

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


def get_rebuild_data_real(path):
    file = open(path, 'r')
    file_content = file.readlines()
    file.close()

    pro_time = []
    pro_vp_data = []
    for i in range(len(file_content)-4):
        if i%2 == 0:
            pro_time.append([])
            for j in range(len(file_content[i].split())-1):
                pro_time[int(i/2)].append(float(file_content[i].split()[j+1]))
        else:
            pro_vp_data.append([])
            for j in range(len(file_content[i].split())-1):
                pro_vp_data[int(i/2-0.5)].append(float(file_content[i].split()[j+1]))
    
    temp = file_content[-2]
    temp_t = temp.split(':')[1].split(',')[:-1]
    use_index = []
    for i in range(len(temp_t)):
        use_index.append(int(temp_t[i]))
    
    temp = file_content[-4]
    temp_t = temp.split(':')[1].split(',')[:-1]
    sta_location = []
    for i in range(len(temp_t)):
        sta_location.append(float(temp_t[i]))

    return pro_time, pro_vp_data, sta_location, use_index

def get_rebuild_data_rebuild(path):
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
    
    temp = file_content[-7]
    temp_t = temp.split(':')[1].split(',')[:-1]
    use_index = []
    for i in range(len(temp_t)):
        use_index.append(int(temp_t[i]))
    
    temp = file_content[-6]
    temp_t = temp.split(':')[1].split(',')[:-1]
    sta_location = []
    for i in range(len(temp_t)):
        sta_location.append(float(temp_t[i]))

    return pro_time, pro_vp_data, sta_location, use_index


