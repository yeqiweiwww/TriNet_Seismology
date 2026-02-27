
'''
'''

import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from pandas.core.frame import DataFrame
from scipy.spatial import ConvexHull
from scipy.interpolate import interp1d


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


# vel_base
def vel_base(path):
    file = open(path,'r')
    file_content = file.readlines()
    file.close()

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

def get_real_pre_model_data(pre_model_path):
    file = open(pre_model_path,'r')
    file_content = file.readlines()
    file.close()

    data_content = file_content[1:]
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


def wr_vlb_pre_file(pre, prediction_model_path):
    prediction_model_dic=pre
    prediction_model = open(prediction_model_path, 'w')
    prediction_model.write('no   depth[km]   vp[km/s]   vs[km/s]   ro[g/cm^3]   qp   qs   \n')

    for i in range(len(prediction_model_dic['no'])):
        prediction_model.write(
            str(prediction_model_dic['no'][i])+'   '+
            str(round(prediction_model_dic['depth'][i],2))+'   '+
            str(round(prediction_model_dic['vp'][i],4))+'   '+
            str(round(prediction_model_dic['vs'][i],4))+'   '+
            str(round(prediction_model_dic['ro'][i],4))+'   '+
            str(round(prediction_model_dic['qp'][i],2))+'   '+
            str(round(prediction_model_dic['qs'][i],2))+'   '+
            '\n'
            )

    prediction_model.close()




############################
############################
############################



changeindexuse1=17
changeindexuse2=31


dep660index1=22
dep660index2=23




ak135_model_dic = get_real_pre_model_data('./ak_inter.dat')
ak_dep = ak135_model_dic['depth'][dep660index1]
ak_thick = ak135_model_dic['depth'][dep660index2]-ak_dep
ak_vp = ak135_model_dic['vp'][changeindexuse1:changeindexuse2+1]

depth_intero = ak135_model_dic['depth'][changeindexuse1:dep660index1-1]
depth_intero.extend(list(np.arange(ak135_model_dic['depth'][dep660index1-1],ak135_model_dic['depth'][dep660index2+1],0.001)))
depth_intero.extend(ak135_model_dic['depth'][dep660index2+1:changeindexuse2+1])

f = interp1d(ak135_model_dic['depth'][changeindexuse1:changeindexuse2+1], ak135_model_dic['vp'][changeindexuse1:changeindexuse2+1], kind='linear')
ak_vp_inter = list(f(depth_intero))


compare_model_dic = get_real_pre_model_data('./all_medi.dat')
com_dep = compare_model_dic['depth'][dep660index1]
com_dep1 = compare_model_dic['depth'][dep660index2]
com_thick = compare_model_dic['depth'][dep660index2]-com_dep
com_vp = compare_model_dic['vp'][changeindexuse1:changeindexuse2+1]

f = interp1d(compare_model_dic['depth'][changeindexuse1:changeindexuse2+1], compare_model_dic['vp'][changeindexuse1:changeindexuse2+1], kind='linear')
com_vp_inter = list(f(depth_intero))

files_dir = './random_real_data'
files_name = os.listdir(files_dir)

all_dep_unce = []
all_dep1_unce = []
all_thick_unce = []
all_vel_unce = []

all_dep_unce_abs = []
all_dep1_unce_abs = []
all_thick_unce_abs = []
all_vel_unce_abs = []

all_all_vel_rmse = []
all_model_rmse_loss = []

for i in range(len(files_name)):
    pre_files = os.listdir('./pre/' + files_name[i].replace('.dat',''))
    for j in range(len(pre_files)):
        pre_model_dic = get_real_pre_model_data('./pre/' + files_name[i].replace('.dat','')+'/' + pre_files[j])
        pre_dep = pre_model_dic['depth'][dep660index1]
        pre_dep1 = pre_model_dic['depth'][dep660index2]
        pre_thick = pre_model_dic['depth'][dep660index2]-pre_dep
        pre_vp = pre_model_dic['vp'][changeindexuse1:changeindexuse2+1]

        f = interp1d(pre_model_dic['depth'][changeindexuse1:changeindexuse2+1], pre_model_dic['vp'][changeindexuse1:changeindexuse2+1], kind='linear')
        pre_vp_inter = list(f(depth_intero))

        all_dep_unce.append(pre_dep-com_dep)
        all_dep1_unce.append(pre_dep1-com_dep1)
        all_thick_unce.append(pre_thick-com_thick)

        all_dep_unce_abs.append(np.abs(pre_dep-com_dep))
        all_dep1_unce_abs.append(np.abs(pre_dep1-com_dep1))
        all_thick_unce_abs.append(np.abs(pre_thick-com_thick))

        for k in range(len(pre_vp)):
            all_vel_unce.append((pre_vp[k]-com_vp[k])/ak_vp[k])
            all_vel_unce_abs.append(np.abs((pre_vp[k]-com_vp[k])/ak_vp[k]))

        all_all_vel_rmse_tmp = []
        for k in range(len(pre_vp)):
            all_all_vel_rmse_tmp.append(((pre_vp[k]-com_vp[k])/ak_vp[k])**2)
        all_all_vel_rmse.append(np.sqrt(np.mean(all_all_vel_rmse_tmp)))

        all_model_rmse_loss_tmp = [((pre_dep-com_dep)/30)**2, ((pre_thick-com_thick)/30)**2]
        for k in range(len(pre_vp)):
            all_model_rmse_loss_tmp.append(((pre_vp[k]-com_vp[k])/ak_vp[k]/0.03)**2)

        all_model_rmse_loss.append(np.sqrt(np.mean(all_model_rmse_loss_tmp)))



f = open('./get_unce.txt','w')

bin_num = 20

data = deepcopy(all_model_rmse_loss)
counts, bins = np.histogram(data, bins=bin_num)
max_index = np.argmax(counts)
max_bin_range = (bins[max_index], bins[max_index + 1])
max_freq = counts[max_index]
f.write(str((max_bin_range[0]+max_bin_range[1])/2)+','+str(np.median(data))+','+str(np.mean(data))+','+str(np.std(data))+','+str(np.percentile(data,25))+','+str(np.percentile(data,75))+','+str(np.percentile(data,75)-np.percentile(data,25))+','+str(max(data))+','+str(min(data))+'\n')

data = deepcopy(all_dep_unce)
counts, bins = np.histogram(data, bins=bin_num)
max_index = np.argmax(counts)
max_bin_range = (bins[max_index], bins[max_index + 1])
max_freq = counts[max_index]
f.write(str((max_bin_range[0]+max_bin_range[1])/2)+','+str(np.median(data))+','+str(np.mean(data))+','+str(np.std(data))+','+str(np.percentile(data,25))+','+str(np.percentile(data,75))+','+str(np.percentile(data,75)-np.percentile(data,25))+','+str(max(data))+','+str(min(data))+'\n')

data = deepcopy(all_dep_unce_abs)
counts, bins = np.histogram(data, bins=bin_num)
max_index = np.argmax(counts)
max_bin_range = (bins[max_index], bins[max_index + 1])
max_freq = counts[max_index]
f.write(str((max_bin_range[0]+max_bin_range[1])/2)+','+str(np.median(data))+','+str(np.mean(data))+','+str(np.std(data))+','+str(np.percentile(data,25))+','+str(np.percentile(data,75))+','+str(np.percentile(data,75)-np.percentile(data,25))+','+str(max(data))+','+str(min(data))+'\n')

data = deepcopy(all_dep1_unce)
counts, bins = np.histogram(data, bins=bin_num)
max_index = np.argmax(counts)
max_bin_range = (bins[max_index], bins[max_index + 1])
max_freq = counts[max_index]
f.write(str((max_bin_range[0]+max_bin_range[1])/2)+','+str(np.median(data))+','+str(np.mean(data))+','+str(np.std(data))+','+str(np.percentile(data,25))+','+str(np.percentile(data,75))+','+str(np.percentile(data,75)-np.percentile(data,25))+','+str(max(data))+','+str(min(data))+'\n')

data = deepcopy(all_dep1_unce_abs)
counts, bins = np.histogram(data, bins=bin_num)
max_index = np.argmax(counts)
max_bin_range = (bins[max_index], bins[max_index + 1])
max_freq = counts[max_index]
f.write(str((max_bin_range[0]+max_bin_range[1])/2)+','+str(np.median(data))+','+str(np.mean(data))+','+str(np.std(data))+','+str(np.percentile(data,25))+','+str(np.percentile(data,75))+','+str(np.percentile(data,75)-np.percentile(data,25))+','+str(max(data))+','+str(min(data))+'\n')

data = deepcopy(all_thick_unce)
counts, bins = np.histogram(data, bins=bin_num)
max_index = np.argmax(counts)
max_bin_range = (bins[max_index], bins[max_index + 1])
max_freq = counts[max_index]
f.write(str((max_bin_range[0]+max_bin_range[1])/2)+','+str(np.median(data))+','+str(np.mean(data))+','+str(np.std(data))+','+str(np.percentile(data,25))+','+str(np.percentile(data,75))+','+str(np.percentile(data,75)-np.percentile(data,25))+','+str(max(data))+','+str(min(data))+'\n')

data = deepcopy(all_thick_unce_abs)
counts, bins = np.histogram(data, bins=bin_num)
max_index = np.argmax(counts)
max_bin_range = (bins[max_index], bins[max_index + 1])
max_freq = counts[max_index]
f.write(str((max_bin_range[0]+max_bin_range[1])/2)+','+str(np.median(data))+','+str(np.mean(data))+','+str(np.std(data))+','+str(np.percentile(data,25))+','+str(np.percentile(data,75))+','+str(np.percentile(data,75)-np.percentile(data,25))+','+str(max(data))+','+str(min(data))+'\n')

data = deepcopy(all_vel_unce)
counts, bins = np.histogram(data, bins=bin_num)
max_index = np.argmax(counts)
max_bin_range = (bins[max_index], bins[max_index + 1])
max_freq = counts[max_index]
f.write(str((max_bin_range[0]+max_bin_range[1])/2)+','+str(np.median(data))+','+str(np.mean(data))+','+str(np.std(data))+','+str(np.percentile(data,25))+','+str(np.percentile(data,75))+','+str(np.percentile(data,75)-np.percentile(data,25))+','+str(max(data))+','+str(min(data))+'\n')

data = deepcopy(all_vel_unce_abs)
counts, bins = np.histogram(data, bins=bin_num)
max_index = np.argmax(counts)
max_bin_range = (bins[max_index], bins[max_index + 1])
max_freq = counts[max_index]
f.write(str((max_bin_range[0]+max_bin_range[1])/2)+','+str(np.median(data))+','+str(np.mean(data))+','+str(np.std(data))+','+str(np.percentile(data,25))+','+str(np.percentile(data,75))+','+str(np.percentile(data,75)-np.percentile(data,25))+','+str(max(data))+','+str(min(data))+'\n')

data = deepcopy(all_all_vel_rmse)
counts, bins = np.histogram(data, bins=bin_num)
max_index = np.argmax(counts)
max_bin_range = (bins[max_index], bins[max_index + 1])
max_freq = counts[max_index]
f.write(str((max_bin_range[0]+max_bin_range[1])/2)+','+str(np.median(data))+','+str(np.mean(data))+','+str(np.std(data))+','+str(np.percentile(data,25))+','+str(np.percentile(data,75))+','+str(np.percentile(data,75)-np.percentile(data,25))+','+str(max(data))+','+str(min(data))+'\n')



f.close()





