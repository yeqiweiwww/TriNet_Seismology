

import os
import numpy as np
from PIL import Image

import torch
import torchvision
from torch import nn

from copy import deepcopy

from dl_utils import set_seed, mkdir, vel_base, cal_diff_with_modify, draw_prediction_modify_model
from dl_model import UNet_Encoder_Decoder
from dl_paraconfig import cuda_visible_devices_str_para, seed_para, dl_tr_data_path, vel_base_path, disc_660, range_660, label_range_dep, label_range_vel, modify_velocity_percent, vel_model_info_dic, draw_depth 
from dl_load_data import load_mydataset, get_rebuild_data, gen_sta_dis_matrix, model_data_process

testset_techo_file_dir_path = '../data'


cuda_visible_devices_str = deepcopy(cuda_visible_devices_str_para)
seed = deepcopy(seed_para)

set_seed(cuda_visible_devices_str, seed)

# model_files = sorted(os.listdir(pre_model_dic_path),key=lambda x: os.path.getmtime(os.path.join(pre_model_dic_path, x)))[-1]
model_path = '../../../../data/trinet_data/event_20080519_data/deeplearning/train/model_epoch_dic/inversion_model_0927151753_epoch199.pth'
# print(model_path)

testset_name = [
    'testset_rebuild_seis_data_noise005',
    'testset_rebuild_seis_data_noise010',
    'testset_rebuild_seis_data_noise020',
    'testset_rebuild_seis_data_noise025',
    'testset_rebuild_seis_data_sta7',
    'testset_rebuild_seis_data_sta15',
    'testset_rebuild_seis_data_sta23',
    'testset_rebuild_seis_data_sta39',
]

testset_num = len(testset_name)
print(testset_name)

load_dataset_test = load_mydataset(techo_file_path=testset_techo_file_dir_path+'/'+testset_name[0]+'.dat')

pic1 = load_dataset_test.get_info()[0].shape[1]
pic2 = load_dataset_test.get_info()[0].shape[2]
# print(pic1,pic2)

in_channel = load_dataset_test.get_info()[0].shape[0]
out_channel = load_dataset_test.get_info()[1].shape[0]
out_channel_velo = load_dataset_test.get_info()[2][0]
out_channel_depth = load_dataset_test.get_info()[2][1]
out_channel_thickness = load_dataset_test.get_info()[2][2]

vp_len, change_660_len, thickness_len = load_dataset_test.get_info()[2]

label_vel_idx=[0,vp_len]
label_dis_idx=[vp_len,vp_len+change_660_len]
label_thick_idx=[vp_len+change_660_len,vp_len+change_660_len+thickness_len]

model = UNet_Encoder_Decoder(in_channel, out_channel_velo, out_channel_depth, out_channel_thickness, pic1, pic2)
# model = nn.DataParallel(model)
state_dict=torch.load(model_path)
model.load_state_dict(state_dict)
model = model.cuda()
model.eval()
# print(model)

loss_fn = nn.MSELoss()

for index_testset in range(testset_num):

    testset_pre_model_dir_path = dl_tr_data_path + '/' + testset_name[index_testset] + '/prediction_model'
    test_show_dir_path = dl_tr_data_path + '/' + testset_name[index_testset] + '/pre_show'
    test_loss_file_dir_path = dl_tr_data_path + '/' + testset_name[index_testset]

    mkdir(testset_pre_model_dir_path)
    mkdir(test_show_dir_path)

    text_temp = open(testset_techo_file_dir_path+'/'+testset_name[index_testset]+'.dat')
    test_techo_file = text_temp.readlines()
    text_temp.close()
    test_size = len(test_techo_file)

    vel_base_model_dic = vel_base(vel_base_path)

    total_test_loss = []
    total_test_loss1 = []
    total_test_loss2 = []
    total_test_loss3 = []
    total_test_loss1_vel = []
    total_test_loss2_dep = []
    total_test_loss3_thi = []
    total_mse_pre_model = []
    total_mse_660 = []
    total_mse_thickness = []
    t_echo_all = []

    pro_time, _, _, _ = get_rebuild_data(os.path.dirname(os.path.dirname(os.path.dirname(test_techo_file[0].replace('\n',''))))+'/rebuild_seis_data/seis_rebuild_data/rebuild_vp_seis'+os.path.basename(test_techo_file[0].replace('\n','')).replace('rebuild_vp_seis', '').replace('.dat', '')+'.dat')
    # print(os.path.dirname(os.path.dirname(os.path.dirname(test_techo_file[0].replace('\n',''))))+'/rebuild_seis_data/seis_rebuild_data/rebuild_vp_seis'+os.path.basename(test_techo_file[0].replace('\n','')).replace('rebuild_vp_seis', '').replace('.dat', '')+'.dat')

    for i in range(len(test_techo_file)):
        files_path = test_techo_file[i].replace('\n','')
        techo = os.path.basename(files_path).replace('rebuild_vp_seis', '').replace('.dat', '')
        print(techo)
        files_dir_path_1 = os.path.dirname(os.path.dirname(os.path.dirname(files_path)))
        files_dir_path_2 = os.path.dirname(os.path.dirname(files_path))
        
        model_path = files_dir_path_1+'/modified_modelfile/modify_model'+techo+'.dat'
        mdp = model_data_process()
        modify_model_dic = mdp.read_modeldata(model_path)
        # tar_velo = torch.FloatTensor(np.array(mdp.make_label(),dtype=np.float64))
        tar_velo_item = mdp.make_label()

        seis_path = files_dir_path_2+'/seis_rebuild_data/rebuild_vp_seis'+techo+'.dat'
        pro_time_t, pro_vp_data, sta_location, use_index = get_rebuild_data(seis_path)

        rebuild_sta_location = gen_sta_dis_matrix(sta_location=sta_location, pro_vp_data=pro_vp_data, arr_type='relative')

        sta_loc_ten = deepcopy(rebuild_sta_location)
        sta_loc_ten = np.array(sta_loc_ten, dtype=np.float64)
        pro_vp_data_tensor = torch.FloatTensor(np.array(pro_vp_data, dtype=np.float64))

        # print(sta_loc_ten)
        seis_image = torch.FloatTensor(np.array([sta_loc_ten,pro_vp_data], dtype=np.float64))
        seis_image = torch.reshape(seis_image, (1, in_channel, pic1, pic2))
        seis_image = seis_image.cuda()
        tar_depth_item = modify_model_dic['changed_660']
        print('depth:',tar_depth_item)
        # tar_depth = torch.FloatTensor(np.array([tar_depth],dtype=np.float64))
        tar_thickness_item = modify_model_dic['thickness']
        print('thickness:',tar_thickness_item)
        # tar_thickness = torch.FloatTensor(np.array([tar_thickness],dtype=np.float64))

        label = deepcopy(tar_velo_item)
        label.extend([(tar_depth_item-disc_660)/range_660*label_range_dep])
        label.extend([(tar_thickness_item-range_660)/range_660*label_range_dep])
        label = torch.FloatTensor(np.array([label], dtype=np.float64))
        label = label.cuda()

        tar_velo = label[:,label_vel_idx[0]:label_vel_idx[1]]
        tar_depth = label[:,label_dis_idx[0]:label_dis_idx[1]]
        tar_thickness = label[:,label_thick_idx[0]:label_thick_idx[1]]

        with torch.no_grad():
            output = model(seis_image)

            output_velo = output[:,label_vel_idx[0]:label_vel_idx[1]]
            output_depth = output[:,label_dis_idx[0]:label_dis_idx[1]]
            output_thickness = output[:,label_thick_idx[0]:label_thick_idx[1]]

            loss  = loss_fn(output, label)
            loss1 = loss_fn(output_velo, tar_velo)
            loss2 = loss_fn(output_depth, tar_depth)
            loss3 = loss_fn(output_thickness, tar_thickness)

        total_test_loss1_vel.append(pow(loss1.item(),0.5)/label_range_vel*modify_velocity_percent)
        total_test_loss2_dep.append(pow(loss2.item(),0.5)/label_range_dep*range_660)
        total_test_loss3_thi.append(pow(loss3.item(),0.5)/label_range_dep*range_660)
        total_test_loss.append(pow(loss.item(),0.5))
        total_test_loss1.append(pow(loss1.item(),0.5))
        total_test_loss2.append(pow(loss2.item(),0.5))
        total_test_loss3.append(pow(loss3.item(),0.5))
        prediction_model_dic = mdp.mk_pre_model_data(torch.squeeze(output,dim=0).tolist(),torch.squeeze(output_depth,dim=0).tolist(), torch.squeeze(output_thickness,dim=0).tolist(), vel_base_path, vel_model_info_dic)

        diff_pre_modi, mse_pre_modified = cal_diff_with_modify(prediction_model_dic,modify_model_dic)

        modify_660 = deepcopy(tar_depth_item)
        modify_660 = torch.FloatTensor(np.array([modify_660],dtype=np.float64))
        pre_660 = float(torch.squeeze(output_depth,dim=0).tolist()[0]/label_range_dep*range_660+disc_660)
        mse_660 = float(torch.squeeze(output_depth,dim=0).tolist()[0]/label_range_dep*range_660+disc_660-modify_660)

        modi_thickness = deepcopy(tar_thickness_item)
        modi_thickness = torch.FloatTensor(np.array([modi_thickness],dtype=np.float64))
        pre_thickness = float(torch.squeeze(output_thickness,dim=0).tolist()[0]/label_range_dep*range_660+range_660)
        mse_thickness = float(torch.squeeze(output_thickness,dim=0).tolist()[0]/label_range_dep*range_660+range_660-modi_thickness)

        total_mse_pre_model.append(mse_pre_modified)
        total_mse_660.append(mse_660)
        total_mse_thickness.append(mse_thickness)

        print('mse_premo',mse_pre_modified)
        print('mse_660',mse_660)
        print('mse_thicknsee',mse_thickness)
        
        change_layer = modify_model_dic['changed_layer']
        pre_path = testset_pre_model_dir_path +'/pre_model'+techo+'.dat'
        mdp.wr_vlb_pre_file(
            str(pow(loss1.item(),0.5)/label_range_vel*modify_velocity_percent),
            str(pow(loss2.item(),0.5)/label_range_dep*range_660),
            str(pow(loss3.item(),0.5)/label_range_dep*range_660),
            str(pow(loss1.item(),0.5)),
            str(pow(loss2.item(),0.5)),
            str(pow(loss3.item(),0.5)),
            str(pow(loss.item(),0.5)),
            str(mse_pre_modified),
            str(modify_660.item()), 
            str(pre_660),
            str(mse_660), 
            str(modi_thickness.item()), 
            str(pre_thickness), 
            str(mse_thickness), 
            diff_pre_modi, 
            change_layer, 
            pre_path)
        print(i)
        print(techo)

        show_pic_dic_path = test_show_dir_path+'/pre_model'+modify_model_dic['t_echo']
        draw_show_pic = draw_prediction_modify_model(
            vel_base_model_dic,
            modify_model_dic,
            prediction_model_dic,
            pro_time,
            pro_vp_data,
            use_index,
            sta_location,
            show_pic_dic_path,
            mse_pre_modified,
            mse_660,
            mse_thickness,
            draw_depth=draw_depth
            )

    test_loss1_vel = sum(total_test_loss1_vel)/len(total_test_loss1_vel)
    test_loss2_dep = sum(total_test_loss2_dep)/len(total_test_loss2_dep)
    test_loss3_thi = sum(total_test_loss3_thi)/len(total_test_loss3_thi)
    test_loss1 = sum(total_test_loss1)/len(total_test_loss1)
    test_loss2 = sum(total_test_loss2)/len(total_test_loss2)
    test_loss3 = sum(total_test_loss3)/len(total_test_loss3)
    test_loss = sum(total_test_loss)/len(total_test_loss)

    f = open(test_loss_file_dir_path+'/test_loss_'+testset_name[index_testset]+'.dat', 'w')
    for i in range(len(total_test_loss1)):
        f.write(test_techo_file[i].replace('\n','') + '---loss1_vel:' + str(total_test_loss1_vel[i]) + '---loss2_dep:' + str(total_test_loss2_dep[i]) + '---loss3_thi:' + str(total_test_loss3_thi[i]) + '---loss1:' + str(total_test_loss1[i]) + '---loss2:' + str(total_test_loss2[i]) + '---loss3:' + str(total_test_loss3[i]) + '---loss:' + str(total_test_loss[i]) + '---mse_pre_model:' + str(total_mse_pre_model[i]) + '---mse_660:' + str(total_mse_660[i]) + '---mse_thickness:' + str(total_mse_thickness[i]) + '\n')
    f.write('loss_vel_mean1:'+str(test_loss1_vel)+'\n')
    f.write('loss_dep_mean2:'+str(test_loss2_dep)+'\n')
    f.write('loss_thi_mean3:'+str(test_loss3_thi)+'\n')
    f.write('loss_mean1:'+str(test_loss1)+'\n')
    f.write('loss_mean2:'+str(test_loss2)+'\n')
    f.write('loss_mean3:'+str(test_loss3)+'\n')
    f.write('loss_mean:'+str(test_loss)+'\n')

    f.write('mse_pre_model:'+str(sum(total_mse_pre_model)/len(total_mse_pre_model))+'\n')

    total_mse_660_cal=[]
    for i in range(len(total_mse_660)):
        total_mse_660_cal.append(abs(total_mse_660[i]))
    f.write('mse_660:'+str(sum(total_mse_660_cal)/len(total_mse_660_cal))+'\n')

    total_mse_thickness_cal=[]
    for i in range(len(total_mse_thickness)):
        total_mse_thickness_cal.append(abs(total_mse_thickness[i]))
    f.write('mse_thickness:'+str(sum(total_mse_thickness_cal)/len(total_mse_thickness_cal))+'\n')
    f.close()