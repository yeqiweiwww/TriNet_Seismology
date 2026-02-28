

import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.lines import Line2D
import matplotlib.patches as patches

from scipy.interpolate import interp1d

from pic7_utils import get_rebuild_data_real, get_rebuild_data_rebuild, vel_base, add_aligned_text


f = open('./corr.dat','r')
f_c = f.readlines()
f.close()

model_li_corr = f_c[0].split(':')[1].replace('\n','')
pre_rerun_corr = f_c[1].split(':')[1].replace('\n','')

draw_depth_para = [400, 1000]

####################################################################


real_pre_rebuild_file_path = '../d/rerundata/20080519/rebuild_vp_seis_real_pre.dat'
model_li_rebuild_file_path = '../../pic7/d/oridata/li/rebuild_vp_seis_model_li_20080519.dat'
real_rebuild_file_path = '../d/oridata/20080519/rebuild_data_real_v2.0_refine_use.dat'

ak135_model_path = '../../pic7/d/oridata/ak/modify_model_ak135_20080519.dat'
model_li_model_path = '../../pic7/d/oridata/li/modify_model_model_li_20080519.dat'
model_pre_model_path = '../d/rerundata/20080519/modify_model_real_pre.dat'
model_pre_model_up_path = '../d/rerundata/20080519/all_up_use.dat'
model_pre_model_low_path = '../d/rerundata/20080519/all_low_use.dat'


####################################################################


real_pre_pro_time, real_pre_pro_vp_data, real_pre_sta_location, real_pre_use_index = get_rebuild_data_rebuild(real_pre_rebuild_file_path)
model_li_pro_time, model_li_pro_vp_data, model_li_sta_location, model_li_use_index = get_rebuild_data_rebuild(model_li_rebuild_file_path)
real_pro_time, real_pro_vp_data, real_sta_location, real_use_index = get_rebuild_data_real(real_rebuild_file_path)

ak135_model = vel_base(ak135_model_path)
model_li_model = vel_base(model_li_model_path)
model_pre_model = vel_base(model_pre_model_path)
model_pre_model_up = vel_base(model_pre_model_up_path)
model_pre_model_low = vel_base(model_pre_model_low_path)

####################################################################


draw_real_pre_pro_vp_data = []
for i in range(len(real_pre_pro_vp_data)):
    draw_real_pre_pro_vp_data.append([])
    for j in range(len(real_pre_pro_vp_data[i])):
        draw_real_pre_pro_vp_data[-1].append(real_pre_pro_vp_data[i][j]/3+real_pre_sta_location[i])

draw_model_li_pro_vp_data = []
for i in range(len(model_li_pro_vp_data)):
    draw_model_li_pro_vp_data.append([])
    for j in range(len(model_li_pro_vp_data[i])):
        draw_model_li_pro_vp_data[-1].append(model_li_pro_vp_data[i][j]/3+real_pre_sta_location[i])

draw_real_pro_vp_data = []
for i in range(len(real_pro_vp_data)):
    draw_real_pro_vp_data.append([])
    for j in range(len(real_pro_vp_data[i])):
        draw_real_pro_vp_data[-1].append(real_pro_vp_data[i][j]/3+real_pre_sta_location[i])


draw_ak135_depth = []
draw_ak135_vp = []
for i in range(len(ak135_model['depth'])):
    if ak135_model['depth'][i]>draw_depth_para[0] and ak135_model['depth'][i]<draw_depth_para[1]:
        draw_ak135_depth.append(ak135_model['depth'][i])
        draw_ak135_vp.append(ak135_model['vp'][i])

draw_model_li_depth = []
draw_model_li_vp = []
for i in range(len(model_li_model['depth'])):
    if model_li_model['depth'][i]>draw_depth_para[0] and model_li_model['depth'][i]<draw_depth_para[1]:
        draw_model_li_depth.append(model_li_model['depth'][i])
        draw_model_li_vp.append(model_li_model['vp'][i])

draw_model_pre_depth = []
draw_model_pre_vp = []
for i in range(len(model_pre_model['depth'])):
    if model_pre_model['depth'][i]>draw_depth_para[0] and model_pre_model['depth'][i]<draw_depth_para[1]:
        draw_model_pre_depth.append(model_pre_model['depth'][i])
        draw_model_pre_vp.append(model_pre_model['vp'][i])

draw_model_pre_depth_up = []
draw_model_pre_vp_up = []
for i in range(len(model_pre_model_up['depth'])):
    if model_pre_model_up['depth'][i]>draw_depth_para[0] and model_pre_model_up['depth'][i]<draw_depth_para[1]:
        draw_model_pre_depth_up.append(model_pre_model_up['depth'][i])
        draw_model_pre_vp_up.append(model_pre_model_up['vp'][i])

draw_model_pre_depth_low = []
draw_model_pre_vp_low = []
for i in range(len(model_pre_model_low['depth'])):
    if model_pre_model_low['depth'][i]>draw_depth_para[0] and model_pre_model_low['depth'][i]<draw_depth_para[1]:
        draw_model_pre_depth_low.append(model_pre_model_low['depth'][i])
        draw_model_pre_vp_low.append(model_pre_model_low['vp'][i])


####################################################################



font_path = '../../fonts/timesnewroman/times.ttf'
fm.fontManager.addfont(font_path)


plt.rcParams['font.family'] = 'Times New Roman'


# plt.rcParams['font.size'] = 12
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

ak_lin_type = '-'
ak_lin_color = 'gray'
ak_lin_wid = 1.3
ak_lin_dashes = []
# li_lin_type = '--'
li_lin_type = '-'
# li_lin_color = (4/255, 41/255, 250/255)
# li_lin_color = (112/255, 151/255, 248/255)
li_lin_color = (66/255, 133/255, 244/255)
li_lin_model_wid = 1.3
li_lin_seis_wid = 1
# li_lin_dashes = [5,3]
li_lin_dashes = []
# pre_lin_type = '-.'
pre_lin_type = '-'
# pre_lin_color = (255/255, 14/255, 21/255)
# pre_lin_color = (233/255, 64/255, 38/255)
pre_lin_color = (219/255, 68/255, 55/255)
pre_lin_color_up_low = (244/255, 180/255, 0/255)
pre_lin_model_wid = 1.3
pre_lin_seis_wid = 1
# pre_lin_dashes = [5,3,2,3]
pre_lin_dashes = []
real_lin_type = '-'
# real_lin_color = 'black'
real_lin_color = 'gray'
real_lin_wid = 1
real_lin_dashes = []


handlelength=3
handletextpad=0.6

####################################################################


# fig = plt.figure(figsize=figsize_para)
fig = plt.figure(figsize=figsize_para,dpi=900)
gs = fig.add_gridspec(1, 5)

####################################################################

ax1 = fig.add_subplot(gs[:,0])

ax1.plot(draw_model_pre_vp_up, draw_model_pre_depth_up, color=pre_lin_color_up_low, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_model_wid, label='model_pre_up', zorder=1)
ax1.plot(draw_model_pre_vp_low, draw_model_pre_depth_low, color=pre_lin_color_up_low, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_model_wid, label='model_pre_low', zorder=1)
ax1.fill_betweenx(draw_model_pre_depth_up, draw_model_pre_vp_up, draw_model_pre_vp_low, color=pre_lin_color_up_low, alpha=0.3, zorder=1)
ax1.plot(draw_ak135_vp, draw_ak135_depth, color=ak_lin_color, linestyle=ak_lin_type, dashes=ak_lin_dashes, linewidth=ak_lin_wid, label='ak135', zorder=2)
ax1.plot(draw_model_li_vp, draw_model_li_depth, color=li_lin_color, linestyle=li_lin_type, dashes=li_lin_dashes, linewidth=li_lin_model_wid, label='model_li', zorder=3)
ax1.plot(draw_model_pre_vp, draw_model_pre_depth, color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_model_wid, label='model_pre', zorder=4)

# ax1.legend(loc='lower left')

handles = [
    Line2D([0], [0], color=ak_lin_color, linestyle=ak_lin_type, linewidth=ak_lin_wid, dashes=ak_lin_dashes, label='AK135'),
    Line2D([0], [0], color=li_lin_color, linestyle=li_lin_type, linewidth=li_lin_model_wid, dashes=li_lin_dashes, label='Li2013'),
    Line2D([0], [0], color=pre_lin_color, linestyle=pre_lin_type, linewidth=pre_lin_model_wid, dashes=pre_lin_dashes, label='TriNet_2008'),
    Line2D([0], [0], color=pre_lin_color_up_low, linestyle=pre_lin_type, linewidth=pre_lin_model_wid, dashes=pre_lin_dashes, label='Pre_Range'),
]

# ax3.legend(handles=handles, handlelength=3, handletextpad=1.0, loc='upper right', bbox_to_anchor=[ax3_pos.x0+ax3_pos.width+0.005, ax3_pos.y0+ax3_pos.height+0.005], bbox_transform=fig.transFigure)
ax1.legend(handles=handles, handlelength=handlelength, handletextpad=handletextpad, loc='lower left')

ax1.set_xlim(8.8,11.8)
ax1.set_ylim(380, 990)

ax1.set_xticks([9,10,11])
ax1.set_yticks([400,500,600,700,800,900])

# ax1.set_xticks()
ax1.invert_yaxis()
ax1.set_ylabel('Depth (km)',fontsize=10)
ax1.set_xlabel('Vp (km/s)',fontsize=10)
ax1.set_title('Velocity Model',fontsize=10)

####################################################################

linewidth = None
# r1edgecolor=(15/255,157/255,88/255)
r1edgecolor='black'
# r2edgecolor=(15/255,157/255,88/255)
r2edgecolor='black'
r1linewidth=2
r2linewidth=2

ax2 = fig.add_subplot(gs[:,1:3])

for i in range(len(real_pro_time)):
    if i == 0:
        ax2.plot(real_pro_time[i], draw_real_pro_vp_data[i], color=real_lin_color, label='Observation', linestyle=real_lin_type, dashes=real_lin_dashes, linewidth=real_lin_wid, zorder=2)
    else:
        ax2.plot(real_pro_time[i], draw_real_pro_vp_data[i], color=real_lin_color, dashes=real_lin_dashes, linestyle=real_lin_type, linewidth=real_lin_wid, zorder=2)

for i in range(len(model_li_pro_time)):
    if i == 0:
        ax2.plot(model_li_pro_time[i], draw_model_li_pro_vp_data[i], color=li_lin_color, label='model_li', linestyle=li_lin_type, dashes=li_lin_dashes, linewidth=li_lin_seis_wid, zorder=3)
    else:
        ax2.plot(model_li_pro_time[i], draw_model_li_pro_vp_data[i], color=li_lin_color, linestyle=li_lin_type, dashes=li_lin_dashes, linewidth=li_lin_seis_wid, zorder=3)

rectangle1 = patches.Rectangle((37, 20.5), 5, 4.5, facecolor='none', edgecolor=r1edgecolor, linewidth=r1linewidth, linestyle='--', zorder=5)
rectangle2 = patches.Rectangle((40, 14), 5, 3.7, facecolor='none', edgecolor=r2edgecolor, linewidth=r2linewidth, linestyle='--', zorder=5)

ax2.add_patch(rectangle1)
ax2.add_patch(rectangle2)

ax2.text(43,24.5,'R1', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.1'))
ax2.text(46,17,'R2', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.1'))

ax2.text(26,30,'D',fontsize=10)
ax2.text(45,13,'C',fontsize=10)
ax2.text(40,25.5,'B',fontsize=10)
ax2.text(40,9.5,'A',fontsize=10)

ax2.set_xlim(25, 50)
ax2.set_ylim(9,31)
# ax2.set_ylabel('Distance (deg)',fontsize=10)
# ax2.set_ylabel('')
ax2.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)',fontsize=10)

ax2.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['','','','','','','','','','',''])
# ax2.set_yticks([])
ax2.yaxis.tick_right ()
ax2.yaxis.set_label_position('right')
# ax2.yaxis.set_visible(False)
ax2.set_title('Seismic Waveform',fontsize=10)

# ax2.legend(loc='lower left')

handles = [
    Line2D([0], [0], color=li_lin_color, linestyle=li_lin_type, linewidth=li_lin_seis_wid, dashes=li_lin_dashes, label='Li2013'),
    Line2D([0], [0], color=real_lin_color, linestyle=real_lin_type, linewidth=real_lin_wid, dashes=real_lin_dashes, label='Observation')
]

# ax3.legend(handles=handles, handlelength=3, handletextpad=1.0, loc='upper right', bbox_to_anchor=[ax3_pos.x0+ax3_pos.width+0.005, ax3_pos.y0+ax3_pos.height+0.005], bbox_transform=fig.transFigure)
ax2.legend(handles=handles, handlelength=handlelength, handletextpad=handletextpad, loc='lower left')
ax2.text(43, 30, 'CC: '+model_li_corr,fontsize=10)

####################################################################

ax3 = fig.add_subplot(gs[:,3:5])

for i in range(len(real_pro_time)):
    if i == 0:
        ax3.plot(real_pro_time[i], draw_real_pro_vp_data[i], color=real_lin_color, label='Observation', linestyle=real_lin_type, dashes=real_lin_dashes, linewidth=real_lin_wid, zorder=2)
    else:
        ax3.plot(real_pro_time[i], draw_real_pro_vp_data[i], color=real_lin_color, linestyle=real_lin_type, dashes=real_lin_dashes, linewidth=real_lin_wid, zorder=2)

for i in range(len(real_pre_pro_time)):
    if i == 0:
        ax3.plot(real_pre_pro_time[i], draw_real_pre_pro_vp_data[i], color=pre_lin_color, label='real_pre', linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_seis_wid, zorder=3)
    else:
        ax3.plot(real_pre_pro_time[i], draw_real_pre_pro_vp_data[i], color=pre_lin_color, linestyle=pre_lin_type, dashes=pre_lin_dashes, linewidth=pre_lin_seis_wid, zorder=3)

rectangle1 = patches.Rectangle((37, 20.5), 5, 4.5, facecolor='none', edgecolor=r1edgecolor, linewidth=r1linewidth, linestyle='--', zorder=5)
rectangle2 = patches.Rectangle((40, 14), 5, 3.7, facecolor='none', edgecolor=r2edgecolor, linewidth=r2linewidth, linestyle='--', zorder=5)

ax3.add_patch(rectangle1)
ax3.add_patch(rectangle2)

ax3.text(43,24.5,'R1', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.1'))
ax3.text(46,17,'R2', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.1'))


ax3.text(26,30,'D',fontsize=10)
ax3.text(45,13,'C',fontsize=10)
ax3.text(40,25.5,'B',fontsize=10)
ax3.text(40,9.5,'A',fontsize=10)

ax3.set_xlim(25, 50)
ax3.set_ylim(9,31)
ax3.set_ylabel('Distance (deg)',fontsize=10)
ax3.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)',fontsize=10)

ax3.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['10','','','','','20','','','','','30'])
# ax3.set_yticklabels(['10', '20', '30'])
ax3.yaxis.tick_right ()
ax3.yaxis.set_label_position('right')
ax3.set_title('Seismic Waveform',fontsize=10)

# ax3.legend(loc='lower left')

handles = [
    Line2D([0], [0], color=pre_lin_color, linestyle=pre_lin_type, linewidth=pre_lin_seis_wid, dashes=pre_lin_dashes, label='TriNet_2008'),
    Line2D([0], [0], color=real_lin_color, linestyle=real_lin_type, linewidth=real_lin_wid, dashes=real_lin_dashes, label='Observation')
]

# ax3.legend(handles=handles, handlelength=3, handletextpad=1.0, loc='upper right', bbox_to_anchor=[ax3_pos.x0+ax3_pos.width+0.005, ax3_pos.y0+ax3_pos.height+0.005], bbox_transform=fig.transFigure)
ax3.legend(handles=handles, handlelength=handlelength, handletextpad=handletextpad, loc='lower left')

ax3.text(43, 30, 'CC: '+pre_rerun_corr,fontsize=10)

####################################################################

fig.tight_layout()

ax1_pos = ax1.get_position()
ax2_pos = ax2.get_position()
ax3_pos = ax3.get_position()
subploticonfontsize = 10

add_aligned_text(fig, ax1_pos, '(a)', subploticonfontsize, -0.03, 0.03)
add_aligned_text(fig, ax2_pos, '(b)', subploticonfontsize, -0.03, 0.03)
add_aligned_text(fig, ax3_pos, '(c)', subploticonfontsize, -0.03, 0.03)

# plt.show()

fig.savefig('pic7_2008_v2.1.svg')
# fig.savefig('pic7_2008_v2.1.jpg')
plt.close(fig=fig)