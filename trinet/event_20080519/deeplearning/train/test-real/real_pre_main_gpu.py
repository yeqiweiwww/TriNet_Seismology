

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt

from copy import deepcopy

import torch
from torch import nn

from real_model import UNet_Encoder_Decoder
from real_model_data_process import model_data_process
from real_utils import set_seed, vel_base, mkdir, get_real_rebuild_data, gen_sta_dis_matrix, deldir
from real_para import cuda_visible_devices_str_para, seed_para, velocity_model_info_dic

ground_true_label = torch.tensor([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]).cuda()
# ground_true_label = torch.tensor([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])


cuda_visible_devices_str = deepcopy(cuda_visible_devices_str_para)
seed = deepcopy(seed_para)

set_seed(cuda_visible_devices_str, seed)

model_path = '../../../../../data/workspace_event_20080519_data/deeplearning/dl0_0/train0_0/model_epoch_dic/inversion_model_0927151753_epoch199.pth'

pic1 = 41
pic2 = 81
print(pic1,pic2)

in_channel=2
out_channel = 15
out_channel_dep = 1
out_channel_thick = 1

mc_dropout_times = 100

model = UNet_Encoder_Decoder(in_channel, out_channel, out_channel_dep, out_channel_thick, pic1, pic2)
# state_dict=torch.load(model_path, map_location='cpu')
state_dict=torch.load(model_path)
model.load_state_dict(state_dict)
model = model.cuda()
model.eval()
print(model)

loss_fn = nn.MSELoss()

vel_base_model_dic = vel_base('./vel_base_model.dat')

files_dir = './random_real_data'
files_name = os.listdir(files_dir)

pre_dir = './pre'
pre_pic_dir = './pre_pic'
rebuild_data_pic_dir = './random_real_data_pic'

deldir(pre_dir)
deldir(pre_pic_dir)
deldir(rebuild_data_pic_dir)

mkdir(pre_dir)
mkdir(pre_pic_dir)
mkdir(rebuild_data_pic_dir)

for index_file in range(len(files_name)):

    mkdir(pre_dir + '/' + files_name[index_file].replace('.dat',''))
    mkdir(pre_pic_dir + '/' + files_name[index_file].replace('.dat',''))

deldir('./loss')
mkdir('./loss')

for file_index in range(len(files_name)):

    print('file_index:',file_index)
    print('files_name:',files_name[file_index])

    files_path = files_dir + '/' + files_name[file_index]

    pro_time, pro_vp_data, sta_location, use_index = get_real_rebuild_data(files_path)

    rebuild_seis_data = []
    for j in range(len(pro_time)):
        rebuild_seis_data.append([])
        for k in range(len(pro_time[j])):
            rebuild_seis_data[-1].append(pro_vp_data[j][k]/2+sta_location[j])

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    for j in range(len(pro_time)):
        if j in use_index:
            ax1.plot(pro_time[j], rebuild_seis_data[j], 'k')
    
    ax1.set_ylim(9,31)
    
    fig1.savefig(rebuild_data_pic_dir+'/'+files_name[file_index].replace('.dat','')+'.png')

    rebuild_sta_location = gen_sta_dis_matrix(sta_location=sta_location, pro_vp_data=pro_vp_data, arr_type='relative')

    sta_loc_ten = np.array(deepcopy(rebuild_sta_location), dtype=np.float64)
    pro_vp_data_tensor = np.array(pro_vp_data, dtype=np.float64)

    pro_vp_data = np.array([[sta_loc_ten,pro_vp_data_tensor]], dtype=np.float64)

    seis_image = torch.FloatTensor(pro_vp_data)
    seis_image = seis_image.cuda()
    print(seis_image.size())

    model_li = vel_base('./model_li.dat')

    loss_file_all = []
    loss_file_path = './loss' + '/loss_' + files_name[file_index].replace('.dat','') + '.txt'
    f = open(loss_file_path,'w')
    f.close()

    for index_mc_dropout_times in range(mc_dropout_times):

        with torch.no_grad():
            output = model(seis_image)

            loss = loss_fn(ground_true_label, output)
            loss_file_all.append(loss.item())

            f = open(loss_file_path,'a')
            f.write('index_mc_dropout_times_'+str(index_mc_dropout_times)+':'+str(loss_file_all[-1])+'\n')
            f.close()

            output_velo = output[:,:out_channel]
            output_depth = output[:,out_channel:out_channel+out_channel_dep]
            output_thickness = output[:,out_channel+out_channel_dep:out_channel+out_channel_dep+out_channel_thick]

            print('index_mc_dropout_times:',index_mc_dropout_times)

        mdp = model_data_process()
        prediction_model_dic = mdp.mk_pre_model_data(torch.squeeze(output_velo,dim=0).tolist(),torch.squeeze(output_depth,dim=0).tolist(), torch.squeeze(output_thickness,dim=0).tolist(), './vel_base_model.dat',velocity_model_info_dic)
        mdp.wr_vlb_pre_file(prediction_model_dic, pre_dir + '/'+ files_name[file_index].replace('.dat','') + '/pre' + str(index_mc_dropout_times) + '.txt')
        plt.figure(figsize=(5,10))
        plt.plot(vel_base_model_dic['vp'],vel_base_model_dic['depth'],'b',label='ak135')
        plt.plot(model_li['vp'],model_li['depth'],'g',label='model_li')
        plt.plot(prediction_model_dic['vp'],prediction_model_dic['depth'],'r',label='pre')

        plt.ylim(410,1000)

        plt.gca().invert_yaxis()
        plt.legend()
        plt.savefig(pre_pic_dir+ '/' + files_name[file_index].replace('.dat','') + '/pre' + str(index_mc_dropout_times) + '.png')
        plt.close('all')
