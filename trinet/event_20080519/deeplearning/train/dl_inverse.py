

'''

'''

import time
import os

from copy import deepcopy

import torch
import torch.nn as nn
import torchvision
from torch.utils.data import DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter

from dl_load_data import load_mydataset
from dl_utils import set_seed, mkdir
from dl_model import UNet_Encoder_Decoder
from dl_paraconfig import cuda_visible_devices_str_para, seed_para, checkpoint_save_dic_path, pre_model_dic_path, total_train_step_para, epoch_para, start_epoch_para, batch_size_para, train_techo_file_path, val_techo_file_path, learningrate_para, checkpoint_dic_path, logging_path, label_range_vel, modify_velocity_percent, range_660, label_range_dep, disc_660, logs_path

# os.environ['CUDA_VISIBLE_DEVICES'] = '0'

cuda_visible_devices_str = deepcopy(cuda_visible_devices_str_para)
seed = deepcopy(seed_para)

generator = set_seed(cuda_visible_devices_str, seed)

# device = torch.device("cuda:0")


mkdir(checkpoint_save_dic_path)
mkdir(pre_model_dic_path)


total_train_step = deepcopy(total_train_step_para)
epoch = deepcopy(epoch_para)
start_epoch = deepcopy(start_epoch_para)
batch_size = deepcopy(batch_size_para)


load_dataset_train = load_mydataset(techo_file_path=train_techo_file_path)
load_dataset_val = load_mydataset(techo_file_path=val_techo_file_path)


pic1 = load_dataset_train.get_info()[0].shape[1]
pic2 = load_dataset_train.get_info()[0].shape[2]
print(pic1,pic2)

in_channel = load_dataset_train.get_info()[0].shape[0]
out_channel = load_dataset_train.get_info()[1].shape[0]
out_channel_velo = load_dataset_train.get_info()[2][0]
out_channel_depth = load_dataset_train.get_info()[2][1]
out_channel_thickness = load_dataset_train.get_info()[2][2]

vp_len, change_660_len, thickness_len = load_dataset_train.get_info()[2]

label_vel_idx=[0,vp_len]
label_dis_idx=[vp_len,vp_len+change_660_len]
label_thick_idx=[vp_len+change_660_len,vp_len+change_660_len+thickness_len]

train_size = len(load_dataset_train)
val_size = len(load_dataset_val)

train_loader = DataLoader(load_dataset_train, batch_size=batch_size, shuffle=True, generator=generator)
val_loader = DataLoader(load_dataset_val, batch_size=1, shuffle=True, generator=generator)



network = UNet_Encoder_Decoder(in_channel, out_channel_velo, out_channel_depth, out_channel_thickness, pic1, pic2)
# network = nn.DataParallel(network)
# network.to(device)
network = network.cuda()



loss_fn = nn.MSELoss()
# loss_fn.to(device)
loss_fn = loss_fn.cuda()


learningrate = deepcopy(learningrate_para)
optimizer = torch.optim.Adagrad(network.parameters(), lr=learningrate)



resume = False

if resume:
    checkpoint_files = os.listdir(checkpoint_dic_path)
    checkpoint_files = sorted(checkpoint_files,key=lambda x: os.path.getmtime(os.path.join(checkpoint_dic_path, x)))
    checkpoint_path = checkpoint_dic_path+'/'+checkpoint_files[-1]
    checkpoint = torch.load(checkpoint_path)
    network.load_state_dict(checkpoint['model'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    start_epoch = checkpoint['epoch']+1
    total_train_step = checkpoint['total_train_step']
    logs_path = './logs_re'
    print(' epoch {} '.format(start_epoch-1))

else:
    start_epoch = 0
    print('!')
    
# tensorboard
writer = SummaryWriter(logs_path)

script_pid = os.getpid()
print("PID:", script_pid)

logging = ''
logging = logging + 'PID:'+str(script_pid)+'\n'
logging = logging + 'epoch:'+str(epoch)+'\n'
logging = logging + 'train_size ' + str(train_size) +'\n'
logging = logging + 'val_size ' + str(val_size) +'\n'
logging_file = open(logging_path,'a')
logging_file.write(logging)
logging_file.close()

total_start_time = time.time()
for i in range(start_epoch, epoch+start_epoch):
    logging = ''
    start_time = time.time()
    print("----------{}--------".format(i))
    logging = logging + "----------{}--------".format(i) + '\n'

    network.train()
    total_train_loss1 = 0
    total_train_loss2 = 0
    total_train_loss3 = 0

    total_train_loss_all = 0
    total_train_loss_back  = 0

    for data in train_loader:
        imgs, targets = data

        imgs = imgs.cuda()
        targets = targets.cuda()

        output = network(imgs)

        tar_velo = targets[:,label_vel_idx[0]:label_vel_idx[1]]
        tar_depth = targets[:,label_dis_idx[0]:label_dis_idx[1]]
        tar_thickness = targets[:,label_thick_idx[0]:label_thick_idx[1]]

        output_velo = output[:,label_vel_idx[0]:label_vel_idx[1]]
        output_depth = output[:,label_dis_idx[0]:label_dis_idx[1]]
        output_thickness = output[:,label_thick_idx[0]:label_thick_idx[1]]

        loss1 = loss_fn(output_velo, tar_velo)
        loss2 = loss_fn(output_depth, tar_depth)
        loss3 = loss_fn(output_thickness, tar_thickness)

        # loss = loss1 + loss2 + loss3
        loss = loss_fn(output, targets)

        # loss_back = 6*loss1+loss2+loss3
        loss_back = loss_fn(output, targets)

        total_train_loss1 = total_train_loss1 + loss1.item()
        total_train_loss2 = total_train_loss2 + loss2.item()
        total_train_loss3 = total_train_loss3 + loss3.item()

        total_train_loss_all = total_train_loss_all + loss.item()
        total_train_loss_back = total_train_loss_back + loss_back.item()


        optimizer.zero_grad()
        loss_back.backward()
        optimizer.step()


    epoch_train_loss1_vel = pow(total_train_loss1/len(train_loader),0.5)/label_range_vel*modify_velocity_percent
    epoch_train_loss2_dep = pow(total_train_loss2/len(train_loader),0.5)/label_range_dep*range_660
    epoch_train_loss3_thi = pow(total_train_loss3/len(train_loader),0.5)/label_range_dep*range_660

    epoch_train_loss1 = pow(total_train_loss1/len(train_loader),0.5)
    epoch_train_loss2 = pow(total_train_loss2/len(train_loader),0.5)
    epoch_train_loss3 = pow(total_train_loss3/len(train_loader),0.5)
    epoch_train_loss_all = pow(total_train_loss_all/len(train_loader),0.5)
    epoch_train_loss_back = pow(total_train_loss_back/len(train_loader),0.5)

    logging = logging + "loss1:{}".format(epoch_train_loss1) + '\n'
    logging = logging + "loss2:{}".format(epoch_train_loss2) + '\n'
    logging = logging + "loss3:{}".format(epoch_train_loss3) + '\n'
    logging = logging + "loss_all:{}".format(epoch_train_loss_all) + '\n'
    logging = logging + "loss_back:{}".format(epoch_train_loss_back) + '\n'

    logging = logging + "loss1_vel:{}".format(epoch_train_loss1_vel) + '\n'
    logging = logging + "loss2_dep:{}".format(epoch_train_loss2_dep) + '\n'
    logging = logging + "loss3_thi:{}".format(epoch_train_loss3_thi) + '\n'

    writer.add_scalar("train_loss1", epoch_train_loss1, total_train_step)
    writer.add_scalar("train_loss2", epoch_train_loss2, total_train_step)
    writer.add_scalar("train_loss3", epoch_train_loss3, total_train_step)
    writer.add_scalar("train_loss_all", epoch_train_loss_all, total_train_step)
    writer.add_scalar("train_loss_back", epoch_train_loss_back, total_train_step)

    writer.add_scalar("train_loss1_vel", epoch_train_loss1_vel, total_train_step)
    writer.add_scalar("train_loss2_dep", epoch_train_loss2_dep, total_train_step)
    writer.add_scalar("train_loss3_thi", epoch_train_loss3_thi, total_train_step)

    network.eval()
    total_val_loss1 = 0
    total_val_loss2 = 0
    total_val_loss3 = 0

    total_val_loss_all = 0

    record = 0
    with torch.no_grad():
        for data in val_loader:
            imgs, targets= data

            imgs = imgs.cuda()
            targets = targets.cuda()

            output = network(imgs)

            tar_velo = targets[:,label_vel_idx[0]:label_vel_idx[1]]
            tar_depth = targets[:,label_dis_idx[0]:label_dis_idx[1]]
            tar_thickness = targets[:,label_thick_idx[0]:label_thick_idx[1]]

            output_velo = output[:,label_vel_idx[0]:label_vel_idx[1]]
            output_depth = output[:,label_dis_idx[0]:label_dis_idx[1]]
            output_thickness = output[:,label_thick_idx[0]:label_thick_idx[1]]

            loss1 = loss_fn(output_velo, tar_velo)
            total_val_loss1 = total_val_loss1 + loss1.item()
            loss2 = loss_fn(output_depth, tar_depth)
            total_val_loss2 = total_val_loss2 + loss2.item()
            loss3 = loss_fn(output_thickness, tar_thickness)
            total_val_loss3 = total_val_loss3 + loss3.item()

            loss = loss_fn(output, targets)
            # loss = loss1 + loss2 + loss3
            total_val_loss_all = total_val_loss_all + loss.item()

            if record<3:
                logging = logging + "record:{}".format(record) + '\n'
                logging = logging + "vp_t:"
                tar_velo_r = deepcopy(tar_velo.squeeze(dim=0).tolist())
                tar_velo_r_txt = ''
                for record_i in range(len(tar_velo_r)):
                    tar_velo_r_txt = tar_velo_r_txt + str(tar_velo_r[record_i])+','
                logging = logging + tar_velo_r_txt
                logging = logging + '\n'
                logging = logging + "vp_o:"
                output_velo_r = deepcopy(output_velo.squeeze(dim=0).tolist())
                output_velo_r_txt = ''
                for record_i in range(len(output_velo_r)):
                    output_velo_r_txt = output_velo_r_txt + str(output_velo_r[record_i])+','
                logging = logging + output_velo_r_txt
                logging = logging + '\n'
                logging = logging + "diff:"
                diff_txt = ''
                for record_i in range(len(output_velo_r)):
                    diff_txt = diff_txt + str(output_velo_r[record_i]-tar_velo_r[record_i])+','
                logging = logging + diff_txt
                logging = logging + '\n'
                logging = logging + "de_t:"
                tar_depth_r = deepcopy(tar_depth.squeeze(dim=0).tolist())
                tar_depth_r_txt = ''
                for record_i in range(len(tar_depth_r)):
                    tar_depth_r_txt = tar_depth_r_txt + str(tar_depth_r[record_i]*range_660/label_range_dep+disc_660)+','
                logging = logging + tar_depth_r_txt
                logging = logging + '\n'
                logging = logging + "de_o:"
                output_depth_r = deepcopy(output_depth.squeeze(dim=0).tolist())
                output_depth_r_txt = ''
                for record_i in range(len(output_depth_r)):
                    output_depth_r_txt = output_depth_r_txt + str(output_depth_r[record_i]*range_660/label_range_dep+disc_660)+','
                logging = logging + output_depth_r_txt
                logging = logging + '\n'

                logging = logging + "thick_t:"
                tar_thickness_r = deepcopy(tar_thickness.squeeze(dim=0).tolist())
                tar_thickness_r_txt = ''
                for record_i in range(len(tar_thickness_r)):
                    tar_thickness_r_txt = tar_thickness_r_txt + str(tar_thickness_r[record_i]*range_660/label_range_dep+range_660)+','
                logging = logging + tar_thickness_r_txt
                logging = logging + '\n'
                logging = logging + "thick_o:"
                output_thickness_r = deepcopy(output_thickness.squeeze(dim=0).tolist())
                output_thickness_r_txt = ''
                for record_i in range(len(output_thickness_r)):
                    output_thickness_r_txt = output_thickness_r_txt + str(output_thickness_r[record_i]*range_660/label_range_dep+range_660)+','
                logging = logging + output_thickness_r_txt
                logging = logging + '\n'
            
            record +=1

    val_loss1_vel = pow(total_val_loss1/len(val_loader),0.5)/label_range_vel*modify_velocity_percent
    val_loss2_dep = pow(total_val_loss2/len(val_loader),0.5)/label_range_dep*range_660
    val_loss3_thi = pow(total_val_loss3/len(val_loader),0.5)/label_range_dep*range_660

    val_loss1 = pow(total_val_loss1/len(val_loader),0.5)
    val_loss2 = pow(total_val_loss2/len(val_loader),0.5)
    val_loss3 = pow(total_val_loss3/len(val_loader),0.5)
    val_loss_all = pow(total_val_loss_all/len(val_loader),0.5)

    logging = logging + "loss1:{}".format(val_loss1) + '\n'
    writer.add_scalar("validate_loss1", val_loss1, total_train_step)
    logging = logging + "loss2:{}".format(val_loss2) + '\n'
    writer.add_scalar("validate_loss2", val_loss2, total_train_step)
    logging = logging + "loss3:{}".format(val_loss3) + '\n'
    writer.add_scalar("validate_loss3", val_loss3, total_train_step)

    logging = logging + "loss_all:{}".format(val_loss_all) + '\n'
    writer.add_scalar("validate_loss_all", val_loss_all, total_train_step)

    logging = logging + "loss1_vel:{}".format(val_loss1_vel) + '\n'
    writer.add_scalar("validate_loss1_vel", val_loss1_vel, total_train_step)
    logging = logging + "loss2_dep:{}".format(val_loss2_dep) + '\n'
    writer.add_scalar("validate_loss2_dep", val_loss2_dep, total_train_step)
    logging = logging + "loss3_thi:{}".format(val_loss3_thi) + '\n'
    writer.add_scalar("validate_loss3_thi", val_loss3_thi, total_train_step)

    if (i) % 10 == 0:
        torch.save(network.state_dict(), pre_model_dic_path+'/inversion_model_{}_epoch{}.pth'.format(time.strftime('%m%d%H%M%S', time.localtime()), i))

    # 断点保存
    if (i) % 100 == 0:
        checkpoint = {
            'epoch' : i,
            'model' : network.state_dict(),
            'optimizer' : optimizer.state_dict(),
            'total_train_step' : total_train_step,
        }
        torch.save(checkpoint, checkpoint_save_dic_path+'/checkpoint_epoch'+'_'+time.strftime('%m%d%H%M%S', time.localtime())+'_'+str(i)+'.pth.tar')
        print("{}".format(i))

    if i == epoch+start_epoch-1:
        torch.save(network.state_dict(), pre_model_dic_path+'/inversion_model_{}_epoch{}.pth'.format(time.strftime('%m%d%H%M%S', time.localtime()), i))
        checkpoint = {
            'epoch' : i,
            'model' : network.state_dict(),
            'optimizer' : optimizer.state_dict(),
            'total_train_step' : total_train_step,
        }
        torch.save(checkpoint, checkpoint_save_dic_path+'/checkpoint_epoch'+'_'+time.strftime('%m%d%H%M%S', time.localtime())+'_'+str(i)+'.pth.tar')
        print("{}".format(i))

    end_time = time.time()
    epoch_time = end_time - start_time
    print("time", epoch_time)
    logging = logging + "time"+str(epoch_time) +'\n'
    logging_file = open(logging_path,'a')
    logging_file.write(logging)
    logging_file.close()
    total_train_step = total_train_step + 1

total_end_time = time.time()
total_time = total_end_time - total_start_time
print("alltime", total_time)

writer.close()

