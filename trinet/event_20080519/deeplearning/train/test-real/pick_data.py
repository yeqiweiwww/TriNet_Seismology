

'''
'''

import os
import shutil
import sys
import random
from copy import deepcopy

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

def get_real_rebuild_data(path):
    file = open(path, 'r')
    file_content = file.readlines()
    file.close()

    pro_time = []
    pro_vp_data = []
    for i in range(len(file_content)-4):
        if i%2 == 0:
            pro_time.append([])
            for j in range(len(file_content[i].split())-1):
                pro_time[int(i/2)].append(float(file_content[i].split()[j+1]))
        else:
            pro_vp_data.append([])
            for j in range(len(file_content[i].split())-1):
                pro_vp_data[int(i/2-0.5)].append(float(file_content[i].split()[j+1]))
    
    temp = file_content[-2]
    temp_t = temp.split(':')[1].split(',')[:-1]
    use_index = []
    for i in range(len(temp_t)):
        use_index.append(int(temp_t[i]))
    
    temp = file_content[-4]
    temp_t = temp.split(':')[1].split(',')[:-1]
    sta_location = []
    for i in range(len(temp_t)):
        sta_location.append(float(temp_t[i]))

    return pro_vp_data, use_index, sta_location, pro_time

#######################################################
#######################################################
#######################################################

deldir('./random_real_data')
mkdir('./random_real_data')

pro_vp_data, use_index, sta_location, pro_time = get_real_rebuild_data('./rebuild-data_all.dat')

spe_sta_loc_range = []
for i in range(42):
    spe_sta_loc_range.append(i*0.5+9.5)

class_sta = []
for i in range(len(spe_sta_loc_range)-1):
    class_sta.append([])
    for j in range(len(sta_location)):
        if sta_location[j] < spe_sta_loc_range[i+1] and sta_location[j] >= spe_sta_loc_range[i]:
            class_sta[i].append(j)
class_sta_no_empty = [item for item in class_sta if item]
#######################################################


sta_num = 31
pick_sta_ratio = 0.5
epoch_all = 100

#######################################################

if sta_num > len(class_sta_no_empty):
    print('The ratio of station is too large! The largest station number is '+str(len(class_sta_no_empty))+'.')
    sys.exit()

spe_sta_loc_use = []
for i in range(41):
    spe_sta_loc_use.append(i*0.5+9.75)

epoch = 0
while epoch < epoch_all:
    re_re_sta = deepcopy(spe_sta_loc_use)
    re_re_pro = [[0] * len(pro_vp_data[0]) for _ in range(len(spe_sta_loc_use))]
    re_re_time = [pro_time[0] for _ in range(len(spe_sta_loc_use))]
    re_re_use = []

    non_empty_indices = [i for i, sub in enumerate(class_sta) if sub]

    chosen_indices = random.sample(non_empty_indices, sta_num)

    re_indices = []
    for i, sub in enumerate(class_sta):
        if i in chosen_indices:

            re_indices.append(random.choice(sub))
        else:

            re_indices.append([])

    for i in range(len(re_indices)):
        if re_indices[i] == []:
            pass
        else:
            re_re_sta[i] = sta_location[re_indices[i]]
            re_re_pro[i] = pro_vp_data[re_indices[i]]
            re_re_use.append(i)


    f = open('./random_real_data/'+'re_data'+str(epoch)+'.dat', 'w')

    for j in range(len(re_re_time)):
        f.write('T_sec   ')
        for k in range(len(re_re_time[0])):
            f.write(str(re_re_time[j][k])+'   ')
        f.write('\n')
        f.write('U'+str(j)+'   ')
        for k in range(len(re_re_pro[j])):
            f.write(str(re_re_pro[j][k])+'   ')
        f.write('\n')
    re_re_sta_str = ''
    for j in range(len(re_re_sta)):
        re_re_sta_str = re_re_sta_str + str(re_re_sta[j]) + ','
    f.write('sta_location:'+re_re_sta_str)
    f.write('\n')
    f.write('rebuild_index:0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,')
    f.write('\n')
    use_index_str = ''
    for j in range(len(re_re_use)):
        use_index_str = use_index_str + str(re_re_use[j]) + ','
    f.write('use_index:'+use_index_str)
    f.write('\n')
    f.write('cut_start_time:20---cut_windows:35---reduction_v:10')
    f.close()
    epoch = epoch + 1