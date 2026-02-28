

import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.lines import Line2D

from scipy.interpolate import interp1d

from pic7_utils import get_rebuild_data_real, get_rebuild_data_rebuild, vel_base, add_aligned_text


f = open('./corr.dat','r')
f_c = f.readlines()
f.close()

model_li_corr = f_c[0].split(':')[1].replace('\n','')
ak135_corr = f_c[1].split(':')[1].replace('\n','')

draw_depth_para = [400, 1000]

####################################################################


model_li_pre_rerun_rebuild_file_path = '../d/rerundata/li/rebuild_vp_seis_real_pre.dat'
model_li_rebuild_file_path = '../d/oridata/li/rebuild_vp_seis_model_li_20080519.dat'

ak135_pre_rerun_rebuild_file_path = '../d/rerundata/ak/rebuild_vp_seis_real_pre.dat'
ak135_rebuild_file_path = '../d/oridata/ak/rebuild_vp_seis_ak135_20080519.dat'


model_li_pre_rerun_model_path = '../d/rerundata/li/modify_model_real_pre.dat'
model_li_pre_rerun_model_up_path = '../d/rerundata/li/all_up_use.dat'
model_li_pre_rerun_model_low_path = '../d/rerundata/li/all_low_use.dat'
model_li_model_path = '../d/oridata/li/modify_model_model_li_20080519.dat'

ak135_pre_rerun_model_path = '../d/rerundata/ak/modify_model_real_pre.dat'
ak135_pre_rerun_model_up_path = '../d/rerundata/ak/all_up_use.dat'
ak135_pre_rerun_model_low_path = '../d/rerundata/ak/all_low_use.dat'
ak135_model_path = '../d/oridata/ak/modify_model_ak135_20080519.dat'


####################################################################


model_li_pre_rerun_pro_time, model_li_pre_rerun_pro_vp_data, model_li_pre_rerun_sta_location, model_li_pre_rerun_use_index = get_rebuild_data_rebuild(model_li_pre_rerun_rebuild_file_path)
model_li_pro_time, model_li_pro_vp_data, model_li_sta_location, model_li_use_index = get_rebuild_data_rebuild(model_li_rebuild_file_path)

ak135_pre_rerun_pro_time, ak135_pre_rerun_pro_vp_data, ak135_pre_rerun_sta_location, ak135_pre_rerun_use_index = get_rebuild_data_rebuild(ak135_pre_rerun_rebuild_file_path)
ak135_pro_time, ak135_pro_vp_data, ak135_sta_location, ak135_use_index = get_rebuild_data_rebuild(ak135_rebuild_file_path)

model_li_pre_rerun_model = vel_base(model_li_pre_rerun_model_path)
model_li_pre_rerun_model_up = vel_base(model_li_pre_rerun_model_up_path)
model_li_pre_rerun_model_low = vel_base(model_li_pre_rerun_model_low_path)
model_li_model = vel_base(model_li_model_path)

ak135_pre_rerun_model = vel_base(ak135_pre_rerun_model_path)
ak135_pre_rerun_model_up = vel_base(ak135_pre_rerun_model_up_path)
ak135_pre_rerun_model_low = vel_base(ak135_pre_rerun_model_low_path)
ak135_model = vel_base(ak135_model_path)


####################################################################


draw_model_li_pre_rerun_pro_vp_data = []
for i in range(len(model_li_pre_rerun_pro_vp_data)):
    draw_model_li_pre_rerun_pro_vp_data.append([])
    for j in range(len(model_li_pre_rerun_pro_vp_data[i])):
        draw_model_li_pre_rerun_pro_vp_data[-1].append(model_li_pre_rerun_pro_vp_data[i][j]/3+model_li_pre_rerun_sta_location[i])

draw_model_li_pro_vp_data = []
for i in range(len(model_li_pro_vp_data)):
    draw_model_li_pro_vp_data.append([])
    for j in range(len(model_li_pro_vp_data[i])):
        draw_model_li_pro_vp_data[-1].append(model_li_pro_vp_data[i][j]/3+model_li_sta_location[i])

draw_ak135_pre_rerun_pro_vp_data = []
for i in range(len(ak135_pre_rerun_pro_vp_data)):
    draw_ak135_pre_rerun_pro_vp_data.append([])
    for j in range(len(ak135_pre_rerun_pro_vp_data[i])):
        draw_ak135_pre_rerun_pro_vp_data[-1].append(ak135_pre_rerun_pro_vp_data[i][j]/3+ak135_pre_rerun_sta_location[i])

draw_ak135_pro_vp_data = []
for i in range(len(ak135_pro_vp_data)):
    draw_ak135_pro_vp_data.append([])
    for j in range(len(ak135_pro_vp_data[i])):
        draw_ak135_pro_vp_data[-1].append(ak135_pro_vp_data[i][j]/3+ak135_sta_location[i])


draw_ak135_depth = []
draw_ak135_vp = []
for i in range(len(ak135_model['depth'])):
    if ak135_model['depth'][i]>draw_depth_para[0] and ak135_model['depth'][i]<draw_depth_para[1]:
        draw_ak135_depth.append(ak135_model['depth'][i])
        draw_ak135_vp.append(ak135_model['vp'][i])

draw_ak135_pre_rerun_depth = []
draw_ak135_pre_rerun_vp = []
for i in range(len(ak135_pre_rerun_model['depth'])):
    if ak135_pre_rerun_model['depth'][i]>draw_depth_para[0] and ak135_pre_rerun_model['depth'][i]<draw_depth_para[1]:
        draw_ak135_pre_rerun_depth.append(ak135_pre_rerun_model['depth'][i])
        draw_ak135_pre_rerun_vp.append(ak135_pre_rerun_model['vp'][i])

draw_ak135_pre_rerun_depth_up = []
draw_ak135_pre_rerun_vp_up = []
for i in range(len(ak135_pre_rerun_model_up['depth'])):
    if ak135_pre_rerun_model_up['depth'][i]>draw_depth_para[0] and ak135_pre_rerun_model_up['depth'][i]<draw_depth_para[1]:
        draw_ak135_pre_rerun_depth_up.append(ak135_pre_rerun_model_up['depth'][i])
        draw_ak135_pre_rerun_vp_up.append(ak135_pre_rerun_model_up['vp'][i])

draw_ak135_pre_rerun_depth_low = []
draw_ak135_pre_rerun_vp_low = []
for i in range(len(ak135_pre_rerun_model_low['depth'])):
    if ak135_pre_rerun_model_low['depth'][i]>draw_depth_para[0] and ak135_pre_rerun_model_low['depth'][i]<draw_depth_para[1]:
        draw_ak135_pre_rerun_depth_low.append(ak135_pre_rerun_model_low['depth'][i])
        draw_ak135_pre_rerun_vp_low.append(ak135_pre_rerun_model_low['vp'][i])

draw_model_li_depth = []
draw_model_li_vp = []
for i in range(len(model_li_model['depth'])):
    if model_li_model['depth'][i]>draw_depth_para[0] and model_li_model['depth'][i]<draw_depth_para[1]:
        draw_model_li_depth.append(model_li_model['depth'][i])
        draw_model_li_vp.append(model_li_model['vp'][i])

draw_model_li_pre_rerun_depth = []
draw_model_li_pre_rerun_vp = []
for i in range(len(model_li_pre_rerun_model['depth'])):
    if model_li_pre_rerun_model['depth'][i]>draw_depth_para[0] and model_li_pre_rerun_model['depth'][i]<draw_depth_para[1]:
        draw_model_li_pre_rerun_depth.append(model_li_pre_rerun_model['depth'][i])
        draw_model_li_pre_rerun_vp.append(model_li_pre_rerun_model['vp'][i])

draw_model_li_pre_rerun_depth_up = []
draw_model_li_pre_rerun_vp_up = []
for i in range(len(model_li_pre_rerun_model_up['depth'])):
    if model_li_pre_rerun_model_up['depth'][i]>draw_depth_para[0] and model_li_pre_rerun_model_up['depth'][i]<draw_depth_para[1]:
        draw_model_li_pre_rerun_depth_up.append(model_li_pre_rerun_model_up['depth'][i])
        draw_model_li_pre_rerun_vp_up.append(model_li_pre_rerun_model_up['vp'][i])

draw_model_li_pre_rerun_depth_low = []
draw_model_li_pre_rerun_vp_low = []
for i in range(len(model_li_pre_rerun_model_low['depth'])):
    if model_li_pre_rerun_model_low['depth'][i]>draw_depth_para[0] and model_li_pre_rerun_model_low['depth'][i]<draw_depth_para[1]:
        draw_model_li_pre_rerun_depth_low.append(model_li_pre_rerun_model_low['depth'][i])
        draw_model_li_pre_rerun_vp_low.append(model_li_pre_rerun_model_low['vp'][i])


idx_b=17
idx_e=31
idx_6601=22
idx_6602=23

ak_vp=ak135_model['vp'][idx_b:idx_e+1]
ak6601=ak135_model['depth'][idx_6601]
ak6602=ak135_model['depth'][idx_6602]
akthi=ak6602-ak6601
akpre_vp=ak135_pre_rerun_model['vp'][idx_b:idx_e+1]
akpre6601=ak135_pre_rerun_model['depth'][idx_6601]
akpre6602=ak135_pre_rerun_model['depth'][idx_6602]
akprethi=akpre6602-akpre6601
modelli_vp=model_li_model['vp'][idx_b:idx_e+1]
modelli6601=model_li_model['depth'][idx_6601]
modelli6602=model_li_model['depth'][idx_6602]
modellithi=modelli6602-modelli6601
modellipre_vp=model_li_pre_rerun_model['vp'][idx_b:idx_e+1]
modellipre6601=model_li_pre_rerun_model['depth'][idx_6601]
modellipre6602=model_li_pre_rerun_model['depth'][idx_6602]
modelliprethi=modellipre6602-modellipre6601

all_loss_ak = []
for i in range(len(ak_vp)):
    all_loss_ak.append(((akpre_vp[i]-ak_vp[i])/ak_vp[i]/0.03)**2)

all_loss_ak.append(((akpre6601-ak6601)/30)**2)
all_loss_ak.append(((akprethi-akthi)/30)**2)

all_loss_ak = np.sqrt(np.mean(all_loss_ak))

all_loss_li = []
for i in range(len(modelli_vp)):
    all_loss_li.append(((modellipre_vp[i]-modelli_vp[i])/ak_vp[i]/0.03)**2)

all_loss_li.append(((modellipre6601-modelli6601)/30)**2)
all_loss_li.append(((modelliprethi-modellithi)/30)**2)

all_loss_li = np.sqrt(np.mean(all_loss_li))

####################################################################

font_path = '../../fonts/timesnewroman/times.ttf'
fm.fontManager.addfont(font_path)


plt.rcParams['font.family'] = 'Times New Roman'


plt.rcParams['font.size'] = 8 
plt.rcParams['axes.titlesize'] = 8
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8

plt.rcParams['svg.fonttype'] = 'none'

reduction_v_para = 10
cut_time_start_time_para = 20
cut_time_windows_para = 35

figsize_para = (8, 5)


# li_lin_type = '--'
li_lin_type = '-'
# li_lin_color = (4/255, 41/255, 250/255)
li_lin_color = (66/255, 133/255, 244/255)
li_lin_model_wid = 1.3
li_lin_seis_wid = 1
# li_lin_dashes = [5,3]
li_lin_dashes = []
# li_pre_rerun_lin_type = '--'
li_pre_rerun_lin_type = '-'
# li_pre_rerun_lin_color = (4/255, 41/255, 250/255)
li_pre_rerun_lin_color = (219/255, 68/255, 55/255)
li_pre_rerun_lin_color_up_low = (244/255, 180/255, 0/255)
li_pre_rerun_lin_model_wid = 1.3
li_pre_rerun_lin_seis_wid = 1
# li_pre_rerun_lin_dashes = [5,3]
li_pre_rerun_lin_dashes = []


handlelength=3
handletextpad=0.6


####################################################################


# fig = plt.figure(figsize=figsize_para)
fig = plt.figure(figsize=figsize_para,dpi=900)
gs = fig.add_gridspec(1, 5)

####################################################################

ax1 = fig.add_subplot(gs[:,0])

ax1.plot(draw_model_li_pre_rerun_vp_up, draw_model_li_pre_rerun_depth_up, color=li_pre_rerun_lin_color_up_low, linestyle=li_pre_rerun_lin_type, dashes=li_pre_rerun_lin_dashes, linewidth=li_pre_rerun_lin_model_wid, label='Li_2013_Pre', zorder=1)
ax1.plot(draw_model_li_pre_rerun_vp_low, draw_model_li_pre_rerun_depth_low, color=li_pre_rerun_lin_color_up_low, linestyle=li_pre_rerun_lin_type, dashes=li_pre_rerun_lin_dashes, linewidth=li_pre_rerun_lin_model_wid, label='Li_2013_Pre', zorder=1)
ax1.fill_betweenx(draw_model_li_pre_rerun_depth_up, draw_model_li_pre_rerun_vp_up, draw_model_li_pre_rerun_vp_low, color=li_pre_rerun_lin_color_up_low, alpha=0.3, zorder=1)
ax1.plot(draw_model_li_vp, draw_model_li_depth, color=li_lin_color, linestyle=li_lin_type, dashes=li_lin_dashes, linewidth=li_lin_model_wid, label='Li_2013', zorder=2)
ax1.plot(draw_model_li_pre_rerun_vp, draw_model_li_pre_rerun_depth, color=li_pre_rerun_lin_color, linestyle=li_pre_rerun_lin_type, dashes=li_pre_rerun_lin_dashes, linewidth=li_pre_rerun_lin_model_wid, label='Li_2013_Pre', zorder=3)

# ax1.legend(loc='lower left')

handles = [
    Line2D([0], [0], color=li_lin_color, linestyle=li_lin_type, linewidth=li_lin_model_wid, dashes=li_lin_dashes, label='Li_2013'),
    Line2D([0], [0], color=li_pre_rerun_lin_color, linestyle=li_pre_rerun_lin_type, linewidth=li_pre_rerun_lin_model_wid, dashes=li_pre_rerun_lin_dashes, label='Li_2013_Pre'),
    Line2D([0], [0], color=li_pre_rerun_lin_color_up_low, linestyle=li_pre_rerun_lin_type, linewidth=li_pre_rerun_lin_model_wid, dashes=li_pre_rerun_lin_dashes, label='Pre_Range'),
]

# ax3.legend(handles=handles, handlelength=3, handletextpad=1.0, loc='upper right', bbox_to_anchor=[ax3_pos.x0+ax3_pos.width+0.005, ax3_pos.y0+ax3_pos.height+0.005], bbox_transform=fig.transFigure)
# ax1.legend(handles=handles, handlelength=handlelength, handletextpad=handletextpad, loc='lower left')

ax1.set_xlim(8.8,11.8)
ax1.set_ylim(380, 990)

ax1.set_xticks([9,10,11])
ax1.set_yticks([400,500,600,700,800,900])

ax1.text(9.8, 405, 'Loss: '+f"{all_loss_li:.3f}",fontsize=10)
# ax1.set_xticks()
ax1.invert_yaxis()
ax1.set_ylabel('Depth (km)',fontsize=10)
ax1.set_xlabel('Vp (km/s)',fontsize=10)
ax1.set_title('Velocity Model',fontsize=10)

####################################################################

linewidth = None


ax2 = fig.add_subplot(gs[:,1:3])

for i in range(len(model_li_pro_time)):
    if i == 0:
        ax2.plot(model_li_pro_time[i], draw_model_li_pro_vp_data[i], color=li_lin_color, label='Li_2013', linestyle=li_lin_type, dashes=li_lin_dashes, linewidth=li_lin_seis_wid)
    else:
        ax2.plot(model_li_pro_time[i], draw_model_li_pro_vp_data[i], color=li_lin_color, dashes=li_lin_dashes, linestyle=li_lin_type, linewidth=li_lin_seis_wid)

for i in range(len(model_li_pre_rerun_pro_time)):
    if i == 0:
        ax2.plot(model_li_pre_rerun_pro_time[i], draw_model_li_pre_rerun_pro_vp_data[i], color=li_pre_rerun_lin_color, label='Li_2013_Pre', linestyle=li_pre_rerun_lin_type, dashes=li_pre_rerun_lin_dashes, linewidth=li_pre_rerun_lin_seis_wid)
    else:
        ax2.plot(model_li_pre_rerun_pro_time[i], draw_model_li_pre_rerun_pro_vp_data[i], color=li_pre_rerun_lin_color, dashes=li_pre_rerun_lin_dashes, linestyle=li_pre_rerun_lin_type, linewidth=li_pre_rerun_lin_seis_wid)



ax2.set_xlim(25,50)
ax2.set_ylim(9,31)
# ax2.set_ylabel('Distance (deg)')
# ax2.set_ylabel('')
ax2.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)',fontsize=10)

ax2.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['','','','','','','','','','',''])
# ax2.set_yticks([])
ax2.yaxis.tick_right ()
ax2.yaxis.set_label_position('right')
ax2.set_title('Seismic Waveform',fontsize=10)

# ax2.legend(loc='lower left')

handles = [
    Line2D([0], [0], color=li_lin_color, linestyle=li_lin_type, linewidth=li_lin_seis_wid, dashes=li_lin_dashes, label='Li2013'),
    Line2D([0], [0], color=li_pre_rerun_lin_color, linestyle=li_pre_rerun_lin_type, linewidth=li_pre_rerun_lin_seis_wid, dashes=li_pre_rerun_lin_dashes, label='TriNet_Li2013'),
    Line2D([0], [0], color=li_pre_rerun_lin_color_up_low, linestyle=li_pre_rerun_lin_type, linewidth=li_pre_rerun_lin_seis_wid, dashes=li_pre_rerun_lin_dashes, label='Pre_Range'),
]

ax2.text(26,29.8,'D',fontsize=10)
ax2.text(46,11,'C',fontsize=10)
ax2.text(41.2,24,'B',fontsize=10)
ax2.text(40,10,'A',fontsize=10)

# ax3.legend(handles=handles, handlelength=3, handletextpad=1.0, loc='upper right', bbox_to_anchor=[ax3_pos.x0+ax3_pos.width+0.005, ax3_pos.y0+ax3_pos.height+0.005], bbox_transform=fig.transFigure)
ax2.legend(handles=handles, handlelength=handlelength, handletextpad=handletextpad, loc='lower left')
ax2.text(43, 30, 'CC: '+model_li_corr,fontsize=10)

####################################################################

ax3 = fig.add_subplot(gs[:,3:5])

ax3.set_xlim(cut_time_start_time_para+4, cut_time_start_time_para+cut_time_windows_para-6)
ax3.set_ylim(9,31)
ax3.set_ylabel('Distance (deg)',fontsize=10)
ax3.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)',fontsize=10)

ax3.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['10','','','','','20','','','','','30'])
ax3.yaxis.tick_right ()
ax3.yaxis.set_label_position('right')
ax3.set_title('Seismic Waveform',fontsize=10)

# ax3.legend(loc='lower left')

ax3.text(42, 30, 'CC: '+model_li_corr,fontsize=10)

####################################################################

fig.tight_layout()

ax1_pos = ax1.get_position()
ax2_pos = ax2.get_position()
ax3_pos = ax3.get_position()
subploticonfontsize = 10

add_aligned_text(fig, ax1_pos, '(a)', subploticonfontsize, -0.02, 0.03)
add_aligned_text(fig, ax2_pos, '(b)', subploticonfontsize, -0.02, 0.03)
add_aligned_text(fig, ax3_pos, '(c)', subploticonfontsize, -0.02, 0.03)

fig.savefig('li_v2.0.svg')
# fig.savefig('pic8_li_v2.0.jpg')
plt.close(fig=fig)