

import time
import os

##########################################################################


workspace_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
workspace_data_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) +'_data'

workspace_data_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).replace('workspace_event_20080519','data') + '/' + workspace_data_name

dl_tr_data_path = os.path.dirname(os.path.abspath(__file__)).replace('workspace_event_20080519','data/'+workspace_data_name)


train_techo_file_path = '../data/train_techo_file.dat'
val_techo_file_path = '../data/val_techo_file.dat'
test_techo_file_path = '../data/test_techo_file.dat'

checkpoint_dic_path = ''
checkpoint_save_dic_path = dl_tr_data_path + '/checkpoint'
pre_model_dic_path = dl_tr_data_path + '/model_epoch_dic'
logging_path = time.strftime('%m%d%H%M%S', time.localtime())+'.log'

test_prediction_model_path = dl_tr_data_path + '/test/prediction_model'
test_show_path = dl_tr_data_path + '/test/pre_show'
test_loss_file_path = dl_tr_data_path + '/test/test_loss.dat'

# test_prediction_model_path_one_all = './test_one_all/prediction_model'
# test_show_path_one_all = './test_one_all/pre_show'
# test_loss_file_path_one_all = './test_loss_one_all.dat'

logs_path = './logs'

vel_base_path = workspace_data_path + '/data/vel_base_model.dat'

# featmap_path = './test/featmap-gradcam++'

# test_prediction_model_path1 = './test-1/prediction_model'
# test_show_path1 = './test-1/pre_show'

###########################################################################
###########################################################################


rang_draw = [25,55]
reduction_v = 10
draw_depth = [400,1000]


###########################################################################
###########################################################################
# 

file_path = workspace_data_path + '/data/data0/modified_modelfile/'+os.listdir(workspace_data_path + '/data/data0/modified_modelfile')[0]
file = open(file_path,'r')
file_content = file.readlines()
file.close()

temp = file_content[-5].split(':')[1].split(',')[:-1]
changed_layer_no = []
for i in range(len(temp)):
    changed_layer_no.append(int(temp[i]))

changed_layer_num = len(changed_layer_no)

###########################################################################
###########################################################################
# 生成速度模型所使用的参数

vel_model_info_dic = {
    'modify_depth_layer_depth' : 660.0,
    'modify_depth_changed_range' : 30.0,
    'interpolation_start_depth' : 510.0,
    'interpolation_end_depth' : 800.0,
    'interpolation_each_layer_depth' : 20.0,
    'modify_velocity_percent' : 0.03,
    'modify_start_depth' : 510.0,
    'modify_end_depth' : 1000.0,
}


###########################################################################
###########################################################################
# 生成标签文件的参数
range_660=vel_model_info_dic['modify_depth_changed_range']
modify_velocity_percent=vel_model_info_dic['modify_velocity_percent']
disc_660=vel_model_info_dic['modify_depth_layer_depth']

label_range_vel=1
label_range_dep=1

spe_sta_loc_para = []
for j in range(41):
    spe_sta_loc_para.append(j*0.5+9.75)

loc_range_para = 0.25

loc_range_min_para = 9.5
loc_range_max_para = 30

###########################################################################
###########################################################################
# 训练文件参数

total_train_step_para = 0
epoch_para = 200
start_epoch_para = 0
batch_size_para = 16
learningrate_para = 0.001

seed_para = 3407
cuda_visible_devices_str_para = '0'