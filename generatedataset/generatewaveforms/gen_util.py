
'''
'''
import os
import shutil
import time
import random

from pandas.core.frame import DataFrame

def del_file(filepath, file_end):
    files_path = os.listdir(filepath)

    for i in file_end:
        for file in files_path:
            if file.endswith(i):
                os.remove(os.path.join(filepath, file))

def move_file(filepath, file_end, move_dir):
    files_path = os.listdir(filepath)

    for i in file_end:
        for file in files_path:
            if file.endswith(i):
                shutil.move(os.path.join(filepath, file), move_dir+'/'+os.path.basename(os.path.join(filepath, file)))

def mkdir(path):
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)

# def judge_filename(t, filepath):
#     file_name = os.listdir(filepath)
#     temp_t = []
#     for i in file_name:
#         temp_t.append(i.split('-')[1])
#         temp_t = list(set(temp_t))
#     for i in temp_t:
#         if temp_t == t:
#             time.sleep(int(random.random()*10)+1)
#             t = time.strftime('%m%d%H%M%S', time.localtime())
#         else:
#             continue
    
#     return '-'+t+'-'


###########################################################################################
###########################################################################################
###########################################################################################


def get_modify_model_data(modify_model_path):
    file = open(modify_model_path,'r')
    file_content = file.readlines()
    file.close

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
    }
    
    return modify_model_dic
