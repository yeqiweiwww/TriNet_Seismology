

import os
from pandas.core.frame import DataFrame


def get_vel_model(model_path):
    file = open(model_path,'r')
    file_content = file.readlines()
    file.close()

    data_content = file_content[1:]
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
    }

    return modify_model_dic

