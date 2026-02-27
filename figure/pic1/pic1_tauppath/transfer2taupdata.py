
import numpy as np
from pandas.core.frame import DataFrame
from scipy.interpolate import interp1d



def vel_base(path):
    file = open(path,'r')
    file_content = file.readlines()
    file.close

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

def find_duplicates(lst):
    return list(set([x for x in lst if lst.count(x) > 1]))

##########################################


model = vel_base('')

depth = model['depth']
vp = model['vp']
vs = model['vs']
ro = model['ro']
qp = model['qp']
qs = model['qs']

dis_depth = find_duplicates(depth)
dis_depth.sort()

split_index = [0]

for item_dis_depth in dis_depth:
    split_index.extend([i for i, x in enumerate(depth) if x == item_dis_depth])

split_index.append(len(depth))

split_depth_all = []
split_vp_all = []
split_vs_all = []
split_ro_all = []
split_qp_all = []
split_qs_all = []


for index_split_index in range(int(len(split_index)/2)):
    split_depth_all.append(depth[split_index[index_split_index*2]:split_index[index_split_index*2+1]+1])
    split_vp_all.append(vp[split_index[index_split_index*2]:split_index[index_split_index*2+1]+1])
    split_vs_all.append(vs[split_index[index_split_index*2]:split_index[index_split_index*2+1]+1])
    split_ro_all.append(ro[split_index[index_split_index*2]:split_index[index_split_index*2+1]+1])
    split_qp_all.append(qp[split_index[index_split_index*2]:split_index[index_split_index*2+1]+1])
    split_qs_all.append(qs[split_index[index_split_index*2]:split_index[index_split_index*2+1]+1])

print(split_depth_all)

interpo = 10

interpo_depth_all = []
interpo_vp_all = []
interpo_vs_all = []
interpo_ro_all = []
interpo_qp_all = []
interpo_qs_all = []

for index_split_depth_all in range(len(split_depth_all)):
    depth_each = split_depth_all[index_split_depth_all]
    new_depth_each = []
    for index_depth_each in range(len(depth_each)-1):
        new_depth_each.append(depth_each[index_depth_each])
        while new_depth_each[-1] + interpo > depth_each[index_depth_each] and new_depth_each[-1] + interpo < depth_each[index_depth_each+1]:
            new_depth_each.append(new_depth_each[-1] + interpo)
    new_depth_each.append(depth_each[-1])

    interpo_depth_all.extend(new_depth_each)

    vp_each = split_vp_all[index_split_depth_all]
    func = interp1d(depth_each, vp_each, kind='linear')
    interpo_vp_all.extend(list(func(new_depth_each)))

    vs_each = split_vs_all[index_split_depth_all]
    func = interp1d(depth_each, vs_each, kind='linear')
    interpo_vs_all.extend(list(func(new_depth_each)))

    ro_each = split_ro_all[index_split_depth_all]
    func = interp1d(depth_each, ro_each, kind='linear')
    interpo_ro_all.extend(list(func(new_depth_each)))

    qp_each = split_qp_all[index_split_depth_all]
    func = interp1d(depth_each, qp_each, kind='linear')
    interpo_qp_all.extend(list(func(new_depth_each)))

    qs_each = split_qs_all[index_split_depth_all]
    func = interp1d(depth_each, qs_each, kind='linear')
    interpo_qs_all.extend(list(func(new_depth_each)))

print(interpo_depth_all)


f = open('','w')

f.write('modify_model_real_pre - P\nmodify_model_real_pre - S\n')

for index_depth_all in range(len(depth)):
    f.write('{:>10.3f}'.format(depth[index_depth_all])+'{:>12.4f}'.format(vp[index_depth_all])+'{:>12.4f}'.format(vs[index_depth_all])+'{:>12.4f}'.format(ro[index_depth_all])+'\n')

f.close()

