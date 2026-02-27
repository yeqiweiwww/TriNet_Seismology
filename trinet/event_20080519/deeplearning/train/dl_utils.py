


import os
import random
import shutil
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from copy import deepcopy
from scipy.interpolate import interp1d
from pandas.core.frame import DataFrame

import torch

from dl_paraconfig import range_660, disc_660, label_range_dep, modify_velocity_percent, label_range_vel, loc_range_min_para, loc_range_max_para, loc_range_para, spe_sta_loc_para, changed_layer_num, draw_depth, rang_draw, reduction_v
from gen_modify_vel_base import modify_vel_base_model

class model_data_process:
    def __init__(self):
        pass
        
    def read_modeldata(self, file_path):

        self.modify_model_dic = get_modify_model_data(file_path)

        return self.modify_model_dic

    def get_change_660(self,range_660=range_660):

        modify_660 = deepcopy(self.modify_model_dic['changed_660'])
        changed_660 = (modify_660-disc_660)/range_660*label_range_dep

        return [changed_660]
    
    def get_change_depth(self):
        depth_data = deepcopy(self.modify_model_dic['depth'])
        changed_layer = deepcopy(self.modify_model_dic['changed_layer'])

        self.depth_used = []
        for i in changed_layer:
            self.depth_used.append(depth_data[i-1])
        
        return self.depth_used
    
    def get_change_thickness(self):
        thickness = deepcopy(self.modify_model_dic['thickness'])
        changed_thickness = (thickness-range_660)/range_660*label_range_dep

        return [changed_thickness]

    def make_label(self):
        vp_change = deepcopy(self.modify_model_dic['vp_change'])
        vp_change_u = []
        for i in range(len(vp_change)):
            vp_change_u.append(vp_change[i]/modify_velocity_percent*label_range_vel)
        
        self.vp_change_u = vp_change_u

        return self.vp_change_u


    def mk_pre_model_data(self, outputdata, output_depth, output_thickness, vel_base_model_path, velocity_model_info_dic):

        path_info_dic = {}
        
        m_a_m = modify_vel_base_model(velocity_model_info_dic, path_info_dic)
        vel_base_model_dict_original = m_a_m.read_vel_base(vel_base_model_path)
        vel_base_model_dict_interpolation = m_a_m.interpolation_model()
        vel_base_model_dict_modify_layer_depth,thickness = m_a_m.modify_layer_depth()
        vel_base_model_dict_modify_velocity, v_ran_chan,changed_depth_no = m_a_m.modify_velocity()

        vel_base_vp = deepcopy(vel_base_model_dict_interpolation['vp'])
        vel_base_depth = vel_base_model_dict_interpolation['depth']

        for i in range(len(changed_depth_no)):
            vel_base_vp[changed_depth_no[i]-1]=vel_base_vp[changed_depth_no[i]-1]*outputdata[i]*modify_velocity_percent/label_range_vel+vel_base_vp[changed_depth_no[i]-1]

        depth_ind = get_index(vel_base_depth, disc_660)
        vel_base_depth[depth_ind[0]] = output_depth[0]*range_660/label_range_dep+disc_660
        vel_base_depth[depth_ind[0]+1] = output_thickness[0]*range_660/label_range_dep+range_660+vel_base_depth[depth_ind[0]]

        self.prediction_model_dic = {
            'no' : vel_base_model_dict_interpolation['no'],
            'depth' : vel_base_depth,
            'vp' : vel_base_vp,
            'vs' : vel_base_model_dict_interpolation['vs'],
            'ro' : vel_base_model_dict_interpolation['ro'],
            'qp' : vel_base_model_dict_interpolation['qp'],
            'qs' : vel_base_model_dict_interpolation['qs'],
        }

        return self.prediction_model_dic

    # write label prediction file
    def wr_vlb_pre_file(
            self, 
            loss1_vel, 
            loss2_dep, 
            loss3_thi, 
            loss1,
            loss2,
            loss3,
            loss,
            mse_pre_modified, 
            modify_660, 
            pre_660, 
            mse_660, 
            modi_thickness, 
            pre_thickness, 
            mse_thickness, 
            diff_pre_modi, 
            change_layer, 
            prediction_model_path
            ):

        prediction_model = open(prediction_model_path, 'w')
        prediction_model.write('no   depth[km]   vp[km/s]   vs[km/s]   ro[g/cm^3]   qp   qs   \n')

        for i in range(len(self.modify_model_dic['no'])):
            prediction_model.write(
                str(self.prediction_model_dic['no'][i])+'   '+
                str(self.prediction_model_dic['depth'][i])+'   '+
                str(self.prediction_model_dic['vp'][i])+'   '+
                str(self.prediction_model_dic['vs'][i])+'   '+
                str(self.prediction_model_dic['ro'][i])+'   '+
                str(self.prediction_model_dic['qp'][i])+'   '+
                str(self.prediction_model_dic['qs'][i])+'   '+
                '\n'
            )

        prediction_model.write('loss1_vel:'+loss1_vel+'\n')
        prediction_model.write('loss2_dep:'+loss2_dep+'\n')
        prediction_model.write('loss3_thi:'+loss3_thi+'\n')
        prediction_model.write('loss1:'+loss1+'\n')
        prediction_model.write('loss2:'+loss2+'\n')
        prediction_model.write('loss3:'+loss3+'\n')
        prediction_model.write('loss:'+loss+'\n')
        prediction_model.write('mse_pre_modified:'+mse_pre_modified+'\n')
        prediction_model.write('modify_660:'+modify_660+'\n')
        prediction_model.write('pre_660:'+pre_660+'\n')
        prediction_model.write('mse_660:'+mse_660+'\n')
        prediction_model.write('modi_thickness:'+modi_thickness+'\n')
        prediction_model.write('pre_thickness:'+pre_thickness+'\n')
        prediction_model.write('mse_thickness:'+mse_thickness+'\n')
        prediction_model.write('diff_pre_modi:')
        for i in range(len(diff_pre_modi)):
            prediction_model.write(str(diff_pre_modi[i])+',')
        prediction_model.write('\n')
        prediction_model.write('change_layer:')
        for i in range(len(change_layer)):
            prediction_model.write(str(change_layer[i])+',')
        prediction_model.close()


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

    torch.backends.cudnn.enabled = False
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.use_deterministic_algorithms(mode=True, warn_only=True)

    generator=torch.Generator()
    generator.manual_seed(seed)

    return generator
