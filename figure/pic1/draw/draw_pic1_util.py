
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame



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

##########################################

def read_three_raypath(path, x_plus, y_factor):
    f = open(path, 'r')
    f_c = f.readlines()
    f.close()

    raypath_all = []
    for i in range(len(f_c)):
        if f_c[i].startswith('>'):
            raypath_all.append([])
        else:
            raypath_all[-1].append(f_c[i])

    raypath_x_all = []
    raypath_y_all = []

    for i in range(len(raypath_all)):
        raypath_x_all.append([])
        raypath_y_all.append([])
        for j in range(len(raypath_all[i])):
            raypath_x_all[-1].append((-float(raypath_all[i][j].split()[0])+x_plus)/180*np.pi)
            raypath_y_all[-1].append(float(raypath_all[i][j].split()[1])**y_factor)

    return raypath_x_all, raypath_y_all

##########################################

def get_rebuild_data(path):
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
        use_index.append(float(temp_t[i]))

    temp = file_content[-6]
    temp_t = temp.split(':')[1].split(',')[:-1]
    sta_location = []
    for i in range(len(temp_t)):
        sta_location.append(float(temp_t[i]))
        
    return pro_time, pro_vp_data, sta_location, use_index


##########################################


def add_aligned_text(fig, ax_pos, text, fontsize, x_plus=0, y_plus=0):

    fig.text(
        ax_pos.x0 + x_plus,
        ax_pos.y1 + y_plus,
        text,
        fontsize=fontsize,
        ha='left',
        va='top'
    )