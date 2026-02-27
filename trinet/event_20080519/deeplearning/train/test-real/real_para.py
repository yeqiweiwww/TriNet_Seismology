

import time
import torchvision
import os


vel_base_path = ''

####################################
####################################
####################################

changed_layer_num=15
rang_draw = [20,55]
reduction_v = 10
draw_depth = [300,1000]

range_660=30
modify_velocity_percent=0.03
label_range_vel=1
label_range_dep=1
disc_660=660


velocity_model_info_dic = {
    'modify_depth_layer_depth' : 660.0,
    'modify_depth_changed_range' : 30.0,
    'interpolation_start_depth' : 510.0,
    'interpolation_end_depth' : 800.0,
    'interpolation_each_layer_depth' : 20.0,
    'modify_velocity_percent' : 0.03,
    'modify_start_depth' : 510.0,
    'modify_end_depth' : 1000.0,
}

##############
spe_sta_loc_para = []
for j in range(41):
    spe_sta_loc_para.append(j*0.5+9.75)

loc_range_para = 0.25

loc_range_min_para = 9.5
loc_range_max_para = 30.0

seed_para = 3407
cuda_visible_devices_str_para = '0'