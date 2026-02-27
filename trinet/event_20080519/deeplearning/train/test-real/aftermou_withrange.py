

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








changeindexuse1=17
changeindexuse2=31


dep660index1=22
dep660index2=23





model_li = vel_base('./model_li.dat')
model_ak135 = vel_base('./vel_base_model.dat')


files_dir = './random_real_data'
files_name = os.listdir(files_dir)

deldir('./pre_anl')
mkdir('./pre_anl')

# for index_file in range(len(files_name)):

#     mkdir('./pre_anl/' + files_name[index_file].replace('.dat',''))




pre_files = os.listdir('./pre/' + files_name[0].replace('.dat',''))

dic = get_real_pre_model_data('./pre/' + files_name[0].replace('.dat','')+'/' + pre_files[0])



fig1 = plt.figure(figsize=(5,10))
ax1 = fig1.add_subplot()



depth_pre_model_all_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]
vp_pre_model_all_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]
vs_pre_model_all_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]
ro_pre_model_all_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]
qp_pre_model_all_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]
qs_pre_model_all_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]

depth_intero = dic['depth'][changeindexuse1:dep660index1-1]
depth_intero.extend(list(np.arange(dic['depth'][dep660index1-1],dic['depth'][dep660index2+1],0.001)))
depth_intero.extend(dic['depth'][dep660index2+1:changeindexuse2+1])
f = interp1d(dic['depth'][changeindexuse1:changeindexuse2+1], dic['vp'][changeindexuse1:changeindexuse2+1], kind='linear')
vp_intero_up_all = list(f(depth_intero))
vp_intero_low_all = list(f(depth_intero))

dic_intero = deepcopy(dic)
dic_intero['depth'][changeindexuse1:changeindexuse2+1] = deepcopy(depth_intero)
dic_intero['no'] = [i+1 for i in range(len(dic['depth'])+len(depth_intero)-len(dic['depth'][changeindexuse1:changeindexuse2+1]))]
dic_intero['vp'][changeindexuse1:changeindexuse2+1] = list(f(depth_intero))
f = interp1d(dic['depth'][changeindexuse1:changeindexuse2+1], dic['vs'][changeindexuse1:changeindexuse2+1], kind='linear')
dic_intero['vs'][changeindexuse1:changeindexuse2+1] = list(f(depth_intero))
f = interp1d(dic['depth'][changeindexuse1:changeindexuse2+1], dic['ro'][changeindexuse1:changeindexuse2+1], kind='linear')
dic_intero['ro'][changeindexuse1:changeindexuse2+1] = list(f(depth_intero))
f = interp1d(dic['depth'][changeindexuse1:changeindexuse2+1], dic['qp'][changeindexuse1:changeindexuse2+1], kind='linear')
dic_intero['qp'][changeindexuse1:changeindexuse2+1] = list(f(depth_intero))
f = interp1d(dic['depth'][changeindexuse1:changeindexuse2+1], dic['qs'][changeindexuse1:changeindexuse2+1], kind='linear')
dic_intero['qs'][changeindexuse1:changeindexuse2+1] = list(f(depth_intero))

changeindexuse1_intero = changeindexuse1
changeindexuse2_intero = changeindexuse1_intero+len(depth_intero)-1


for index_file in range(len(files_name)):
    dic1 = get_real_pre_model_data('./pre/' + files_name[index_file].replace('.dat','')+'/' + pre_files[0])


    fig2 = plt.figure(figsize=(5,10))
    ax2 = fig2.add_subplot()

    depth_pre_model_file_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]
    vp_pre_model_file_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]
    vs_pre_model_file_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]
    ro_pre_model_file_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]
    qp_pre_model_file_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]
    qs_pre_model_file_temp=[[] for _ in range(changeindexuse2+1-changeindexuse1)]

    f = interp1d(dic1['depth'][changeindexuse1:changeindexuse2+1], dic1['vp'][changeindexuse1:changeindexuse2+1], kind='linear')
    vp_intero_up_file = list(f(depth_intero))
    vp_intero_low_file = list(f(depth_intero))

    for i in range(len(pre_files)):
        pre_files_path = './pre/' + files_name[index_file].replace('.dat','')+'/' + pre_files[i]
        pre_model_dic = get_real_pre_model_data(pre_files_path)

        ax2.plot(pre_model_dic['vp'],pre_model_dic['depth'],'green',linewidth=0.6,label='model_ak135_p_all' if i==0 else None)

        ax1.plot(pre_model_dic['vp'],pre_model_dic['depth'],'green',linewidth=0.6,label='model_ak135_p_all' if index_file==0 and i==0 else None)


        for j in range(changeindexuse2+1-changeindexuse1):

            depth_pre_model_file_temp[j].append(pre_model_dic['depth'][changeindexuse1:changeindexuse2+1][j])
            vp_pre_model_file_temp[j].append(pre_model_dic['vp'][changeindexuse1:changeindexuse2+1][j])
            vs_pre_model_file_temp[j].append(pre_model_dic['vs'][changeindexuse1:changeindexuse2+1][j])
            ro_pre_model_file_temp[j].append(pre_model_dic['ro'][changeindexuse1:changeindexuse2+1][j])
            qp_pre_model_file_temp[j].append(pre_model_dic['qp'][changeindexuse1:changeindexuse2+1][j])
            qs_pre_model_file_temp[j].append(pre_model_dic['qs'][changeindexuse1:changeindexuse2+1][j])

            depth_pre_model_all_temp[j].append(pre_model_dic['depth'][changeindexuse1:changeindexuse2+1][j])
            vp_pre_model_all_temp[j].append(pre_model_dic['vp'][changeindexuse1:changeindexuse2+1][j])
            vs_pre_model_all_temp[j].append(pre_model_dic['vs'][changeindexuse1:changeindexuse2+1][j])
            ro_pre_model_all_temp[j].append(pre_model_dic['ro'][changeindexuse1:changeindexuse2+1][j])
            qp_pre_model_all_temp[j].append(pre_model_dic['qp'][changeindexuse1:changeindexuse2+1][j])
            qs_pre_model_all_temp[j].append(pre_model_dic['qs'][changeindexuse1:changeindexuse2+1][j])

        f = interp1d(pre_model_dic['depth'][changeindexuse1:changeindexuse2+1], pre_model_dic['vp'][changeindexuse1:changeindexuse2+1], kind='linear')
        vp_intero_temp = f(depth_intero)
        for j in range(len(depth_intero)):
            if vp_intero_temp[j] > vp_intero_up_file[j]:
                vp_intero_up_file[j] = deepcopy(vp_intero_temp[j])
            if vp_intero_temp[j] < vp_intero_low_file[j]:
                vp_intero_low_file[j] = deepcopy(vp_intero_temp[j])
            if vp_intero_temp[j] > vp_intero_up_all[j]:
                vp_intero_up_all[j] = deepcopy(vp_intero_temp[j])
            if vp_intero_temp[j] < vp_intero_low_all[j]:
                vp_intero_low_all[j] = deepcopy(vp_intero_temp[j])

    depth_pre_model_file_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
    vp_pre_model_file_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
    vs_pre_model_file_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
    ro_pre_model_file_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
    qp_pre_model_file_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
    qs_pre_model_file_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]

    for i in range(changeindexuse2+1-changeindexuse1):
        depth_pre_model_file_mean[i] = np.mean(depth_pre_model_file_temp[i])
        vp_pre_model_file_mean[i] = np.mean(vp_pre_model_file_temp[i])
        vs_pre_model_file_mean[i] = np.mean(vs_pre_model_file_temp[i])
        ro_pre_model_file_mean[i] = np.mean(ro_pre_model_file_temp[i])
        qp_pre_model_file_mean[i] = np.mean(qp_pre_model_file_temp[i])
        qs_pre_model_file_mean[i] = np.mean(qs_pre_model_file_temp[i])

    pre_dic_file_mean = deepcopy(dic)
    pre_dic_file_mean['depth'][changeindexuse1:changeindexuse2+1] = depth_pre_model_file_mean
    pre_dic_file_mean['vp'][changeindexuse1:changeindexuse2+1] = vp_pre_model_file_mean
    pre_dic_file_mean['vs'][changeindexuse1:changeindexuse2+1] = vs_pre_model_file_mean
    pre_dic_file_mean['ro'][changeindexuse1:changeindexuse2+1] = ro_pre_model_file_mean
    pre_dic_file_mean['qp'][changeindexuse1:changeindexuse2+1] = qp_pre_model_file_mean
    pre_dic_file_mean['qs'][changeindexuse1:changeindexuse2+1] = qs_pre_model_file_mean

    wr_vlb_pre_file(pre_dic_file_mean, './pre_anl/' + files_name[index_file].replace('.dat','_mean.dat'))

    depth_pre_model_file_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
    vp_pre_model_file_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
    vs_pre_model_file_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
    ro_pre_model_file_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
    qp_pre_model_file_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
    qs_pre_model_file_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]

    for i in range(changeindexuse2+1-changeindexuse1):
        depth_pre_model_file_medi[i] = np.median(depth_pre_model_file_temp[i])
        vp_pre_model_file_medi[i] = np.median(vp_pre_model_file_temp[i])
        vs_pre_model_file_medi[i] = np.median(vs_pre_model_file_temp[i])
        ro_pre_model_file_medi[i] = np.median(ro_pre_model_file_temp[i])
        qp_pre_model_file_medi[i] = np.median(qp_pre_model_file_temp[i])
        qs_pre_model_file_medi[i] = np.median(qs_pre_model_file_temp[i])

    pre_dic_file_medi = deepcopy(dic)
    pre_dic_file_medi['depth'][changeindexuse1:changeindexuse2+1] = depth_pre_model_file_mean
    pre_dic_file_medi['vp'][changeindexuse1:changeindexuse2+1] = vp_pre_model_file_mean
    pre_dic_file_medi['vs'][changeindexuse1:changeindexuse2+1] = vs_pre_model_file_mean
    pre_dic_file_medi['ro'][changeindexuse1:changeindexuse2+1] = ro_pre_model_file_mean
    pre_dic_file_medi['qp'][changeindexuse1:changeindexuse2+1] = qp_pre_model_file_mean
    pre_dic_file_medi['qs'][changeindexuse1:changeindexuse2+1] = qs_pre_model_file_mean

    wr_vlb_pre_file(pre_dic_file_medi, './pre_anl/' + files_name[index_file].replace('.dat','_medi.dat'))

    pre_dic_up_file = deepcopy(dic_intero)
    pre_dic_up_file['vp'][changeindexuse1_intero:changeindexuse2_intero+1] = deepcopy(vp_intero_up_file)
    wr_vlb_pre_file(pre_dic_up_file, './pre_anl/' + files_name[index_file].replace('.dat','_up.dat'))



    pre_dic_low_file = deepcopy(dic_intero)
    pre_dic_low_file['vp'][changeindexuse1_intero:changeindexuse2_intero+1] = deepcopy(vp_intero_low_file)
    wr_vlb_pre_file(pre_dic_low_file, './pre_anl/' + files_name[index_file].replace('.dat','_low.dat'))


    ax2.plot(pre_dic_up_file['vp'],pre_dic_up_file['depth'],'yellow',linewidth=0.6,label='up')
    ax2.plot(pre_dic_low_file['vp'],pre_dic_low_file['depth'],'yellow',linewidth=0.6,label='low')


    ax2.plot(model_ak135['vp'],model_ak135['depth'],'black',linewidth=0.6,label='model_ak135')
    ax2.plot(pre_dic_file_mean['vp'],pre_dic_file_mean['depth'],'blue',linewidth=0.6,label='pre_mean')
    ax2.plot(pre_dic_file_medi['vp'],pre_dic_file_medi['depth'],'red',linewidth=0.6,label='pre_medi')

    ax2.set_ylim(410,1000)

    ax2.invert_yaxis()
    ax2.legend()
    fig2.savefig('./pre_anl/' + files_name[index_file].replace('.dat','.svg'))
    plt.close(fig2)



depth_pre_model_all_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
vp_pre_model_all_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
vs_pre_model_all_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
ro_pre_model_all_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
qp_pre_model_all_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
qs_pre_model_all_mean=[0 for _ in range(changeindexuse2+1-changeindexuse1)]

for i in range(changeindexuse2+1-changeindexuse1):
    depth_pre_model_all_mean[i] = np.mean(depth_pre_model_all_temp[i])
    vp_pre_model_all_mean[i] = np.mean(vp_pre_model_all_temp[i])
    vs_pre_model_all_mean[i] = np.mean(vs_pre_model_all_temp[i])
    ro_pre_model_all_mean[i] = np.mean(ro_pre_model_all_temp[i])
    qp_pre_model_all_mean[i] = np.mean(qp_pre_model_all_temp[i])
    qs_pre_model_all_mean[i] = np.mean(qs_pre_model_all_temp[i])


pre_dic_all_mean = deepcopy(dic)
pre_dic_all_mean['depth'][changeindexuse1:changeindexuse2+1] = depth_pre_model_all_mean
pre_dic_all_mean['vp'][changeindexuse1:changeindexuse2+1] = vp_pre_model_all_mean
pre_dic_all_mean['vs'][changeindexuse1:changeindexuse2+1] = vs_pre_model_all_mean
pre_dic_all_mean['ro'][changeindexuse1:changeindexuse2+1] = ro_pre_model_all_mean
pre_dic_all_mean['qp'][changeindexuse1:changeindexuse2+1] = qp_pre_model_all_mean
pre_dic_all_mean['qs'][changeindexuse1:changeindexuse2+1] = qs_pre_model_all_mean


wr_vlb_pre_file(pre_dic_all_mean, './all_mean.dat')

depth_pre_model_all_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
vp_pre_model_all_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
vs_pre_model_all_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
ro_pre_model_all_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
qp_pre_model_all_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]
qs_pre_model_all_medi=[0 for _ in range(changeindexuse2+1-changeindexuse1)]

for i in range(changeindexuse2+1-changeindexuse1):
    depth_pre_model_all_medi[i] = np.median(depth_pre_model_all_temp[i])
    vp_pre_model_all_medi[i] = np.median(vp_pre_model_all_temp[i])
    vs_pre_model_all_medi[i] = np.median(vs_pre_model_all_temp[i])
    ro_pre_model_all_medi[i] = np.median(ro_pre_model_all_temp[i])
    qp_pre_model_all_medi[i] = np.median(qp_pre_model_all_temp[i])
    qs_pre_model_all_medi[i] = np.median(qs_pre_model_all_temp[i])


pre_dic_all_medi = deepcopy(dic)
pre_dic_all_medi['depth'][changeindexuse1:changeindexuse2+1] = depth_pre_model_all_medi
pre_dic_all_medi['vp'][changeindexuse1:changeindexuse2+1] = vp_pre_model_all_medi
pre_dic_all_medi['vs'][changeindexuse1:changeindexuse2+1] = vs_pre_model_all_medi
pre_dic_all_medi['ro'][changeindexuse1:changeindexuse2+1] = ro_pre_model_all_medi
pre_dic_all_medi['qp'][changeindexuse1:changeindexuse2+1] = qp_pre_model_all_medi
pre_dic_all_medi['qs'][changeindexuse1:changeindexuse2+1] = qs_pre_model_all_medi


wr_vlb_pre_file(pre_dic_all_medi, './all_medi.dat')



pre_dic_up_all = deepcopy(dic_intero)
pre_dic_up_all['vp'][changeindexuse1_intero:changeindexuse2_intero+1] = deepcopy(vp_intero_up_all)
wr_vlb_pre_file(pre_dic_up_all, './all_up.dat')



pre_dic_low_all = deepcopy(dic_intero)
pre_dic_low_all['vp'][changeindexuse1_intero:changeindexuse2_intero+1] = deepcopy(vp_intero_low_all)
wr_vlb_pre_file(pre_dic_low_all, './all_low.dat')

ax1.plot(pre_dic_up_all['vp'],pre_dic_up_all['depth'],'yellow',linewidth=0.6,label='up')
ax1.plot(pre_dic_low_all['vp'],pre_dic_low_all['depth'],'yellow',linewidth=0.6,label='low')

ax1.plot(model_ak135['vp'],model_ak135['depth'],'black',linewidth=0.6,label='model_ak135')
ax1.plot(pre_dic_all_mean['vp'],pre_dic_all_mean['depth'],'blue',linewidth=0.6,label='pre_mean')
ax1.plot(pre_dic_all_medi['vp'],pre_dic_all_medi['depth'],'red',linewidth=0.6,label='pre_medi')

ax1.set_ylim(410,1000)

ax1.invert_yaxis()
ax1.legend()
fig1.savefig('./all.svg')
plt.close(fig1)



print('Done')