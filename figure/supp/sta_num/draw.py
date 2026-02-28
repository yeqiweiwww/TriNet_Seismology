

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from copy import deepcopy
from pandas.core.frame import DataFrame
from matplotlib.lines import Line2D

##########################################################

def get_rebuild_data(path):
    file = open(path, 'r')
    file_content = file.readlines()
    file.close()

    pro_time = []
    pro_vp_data = []
    for i in range(len(file_content)-9):
        if i%2 == 0:
            pro_time.append([])
            for j in range(len(file_content[i].split())-1):
                pro_time[int(i/2)].append(float(file_content[i].split()[j+1]))
        else:
            pro_vp_data.append([])
            for j in range(len(file_content[i].split())-1):
                pro_vp_data[int(i/2-0.5)].append(float(file_content[i].split()[j+1]))

    temp = file_content[-7]
    temp_t = temp.split(':')[1].split(',')[:-1]
    use_index = []
    for i in range(len(temp_t)):
        use_index.append(float(temp_t[i]))

    temp = file_content[-6]
    temp_t = temp.split(':')[1].split(',')[:-1]
    sta_location = []
    for i in range(len(temp_t)):
        sta_location.append(float(temp_t[i]))
        
    return pro_time, pro_vp_data, sta_location, use_index

def get_ak_vel_model(path):
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

def get_modi_vel_model(path):
    file = open(path,'r')
    file_content = file.readlines()
    file.close

    data_content = file_content[1:-6]
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

def get_pre_vel_model(path):
    file = open(path,'r')
    file_content = file.readlines()
    file.close

    data_content = file_content[1:-16]
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

##########################################################


cut_time_start_time = 15
cut_time_windows = 40
reduction_v = 10

##########################################################

font_path = '../../fonts/timesnewroman/times.ttf'
fm.fontManager.addfont(font_path)


plt.rcParams['font.family'] = 'Times New Roman'


plt.rcParams['font.size'] = 10
# plt.rcParams['axes.titlesize'] = 12
# plt.rcParams['axes.labelsize'] = 10
# plt.rcParams['xtick.labelsize'] = 10
# plt.rcParams['ytick.labelsize'] = 10
# plt.rcParams['legend.fontsize'] = 12

plt.rcParams['svg.fonttype'] = 'none'

reduction_v_para = 10
cut_time_start_time_para = 15
cut_time_windows_para = 40


figsize_para=(8, 5)

draw_depth_para = [400, 1000]

inp_lin_type = '-'
inp_lin_color = 'black'
inp_lin_seis_wid = 1
inp_lin_dashes = []
modi_lin_type = '-'
modi_lin_color = (66/255, 133/255, 244/255)
modi_lin_model_wid = 1.3
modi_lin_seis_wid = 1
modi_lin_dashes = []
pre_lin_type = '-'
pre_lin_color = (219/255, 68/255, 55/255)
pre_lin_model_wid = 1.3
pre_lin_seis_wid = 1
pre_lin_dashes = []



handlelength=3
handletextpad=0.6
##########################################################
ak135_file_path = '../ak135.dat'

ak135_vel_dic = get_ak_vel_model(ak135_file_path)

modi_vel_file_path = './modify_model_stacou031.dat'

rebuild_seis_file_path = './rebuild_vp_seis_stacou031.dat'
non_rebuild_seis_file_path = './rebuild_vp_seis_stacou031_non.dat'

modi_vel_dic = get_modi_vel_model(modi_vel_file_path)

rebui_time, rebui_vp_data, rebui_sta_location, rebui_use_index = get_rebuild_data(rebuild_seis_file_path)
non_rebui_time, non_rebui_vp_data, non_rebui_sta_location, non_rebui_use_index = get_rebuild_data(non_rebuild_seis_file_path)

locdata = rebui_sta_location

draw_modi_vel_depth = []
draw_modi_vel_vp = []
for i in range(len(modi_vel_dic['depth'])):
    if modi_vel_dic['depth'][i]>draw_depth_para[0] and modi_vel_dic['depth'][i]<draw_depth_para[1]:
        draw_modi_vel_depth.append(modi_vel_dic['depth'][i])
        draw_modi_vel_vp.append(modi_vel_dic['vp'][i])

draw_rebui = []
for i in range(len(rebui_vp_data)):
    draw_rebui.append([])
    for j in range(len(rebui_vp_data[i])):
        draw_rebui[-1].append(rebui_vp_data[i][j]/2+locdata[i])

draw_non_rebui = []
for i in range(len(non_rebui_vp_data)):
    draw_non_rebui.append([])
    for j in range(len(non_rebui_vp_data[i])):
        draw_non_rebui[-1].append(non_rebui_vp_data[i][j]/2+locdata[i])


##########################################################
pre_vel_file_path = './pre_model_stacou007.dat'

input_seis_file_path = './rebuild_vp_seis_stacou007.dat'
pre_rebuild_seis_file_path = './rebuild_vp_seis_stacou007_re.dat'

pre_vel_dic = get_pre_vel_model(pre_vel_file_path)

inp_rebui_time, inp_rebui_vp_data, inp_rebui_sta_location, inp_rebui_use_index = get_rebuild_data(input_seis_file_path)
pre_rebui_time, pre_rebui_vp_data, pre_rebui_sta_location, pre_rebui_use_index = get_rebuild_data(pre_rebuild_seis_file_path)

draw_pre_vel_depth = []
draw_pre_vel_vp = []
for i in range(len(pre_vel_dic['depth'])):
    if pre_vel_dic['depth'][i]>draw_depth_para[0] and pre_vel_dic['depth'][i]<draw_depth_para[1]:
        draw_pre_vel_depth.append(pre_vel_dic['depth'][i])
        draw_pre_vel_vp.append(pre_vel_dic['vp'][i])

draw_inp_rebui = []
for i in range(len(inp_rebui_vp_data)):
    draw_inp_rebui.append([])
    for j in range(len(inp_rebui_vp_data[i])):
        draw_inp_rebui[-1].append(inp_rebui_vp_data[i][j]/2+locdata[i])

draw_pre_rebui = []
for i in range(len(pre_rebui_vp_data)):
    draw_pre_rebui.append([])
    for j in range(len(pre_rebui_vp_data[i])):
        draw_pre_rebui[-1].append(pre_rebui_vp_data[i][j]/2+locdata[i])


fig = plt.figure(figsize=figsize_para,dpi=900)
gs = fig.add_gridspec(1, 5)

ax1 = fig.add_subplot(gs[:,0:2])
ax2 = fig.add_subplot(gs[:,2])
ax3 = fig.add_subplot(gs[:,3:5])


for i in range(len(draw_inp_rebui)):
    if i in inp_rebui_use_index:
        ax1.plot(rebui_time[i], draw_inp_rebui[i], color=inp_lin_color, linestyle=inp_lin_type, dashes=inp_lin_dashes, linewidth=inp_lin_seis_wid)


ax1.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax1.set_ylim(9,31)
ax1.set_yticks([10, 20, 30])
ax1.set_ylabel('Distance (deg)')
ax1.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')
ax1.text(34, 29.5, 'Station Count:7', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))


ax1.set_title('Input Seismic Waveform')



ax2.plot(draw_modi_vel_vp, draw_modi_vel_depth, color=modi_lin_color, linestyle=modi_lin_type, dashes=modi_lin_dashes, linewidth=modi_lin_model_wid, label='modi', zorder=2)
ax2.plot(draw_pre_vel_vp, draw_pre_vel_depth, color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_model_wid, label='pre', zorder=3)

idx_b=17
idx_e=31
idx_6601=22
idx_6602=23

ak_vp=ak135_vel_dic['vp'][idx_b:idx_e+1]
ak6601=ak135_vel_dic['depth'][idx_6601]
ak6602=ak135_vel_dic['depth'][idx_6602]
akthi=ak6602-ak6601
modi_vp=modi_vel_dic['vp'][idx_b:idx_e+1]
modi6601=modi_vel_dic['depth'][idx_6601]
modi6602=modi_vel_dic['depth'][idx_6602]
modithi=modi6602-modi6601
pre_vp=pre_vel_dic['vp'][idx_b:idx_e+1]
pre6601=pre_vel_dic['depth'][idx_6601]
pre6602=pre_vel_dic['depth'][idx_6602]
prethi=pre6602-pre6601

all_loss = []
for i in range(len(modi_vp)):
    all_loss.append(((pre_vp[i]-modi_vp[i])/ak_vp[i]/0.03)**2)

all_loss.append(((pre6601-modi6601)/30)**2)
all_loss.append(((prethi-modithi)/30)**2)

all_loss = np.sqrt(np.mean(all_loss))

ax2.text(10.1, 445, 'Loss:\n'+f"{all_loss:.3f}", fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))

ax2.invert_yaxis()
ax2.set_ylabel('Depth (km)')
ax2.set_xlabel('Vp (km/s)')
ax2.set_title('Velocity Model')


for i in range(len(draw_non_rebui)):
    ax3.plot(rebui_time[i], draw_non_rebui[i], color=modi_lin_color, linestyle=modi_lin_type, dashes=modi_lin_dashes, linewidth=modi_lin_seis_wid)

for i in range(len(draw_pre_rebui)):
    ax3.plot(rebui_time[i], draw_pre_rebui[i], color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_seis_wid)



ax3.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax3.set_ylim(9,31)
ax3.set_yticks([10, 20, 30])
ax3.set_ylabel('Distance (deg)')
ax3.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')

ax3.set_title('Seismic Waveform')


handles = [
    Line2D([0], [0], color=modi_lin_color, linestyle=modi_lin_type, linewidth=modi_lin_seis_wid, dashes=modi_lin_dashes, label='Sample'),
    Line2D([0], [0], color=pre_lin_color, linestyle=pre_lin_type, linewidth=pre_lin_seis_wid, dashes=pre_lin_dashes, label='TriNet'),
]

corr_all = []

for i in range(len(non_rebui_vp_data)):
    corr_all.append(np.corrcoef(non_rebui_vp_data[i], pre_rebui_vp_data[i])[0][1])

corr = np.mean(corr_all)


ax3.legend(handles=handles, handlelength=handlelength, handletextpad=handletextpad, loc='lower left')
ax3.text(46, 28.5, 'CC:\n'+f"{corr:.3f}", fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))
# ax3.text(43, 30.15, 'CC: 0.970')

fig.text(0.02, 0.96, '(a)')
fig.tight_layout()
fig.savefig('stacou007.svg')

##########################################################
pre_vel_file_path = './pre_model_stacou015.dat'

input_seis_file_path = './rebuild_vp_seis_stacou015.dat'
pre_rebuild_seis_file_path = './rebuild_vp_seis_stacou015_re.dat'

pre_vel_dic = get_pre_vel_model(pre_vel_file_path)

inp_rebui_time, inp_rebui_vp_data, inp_rebui_sta_location, inp_rebui_use_index = get_rebuild_data(input_seis_file_path)
pre_rebui_time, pre_rebui_vp_data, pre_rebui_sta_location, pre_rebui_use_index = get_rebuild_data(pre_rebuild_seis_file_path)

draw_pre_vel_depth = []
draw_pre_vel_vp = []
for i in range(len(pre_vel_dic['depth'])):
    if pre_vel_dic['depth'][i]>draw_depth_para[0] and pre_vel_dic['depth'][i]<draw_depth_para[1]:
        draw_pre_vel_depth.append(pre_vel_dic['depth'][i])
        draw_pre_vel_vp.append(pre_vel_dic['vp'][i])

draw_inp_rebui = []
for i in range(len(inp_rebui_vp_data)):
    draw_inp_rebui.append([])
    for j in range(len(inp_rebui_vp_data[i])):
        draw_inp_rebui[-1].append(inp_rebui_vp_data[i][j]/2+locdata[i])

draw_pre_rebui = []
for i in range(len(pre_rebui_vp_data)):
    draw_pre_rebui.append([])
    for j in range(len(pre_rebui_vp_data[i])):
        draw_pre_rebui[-1].append(pre_rebui_vp_data[i][j]/2+locdata[i])


fig = plt.figure(figsize=figsize_para,dpi=900)
gs = fig.add_gridspec(1, 5)

ax1 = fig.add_subplot(gs[:,0:2])
ax2 = fig.add_subplot(gs[:,2])
ax3 = fig.add_subplot(gs[:,3:5])


for i in range(len(draw_inp_rebui)):
    if i in inp_rebui_use_index:
        ax1.plot(rebui_time[i], draw_inp_rebui[i], color=inp_lin_color, linestyle=inp_lin_type, dashes=inp_lin_dashes, linewidth=inp_lin_seis_wid)


ax1.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax1.set_ylim(9,31)
ax1.set_yticks([10, 20, 30])
ax1.set_ylabel('Distance (deg)')
ax1.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')
ax1.text(34, 29.5, 'Station Count: 15', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))


ax1.set_title('Input Seismic Waveform')



ax2.plot(draw_modi_vel_vp, draw_modi_vel_depth, color=modi_lin_color, linestyle=modi_lin_type, dashes=modi_lin_dashes, linewidth=modi_lin_model_wid, label='modi', zorder=2)
ax2.plot(draw_pre_vel_vp, draw_pre_vel_depth, color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_model_wid, label='pre', zorder=3)

idx_b=17
idx_e=31
idx_6601=22
idx_6602=23

ak_vp=ak135_vel_dic['vp'][idx_b:idx_e+1]
ak6601=ak135_vel_dic['depth'][idx_6601]
ak6602=ak135_vel_dic['depth'][idx_6602]
akthi=ak6602-ak6601
modi_vp=modi_vel_dic['vp'][idx_b:idx_e+1]
modi6601=modi_vel_dic['depth'][idx_6601]
modi6602=modi_vel_dic['depth'][idx_6602]
modithi=modi6602-modi6601
pre_vp=pre_vel_dic['vp'][idx_b:idx_e+1]
pre6601=pre_vel_dic['depth'][idx_6601]
pre6602=pre_vel_dic['depth'][idx_6602]
prethi=pre6602-pre6601

all_loss = []
for i in range(len(modi_vp)):
    all_loss.append(((pre_vp[i]-modi_vp[i])/ak_vp[i]/0.03)**2)

all_loss.append(((pre6601-modi6601)/30)**2)
all_loss.append(((prethi-modithi)/30)**2)

all_loss = np.sqrt(np.mean(all_loss))

ax2.text(10.1, 445, 'Loss:\n'+f"{all_loss:.3f}", fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))

ax2.invert_yaxis()
ax2.set_ylabel('Depth (km)')
ax2.set_xlabel('Vp (km/s)')
ax2.set_title('Velocity Model')


for i in range(len(draw_non_rebui)):
    ax3.plot(rebui_time[i], draw_non_rebui[i], color=modi_lin_color, linestyle=modi_lin_type, dashes=modi_lin_dashes, linewidth=modi_lin_seis_wid)

for i in range(len(draw_pre_rebui)):
    ax3.plot(rebui_time[i], draw_pre_rebui[i], color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_seis_wid)



ax3.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax3.set_ylim(9,31)
ax3.set_yticks([10, 20, 30])
ax3.set_ylabel('Distance (deg)')
ax3.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')

ax3.set_title('Seismic Waveform')


handles = [
    Line2D([0], [0], color=modi_lin_color, linestyle=modi_lin_type, linewidth=modi_lin_seis_wid, dashes=modi_lin_dashes, label='Sample'),
    Line2D([0], [0], color=pre_lin_color, linestyle=pre_lin_type, linewidth=pre_lin_seis_wid, dashes=pre_lin_dashes, label='TriNet'),
]

corr_all = []

for i in range(len(non_rebui_vp_data)):
    corr_all.append(np.corrcoef(non_rebui_vp_data[i], pre_rebui_vp_data[i])[0][1])

corr = np.mean(corr_all)


ax3.legend(handles=handles, handlelength=handlelength, handletextpad=handletextpad, loc='lower left')
ax3.text(46, 28.5, 'CC:\n'+f"{corr:.3f}", fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))
# ax3.text(43, 30.15, 'CC: 0.970')

fig.text(0.02, 0.96, '(b)')
fig.tight_layout()
fig.savefig('stacou015.svg')

##########################################################
pre_vel_file_path = './pre_model_stacou023.dat'

input_seis_file_path = './rebuild_vp_seis_stacou023.dat'
pre_rebuild_seis_file_path = './rebuild_vp_seis_stacou023_re.dat'

pre_vel_dic = get_pre_vel_model(pre_vel_file_path)

inp_rebui_time, inp_rebui_vp_data, inp_rebui_sta_location, inp_rebui_use_index = get_rebuild_data(input_seis_file_path)
pre_rebui_time, pre_rebui_vp_data, pre_rebui_sta_location, pre_rebui_use_index = get_rebuild_data(pre_rebuild_seis_file_path)

draw_pre_vel_depth = []
draw_pre_vel_vp = []
for i in range(len(pre_vel_dic['depth'])):
    if pre_vel_dic['depth'][i]>draw_depth_para[0] and pre_vel_dic['depth'][i]<draw_depth_para[1]:
        draw_pre_vel_depth.append(pre_vel_dic['depth'][i])
        draw_pre_vel_vp.append(pre_vel_dic['vp'][i])

draw_inp_rebui = []
for i in range(len(inp_rebui_vp_data)):
    draw_inp_rebui.append([])
    for j in range(len(inp_rebui_vp_data[i])):
        draw_inp_rebui[-1].append(inp_rebui_vp_data[i][j]/2+locdata[i])

draw_pre_rebui = []
for i in range(len(pre_rebui_vp_data)):
    draw_pre_rebui.append([])
    for j in range(len(pre_rebui_vp_data[i])):
        draw_pre_rebui[-1].append(pre_rebui_vp_data[i][j]/2+locdata[i])


fig = plt.figure(figsize=figsize_para,dpi=900)
gs = fig.add_gridspec(1, 5)

ax1 = fig.add_subplot(gs[:,0:2])
ax2 = fig.add_subplot(gs[:,2])
ax3 = fig.add_subplot(gs[:,3:5])


for i in range(len(draw_inp_rebui)):
    if i in inp_rebui_use_index:
        ax1.plot(rebui_time[i], draw_inp_rebui[i], color=inp_lin_color, linestyle=inp_lin_type, dashes=inp_lin_dashes, linewidth=inp_lin_seis_wid)


ax1.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax1.set_ylim(9,31)
ax1.set_yticks([10, 20, 30])
ax1.set_ylabel('Distance (deg)')
ax1.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')
ax1.text(34, 29.5, 'Station Count: 23', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))


ax1.set_title('Input Seismic Waveform')



ax2.plot(draw_modi_vel_vp, draw_modi_vel_depth, color=modi_lin_color, linestyle=modi_lin_type, dashes=modi_lin_dashes, linewidth=modi_lin_model_wid, label='modi', zorder=2)
ax2.plot(draw_pre_vel_vp, draw_pre_vel_depth, color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_model_wid, label='pre', zorder=3)

idx_b=17
idx_e=31
idx_6601=22
idx_6602=23

ak_vp=ak135_vel_dic['vp'][idx_b:idx_e+1]
ak6601=ak135_vel_dic['depth'][idx_6601]
ak6602=ak135_vel_dic['depth'][idx_6602]
akthi=ak6602-ak6601
modi_vp=modi_vel_dic['vp'][idx_b:idx_e+1]
modi6601=modi_vel_dic['depth'][idx_6601]
modi6602=modi_vel_dic['depth'][idx_6602]
modithi=modi6602-modi6601
pre_vp=pre_vel_dic['vp'][idx_b:idx_e+1]
pre6601=pre_vel_dic['depth'][idx_6601]
pre6602=pre_vel_dic['depth'][idx_6602]
prethi=pre6602-pre6601

all_loss = []
for i in range(len(modi_vp)):
    all_loss.append(((pre_vp[i]-modi_vp[i])/ak_vp[i]/0.03)**2)

all_loss.append(((pre6601-modi6601)/30)**2)
all_loss.append(((prethi-modithi)/30)**2)

all_loss = np.sqrt(np.mean(all_loss))

ax2.text(10.1, 445, 'Loss:\n'+f"{all_loss:.3f}", fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))

ax2.invert_yaxis()
ax2.set_ylabel('Depth (km)')
ax2.set_xlabel('Vp (km/s)')
ax2.set_title('Velocity Model')


for i in range(len(draw_non_rebui)):
    ax3.plot(rebui_time[i], draw_non_rebui[i], color=modi_lin_color, linestyle=modi_lin_type, dashes=modi_lin_dashes, linewidth=modi_lin_seis_wid)

for i in range(len(draw_pre_rebui)):
    ax3.plot(rebui_time[i], draw_pre_rebui[i], color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_seis_wid)



ax3.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax3.set_ylim(9,31)
ax3.set_yticks([10, 20, 30])
ax3.set_ylabel('Distance (deg)')
ax3.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')

ax3.set_title('Seismic Waveform')


handles = [
    Line2D([0], [0], color=modi_lin_color, linestyle=modi_lin_type, linewidth=modi_lin_seis_wid, dashes=modi_lin_dashes, label='Sample'),
    Line2D([0], [0], color=pre_lin_color, linestyle=pre_lin_type, linewidth=pre_lin_seis_wid, dashes=pre_lin_dashes, label='TriNet'),
]

corr_all = []

for i in range(len(non_rebui_vp_data)):
    corr_all.append(np.corrcoef(non_rebui_vp_data[i], pre_rebui_vp_data[i])[0][1])

corr = np.mean(corr_all)


ax3.legend(handles=handles, handlelength=handlelength, handletextpad=handletextpad, loc='lower left')
ax3.text(46, 28.5, 'CC:\n'+f"{corr:.3f}", fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))
# ax3.text(43, 30.15, 'CC: 0.970')

fig.text(0.02, 0.96, '(c)')
fig.tight_layout()
fig.savefig('stacou023.svg')

##########################################################
pre_vel_file_path = './pre_model_stacou031.dat'

input_seis_file_path = './rebuild_vp_seis_stacou031.dat'
pre_rebuild_seis_file_path = './rebuild_vp_seis_stacou031_re.dat'

pre_vel_dic = get_pre_vel_model(pre_vel_file_path)

inp_rebui_time, inp_rebui_vp_data, inp_rebui_sta_location, inp_rebui_use_index = get_rebuild_data(input_seis_file_path)
pre_rebui_time, pre_rebui_vp_data, pre_rebui_sta_location, pre_rebui_use_index = get_rebuild_data(pre_rebuild_seis_file_path)

draw_pre_vel_depth = []
draw_pre_vel_vp = []
for i in range(len(pre_vel_dic['depth'])):
    if pre_vel_dic['depth'][i]>draw_depth_para[0] and pre_vel_dic['depth'][i]<draw_depth_para[1]:
        draw_pre_vel_depth.append(pre_vel_dic['depth'][i])
        draw_pre_vel_vp.append(pre_vel_dic['vp'][i])

draw_inp_rebui = []
for i in range(len(inp_rebui_vp_data)):
    draw_inp_rebui.append([])
    for j in range(len(inp_rebui_vp_data[i])):
        draw_inp_rebui[-1].append(inp_rebui_vp_data[i][j]/2+locdata[i])

draw_pre_rebui = []
for i in range(len(pre_rebui_vp_data)):
    draw_pre_rebui.append([])
    for j in range(len(pre_rebui_vp_data[i])):
        draw_pre_rebui[-1].append(pre_rebui_vp_data[i][j]/2+locdata[i])


fig = plt.figure(figsize=figsize_para,dpi=900)
gs = fig.add_gridspec(1, 5)

ax1 = fig.add_subplot(gs[:,0:2])
ax2 = fig.add_subplot(gs[:,2])
ax3 = fig.add_subplot(gs[:,3:5])


for i in range(len(draw_inp_rebui)):
    if i in inp_rebui_use_index:
        ax1.plot(rebui_time[i], draw_inp_rebui[i], color=inp_lin_color, linestyle=inp_lin_type, dashes=inp_lin_dashes, linewidth=inp_lin_seis_wid)


ax1.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax1.set_ylim(9,31)
ax1.set_yticks([10, 20, 30])
ax1.set_ylabel('Distance (deg)')
ax1.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')
ax1.text(34, 29.5, 'Station Count: 31', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))


ax1.set_title('Input Seismic Waveform')



ax2.plot(draw_modi_vel_vp, draw_modi_vel_depth, color=modi_lin_color, linestyle=modi_lin_type, dashes=modi_lin_dashes, linewidth=modi_lin_model_wid, label='modi', zorder=2)
ax2.plot(draw_pre_vel_vp, draw_pre_vel_depth, color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_model_wid, label='pre', zorder=3)

idx_b=17
idx_e=31
idx_6601=22
idx_6602=23

ak_vp=ak135_vel_dic['vp'][idx_b:idx_e+1]
ak6601=ak135_vel_dic['depth'][idx_6601]
ak6602=ak135_vel_dic['depth'][idx_6602]
akthi=ak6602-ak6601
modi_vp=modi_vel_dic['vp'][idx_b:idx_e+1]
modi6601=modi_vel_dic['depth'][idx_6601]
modi6602=modi_vel_dic['depth'][idx_6602]
modithi=modi6602-modi6601
pre_vp=pre_vel_dic['vp'][idx_b:idx_e+1]
pre6601=pre_vel_dic['depth'][idx_6601]
pre6602=pre_vel_dic['depth'][idx_6602]
prethi=pre6602-pre6601

all_loss = []
for i in range(len(modi_vp)):
    all_loss.append(((pre_vp[i]-modi_vp[i])/ak_vp[i]/0.03)**2)

all_loss.append(((pre6601-modi6601)/30)**2)
all_loss.append(((prethi-modithi)/30)**2)

all_loss = np.sqrt(np.mean(all_loss))

ax2.text(10.1, 445, 'Loss:\n'+f"{all_loss:.3f}", fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))

ax2.invert_yaxis()
ax2.set_ylabel('Depth (km)')
ax2.set_xlabel('Vp (km/s)')
ax2.set_title('Velocity Model')


for i in range(len(draw_non_rebui)):
    ax3.plot(rebui_time[i], draw_non_rebui[i], color=modi_lin_color, linestyle=modi_lin_type, dashes=modi_lin_dashes, linewidth=modi_lin_seis_wid)

for i in range(len(draw_pre_rebui)):
    ax3.plot(rebui_time[i], draw_pre_rebui[i], color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_seis_wid)



ax3.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax3.set_ylim(9,31)
ax3.set_yticks([10, 20, 30])
ax3.set_ylabel('Distance (deg)')
ax3.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')

ax3.set_title('Seismic Waveform')


handles = [
    Line2D([0], [0], color=modi_lin_color, linestyle=modi_lin_type, linewidth=modi_lin_seis_wid, dashes=modi_lin_dashes, label='Sample'),
    Line2D([0], [0], color=pre_lin_color, linestyle=pre_lin_type, linewidth=pre_lin_seis_wid, dashes=pre_lin_dashes, label='TriNet'),
]

corr_all = []

for i in range(len(non_rebui_vp_data)):
    corr_all.append(np.corrcoef(non_rebui_vp_data[i], pre_rebui_vp_data[i])[0][1])

corr = np.mean(corr_all)


ax3.legend(handles=handles, handlelength=handlelength, handletextpad=handletextpad, loc='lower left')
ax3.text(46, 28.5, 'CC:\n'+f"{corr:.3f}", fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))
# ax3.text(43, 30.15, 'CC: 0.970')

fig.text(0.02, 0.96, '(d)')
fig.tight_layout()
fig.savefig('stacou031.svg')

##########################################################
pre_vel_file_path = './pre_model_stacou039.dat'

input_seis_file_path = './rebuild_vp_seis_stacou039.dat'
pre_rebuild_seis_file_path = './rebuild_vp_seis_stacou039_re.dat'

pre_vel_dic = get_pre_vel_model(pre_vel_file_path)

inp_rebui_time, inp_rebui_vp_data, inp_rebui_sta_location, inp_rebui_use_index = get_rebuild_data(input_seis_file_path)
pre_rebui_time, pre_rebui_vp_data, pre_rebui_sta_location, pre_rebui_use_index = get_rebuild_data(pre_rebuild_seis_file_path)

draw_pre_vel_depth = []
draw_pre_vel_vp = []
for i in range(len(pre_vel_dic['depth'])):
    if pre_vel_dic['depth'][i]>draw_depth_para[0] and pre_vel_dic['depth'][i]<draw_depth_para[1]:
        draw_pre_vel_depth.append(pre_vel_dic['depth'][i])
        draw_pre_vel_vp.append(pre_vel_dic['vp'][i])

draw_inp_rebui = []
for i in range(len(inp_rebui_vp_data)):
    draw_inp_rebui.append([])
    for j in range(len(inp_rebui_vp_data[i])):
        draw_inp_rebui[-1].append(inp_rebui_vp_data[i][j]/2+locdata[i])

draw_pre_rebui = []
for i in range(len(pre_rebui_vp_data)):
    draw_pre_rebui.append([])
    for j in range(len(pre_rebui_vp_data[i])):
        draw_pre_rebui[-1].append(pre_rebui_vp_data[i][j]/2+locdata[i])


fig = plt.figure(figsize=figsize_para,dpi=900)
gs = fig.add_gridspec(1, 5)

ax1 = fig.add_subplot(gs[:,0:2])
ax2 = fig.add_subplot(gs[:,2])
ax3 = fig.add_subplot(gs[:,3:5])


for i in range(len(draw_inp_rebui)):
    if i in inp_rebui_use_index:
        ax1.plot(rebui_time[i], draw_inp_rebui[i], color=inp_lin_color, linestyle=inp_lin_type, dashes=inp_lin_dashes, linewidth=inp_lin_seis_wid)


ax1.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax1.set_ylim(9,31)
ax1.set_yticks([10, 20, 30])
ax1.set_ylabel('Distance (deg)')
ax1.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')
ax1.text(34, 29.5, 'Station Count: 39', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))


ax1.set_title('Input Seismic Waveform')



ax2.plot(draw_modi_vel_vp, draw_modi_vel_depth, color=modi_lin_color, linestyle=modi_lin_type, dashes=modi_lin_dashes, linewidth=modi_lin_model_wid, label='modi', zorder=2)
ax2.plot(draw_pre_vel_vp, draw_pre_vel_depth, color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_model_wid, label='pre', zorder=3)

idx_b=17
idx_e=31
idx_6601=22
idx_6602=23

ak_vp=ak135_vel_dic['vp'][idx_b:idx_e+1]
ak6601=ak135_vel_dic['depth'][idx_6601]
ak6602=ak135_vel_dic['depth'][idx_6602]
akthi=ak6602-ak6601
modi_vp=modi_vel_dic['vp'][idx_b:idx_e+1]
modi6601=modi_vel_dic['depth'][idx_6601]
modi6602=modi_vel_dic['depth'][idx_6602]
modithi=modi6602-modi6601
pre_vp=pre_vel_dic['vp'][idx_b:idx_e+1]
pre6601=pre_vel_dic['depth'][idx_6601]
pre6602=pre_vel_dic['depth'][idx_6602]
prethi=pre6602-pre6601

all_loss = []
for i in range(len(modi_vp)):
    all_loss.append(((pre_vp[i]-modi_vp[i])/ak_vp[i]/0.03)**2)

all_loss.append(((pre6601-modi6601)/30)**2)
all_loss.append(((prethi-modithi)/30)**2)

all_loss = np.sqrt(np.mean(all_loss))

ax2.text(10.1, 445, 'Loss:\n'+f"{all_loss:.3f}", fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))

ax2.invert_yaxis()
ax2.set_ylabel('Depth (km)')
ax2.set_xlabel('Vp (km/s)')
ax2.set_title('Velocity Model')


for i in range(len(draw_non_rebui)):
    ax3.plot(rebui_time[i], draw_non_rebui[i], color=modi_lin_color, linestyle=modi_lin_type, dashes=modi_lin_dashes, linewidth=modi_lin_seis_wid)

for i in range(len(draw_pre_rebui)):
    ax3.plot(rebui_time[i], draw_pre_rebui[i], color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_seis_wid)



ax3.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax3.set_ylim(9,31)
ax3.set_yticks([10, 20, 30])
ax3.set_ylabel('Distance (deg)')
ax3.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')

ax3.set_title('Seismic Waveform')


handles = [
    Line2D([0], [0], color=modi_lin_color, linestyle=modi_lin_type, linewidth=modi_lin_seis_wid, dashes=modi_lin_dashes, label='Sample'),
    Line2D([0], [0], color=pre_lin_color, linestyle=pre_lin_type, linewidth=pre_lin_seis_wid, dashes=pre_lin_dashes, label='TriNet'),
]

corr_all = []

for i in range(len(non_rebui_vp_data)):
    corr_all.append(np.corrcoef(non_rebui_vp_data[i], pre_rebui_vp_data[i])[0][1])

corr = np.mean(corr_all)


ax3.legend(handles=handles, handlelength=handlelength, handletextpad=handletextpad, loc='lower left')
ax3.text(46, 28.5, 'CC:\n'+f"{corr:.3f}", fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))
# ax3.text(43, 30.15, 'CC: 0.970')

fig.text(0.02, 0.96, '(e)')
fig.tight_layout()
fig.savefig('stacou039.svg')