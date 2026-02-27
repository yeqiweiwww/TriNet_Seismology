
import os
import shutil
from PIL import Image
from copy import deepcopy
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt

import torch
import random
import numpy as np

from real_para import *

# def get_image(input_img_path):
#     input_img=Image.open(input_img_path)
#     input_img = input_img.convert('1')

#     return input_img

def get_real_rebuild_data(path):
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


def gen_sta_dis_matrix(sta_location, pro_vp_data, arr_type='relative'):

    if arr_type == 'fix':
        loc_range_min = deepcopy(loc_range_min_para)
        loc_range_max = deepcopy(loc_range_max_para)
        loc_average = (loc_range_min + loc_range_max) / 2
        loc_divide = loc_average - loc_range_min
        rebuild_sta_location = []
        for index_sta in range(len(sta_location)):
            rebuild_sta_location.append([])
            for temp_index in range(len(pro_vp_data[index_sta])):
                rebuild_sta_location[-1].append((sta_location[index_sta]-loc_average)/loc_divide)

    if arr_type == 'relative':
        loc_range = deepcopy(loc_range_para)
        spe_sta_loc = deepcopy(spe_sta_loc_para)
        rebuild_sta_location = []
        for index_sta in range(len(sta_location)):
            rebuild_sta_location.append([])
            for temp_index in range(len(pro_vp_data[index_sta])):
                rebuild_sta_location[-1].append((sta_location[index_sta]-spe_sta_loc[index_sta])/loc_range)
    
    return rebuild_sta_location

# vel_base
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

def get_pre_model_data(pre_model_path):
    file = open(pre_model_path,'r')
    file_content = file.readlines()
    file.close

    data_content = file_content[1:-16]
    pre_model_temp = []
    for i in range(len(data_content)):
        pre_model_temp.append([])
        temp = data_content[i].split()
        for j in range(len(temp)):
            pre_model_temp[i].append(float(temp[j]))
    
    pre_model_need = DataFrame(pre_model_temp)

    no_pre_model = []; depth_pre_model = []; vp_pre_model = []; vs_pre_model = []; ro_pre_model = []; qp_pre_model = []; qs_pre_model = []
    for i in range(len(pre_model_need)):
        no_pre_model.append(int(pre_model_need[0][i]))
        depth_pre_model.append(float(pre_model_need[1][i]))
        vp_pre_model.append(float(pre_model_need[2][i]))
        vs_pre_model.append(float(pre_model_need[3][i]))
        ro_pre_model.append(float(pre_model_need[4][i]))
        qp_pre_model.append(float(pre_model_need[5][i]))
        qs_pre_model.append(float(pre_model_need[6][i]))

    pre_model_dic={
        'no' : no_pre_model,
        'depth' : depth_pre_model,
        'vp' : vp_pre_model,
        'vs' : vs_pre_model,
        'ro' : ro_pre_model,
        'qp' : qp_pre_model,
        'qs' : qs_pre_model
    }

    return pre_model_dic

def cal_diff_with_modify(pre_model_dic, modify_model_dic):
    vp_pre = pre_model_dic['vp']
    vp_modified = modify_model_dic['vp']
    
    mse_temp = []
    diff_pre_modify = []
    for i in range(len(vp_pre)):
        if not vp_pre[i]-vp_modified[i]==0:
            mse_temp.append((vp_pre[i]-vp_modified[i])**2)
            diff_pre_modify.append((vp_pre[i]-vp_modified[i]))

    mse_pre_modified = pow(sum(mse_temp)/changed_layer_num,0.5)

    return diff_pre_modify, mse_pre_modified

def draw_prediction_modify_model(
    vel_base_dic,
    modify_model_dic,
    prediction_model_dic,
    pro_time,
    pro_vp_data,
    draw_index,
    sta_location,
    show_pic_dic_path,
    mse_pre_modified,
    mse_660,
    mse_thickness,
    draw_depth=draw_depth
):

    depth_modify = modify_model_dic['depth']
    vp_modify = modify_model_dic['vp']
    depth_pre = prediction_model_dic['depth']
    vp_pre = prediction_model_dic['vp']
    depth_vel_base = vel_base_dic['depth']
    vp_vel_base = vel_base_dic['vp']

    draw_vel_base_layer_num = 0
    for i in range(len(depth_vel_base)):
        if depth_vel_base[i]>draw_depth[0] and depth_vel_base[i]<draw_depth[1]:
            draw_vel_base_layer_num = draw_vel_base_layer_num +1
    begin_vel_base_draw_num = 0
    for i in range(len(depth_vel_base)):
        if depth_vel_base[i]<=draw_depth[0]:
            begin_vel_base_draw_num = begin_vel_base_draw_num +1

    draw_modify_layer_num = 0
    for i in range(len(depth_modify)):
        if depth_modify[i]>draw_depth[0] and depth_modify[i]<draw_depth[1]:
            draw_modify_layer_num = draw_modify_layer_num +1
    begin_modify_draw_num = 0
    for i in range(len(depth_modify)):
        if depth_modify[i]<=draw_depth[0]:
            begin_modify_draw_num = begin_modify_draw_num +1


    diff_pre_mod = []
    for i in range(len(vp_modify)):
        diff_pre_mod.append((vp_pre[i]-vp_modify[i])/vp_modify[i])

    pro_time = deepcopy(pro_time)
    pro_vp_data = deepcopy(pro_vp_data)

    draw_index = deepcopy(draw_index)
    

    sta_location = deepcopy(sta_location)

    pro_vp_data_p=[]

    for i in range(len(pro_time)):
        plu = sta_location[-i-1]
        pro_vp_data_p.append([])
        for j in range(len(pro_vp_data[i])):
            pro_vp_data_p[i].append(pro_vp_data[i][j]+plu)

    locdata_pic = [10.0,20.0,30.0]
    locdata_str=[]

    for i in range(len(locdata_pic)):
        locdata_str.append(str(locdata_pic[-i-1]))
    fig1 = plt.figure()
    grid = plt.GridSpec(3,4)
    ax1 = fig1.add_subplot(grid[0:3,0])
    ax1.plot(vp_vel_base[begin_vel_base_draw_num:begin_vel_base_draw_num+draw_vel_base_layer_num], depth_vel_base[begin_vel_base_draw_num:begin_vel_base_draw_num+draw_vel_base_layer_num], 'xkcd:blue', linewidth=1, label ='vel_base')
    ax1.plot(vp_modify[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num], depth_modify[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num], 'xkcd:green', linewidth=1, label ='modified')
    ax1.plot(vp_pre[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num], depth_pre[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num], 'xkcd:red', linewidth=1, label ='predicted')
    ax1.text(0.6,0.93,'MSE:\n{}'.format(round(mse_pre_modified,4)),transform = ax1.transAxes,fontsize=8)
    ax1.text(0.6,0.83,'MSE:\n{}'.format(round(mse_660,4)),transform = ax1.transAxes,fontsize=8)
    ax1.text(0.6,0.73,'MSE:\n{}'.format(round(mse_thickness,4)),transform = ax1.transAxes,fontsize=8)
    ax1.legend(loc='lower left', prop={'size':6})
    ax1.set_xticks([min(vp_modify[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num])-0.5,max(vp_modify[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num])+0.5])
    ax1.invert_yaxis()
    ax1.set_ylabel('Depth(km)')
    ax1.set_xlabel('Velocity(km/s)')
    ax1.set_title('Velocity model')

    ax3 = ax1.twiny() 
    ax3.scatter(diff_pre_mod[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num], depth_modify[begin_modify_draw_num:begin_modify_draw_num+draw_modify_layer_num], c='xkcd:red', s=3, label ='diff')
    ax3.set_xticks([-0.1,0,0.1])

    ax2 = fig1.add_subplot(grid[0:3,1:4])
    for i in range(len(pro_vp_data)):
        if i in draw_index:
            ax2.plot(pro_time[i], pro_vp_data_p[i], 'k')
    ax2.set_xlim(rang_draw[0],rang_draw[1])
    ax2.set_ylabel('Distance(deg)')
    ax2.set_xlabel('t-'+str(reduction_v)+'*distance(s))')
    ax2.set_yticks(locdata_pic)
    ax2.set_yticklabels(locdata_str)
    ax2.yaxis.tick_right ()
    ax2.yaxis.set_label_position('right')
    ax2.set_title('Seismic wave')
    
    fig1.tight_layout()
    fig1.savefig(show_pic_dic_path)
    fig1.clf()
    plt.close(fig=fig1)


def mkdir(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

def deldir(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"Successfully removed folder: {path}")
        except Exception as e:
            print(f"Error deleting folder {path}: {e}")
    else:
        print(f"Folder does not exist: {path}")

def get_index(lis,item):
    return [index for (index,value) in enumerate(lis) if value == item]

def set_seed(cuda_visible_devices_str='0', seed=3407):

    os.environ['CUDA_VISIBLE_DEVICES'] = cuda_visible_devices_str

    random.seed(seed)
    np.random.seed(seed)

    os.environ['PYTHONHASHSEED'] = str(seed)
    os.environ['CUBLAS_WORKSPACE_CONFIG']=':16:8'

    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.use_deterministic_algorithms(True)
