

import os
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from draw_diff_vel_utils import *


font_path = '../../../fonts/timesnewroman/times.ttf'
fm.fontManager.addfont(font_path)


plt.rcParams['font.family'] = 'Times New Roman'


plt.rcParams['font.size'] = 16 
# plt.rcParams['axes.titlesize'] = 12
# plt.rcParams['axes.labelsize'] = 10
# plt.rcParams['xtick.labelsize'] = 10
# plt.rcParams['ytick.labelsize'] = 10
# plt.rcParams['legend.fontsize'] = 12

fig_text_size_para = 16

plt.rcParams['svg.fonttype'] = 'none'


figsize_para=(3, 6.5)
color_para = 'black'
marker_para='o'
markerfacecolor_para='red'
markeredgecolor_para='red'
markersize_para=6
linewidth_para=2

#########################

vel_base_model = get_vel_model('./vel_base_model.dat')
vel_interpolation = get_vel_model('./vel_interpolation.dat')
vel_modify_layer_depth = get_vel_model('./vel_modify_layer_depth.dat')
vel_modify_model = get_vel_model('./vel_modify_velocity.dat')


vel_base_model_vp = vel_base_model['vp']
vel_interpolation_vp = vel_interpolation['vp']
vel_modify_layer_depth_vp = vel_modify_layer_depth['vp']
vel_modify_model_vp = vel_modify_model['vp']

vel_base_model_depth = vel_base_model['depth']
vel_interpolation_depth = vel_interpolation['depth']
vel_modify_layer_depth_depth = vel_modify_layer_depth['depth']
vel_modify_model_depth = vel_modify_model['depth']


draw_depth = [510.0, 1000.0]

draw_vel_base_layer_num = 0
for i in range(len(vel_base_model_depth)):
    if vel_base_model_depth[i]>draw_depth[0] and vel_base_model_depth[i]<draw_depth[1]:
        draw_vel_base_layer_num = draw_vel_base_layer_num +1
begin_vel_base_draw_num = 0
for i in range(len(vel_base_model_depth)):
    if vel_base_model_depth[i] < draw_depth[0]:
        begin_vel_base_draw_num = begin_vel_base_draw_num +1

draw_vel_modify_layer_num = 0
for i in range(len(vel_modify_model_depth)):
    if vel_modify_model_depth[i]>draw_depth[0] and vel_modify_model_depth[i]<draw_depth[1]:
        draw_vel_modify_layer_num = draw_vel_modify_layer_num +1
begin_vel_modify_layer_num = 0
for i in range(len(vel_modify_model_depth)):
    if vel_modify_model_depth[i] < draw_depth[0]:
        begin_vel_modify_layer_num = begin_vel_modify_layer_num +1



fig1 = plt.figure(figsize=figsize_para)
ax1 = fig1.add_subplot(111)

ax1.plot(
    vel_base_model_vp[begin_vel_base_draw_num : begin_vel_base_draw_num + draw_vel_base_layer_num],
    vel_base_model_depth[begin_vel_base_draw_num : begin_vel_base_draw_num + draw_vel_base_layer_num],
    color=color_para,
    marker=marker_para,
    markerfacecolor=markerfacecolor_para,
    markeredgecolor=markeredgecolor_para,
    markersize=markersize_para,
    linewidth=linewidth_para,
    label ='vel_base'
    )

ax1.invert_yaxis()

ax1.set_ylabel('Depth (km)')
ax1.set_xlabel('Vp (km/s)')

fig1.text(0.02, 0.96, '(a)')
# fig1.text(0.02, 0.96, '(a)', fontsize=fig_text_size_para, va='top', ha='left')

plt.tight_layout()
fig1.savefig('./vel_base_model.svg')


fig2 = plt.figure(figsize=figsize_para)
ax2 = fig2.add_subplot(111)

ax2.plot(
    vel_interpolation_vp[begin_vel_modify_layer_num : begin_vel_modify_layer_num + draw_vel_modify_layer_num],
    vel_interpolation_depth[begin_vel_modify_layer_num : begin_vel_modify_layer_num + draw_vel_modify_layer_num],
    color=color_para,
    marker=marker_para,
    markerfacecolor=markerfacecolor_para,
    markeredgecolor=markeredgecolor_para,
    markersize=markersize_para,
    linewidth=linewidth_para,
    label ='vel_interpolation'
    )

ax2.invert_yaxis()

ax2.set_ylabel('Depth (km)')
ax2.set_xlabel('Vp (km/s)')

fig1.text(0.02, 0.96, '(b)')

plt.tight_layout()
fig2.savefig('./vel_interpolation.svg')


fig3 = plt.figure(figsize=figsize_para)
ax3 = fig3.add_subplot(111)

ax3.plot(
    vel_modify_layer_depth_vp[begin_vel_modify_layer_num : begin_vel_modify_layer_num + draw_vel_modify_layer_num],
    vel_modify_layer_depth_depth[begin_vel_modify_layer_num : begin_vel_modify_layer_num + draw_vel_modify_layer_num],
    color=color_para,
    marker=marker_para,
    markerfacecolor=markerfacecolor_para,
    markeredgecolor=markeredgecolor_para,
    markersize=markersize_para,
    linewidth=linewidth_para,
    label ='vel_modify_layer_depth'
    )

ax3.invert_yaxis()

ax3.set_ylabel('Depth (km)')
ax3.set_xlabel('Vp (km/s)')

fig3.text(0.02, 0.96, '(c)')

plt.tight_layout()
fig3.savefig('./vel_modify_layer_depth.svg')


fig4 = plt.figure(figsize=figsize_para)
ax4 = fig4.add_subplot(111)

ax4.plot(
    vel_modify_model_vp[begin_vel_modify_layer_num : begin_vel_modify_layer_num + draw_vel_modify_layer_num],
    vel_modify_model_depth[begin_vel_modify_layer_num : begin_vel_modify_layer_num + draw_vel_modify_layer_num],
    color=color_para,
    marker=marker_para,
    markerfacecolor=markerfacecolor_para,
    markeredgecolor=markeredgecolor_para,
    markersize=markersize_para,
    linewidth=linewidth_para,
    label ='vel_modify_model'
    )

ax4.invert_yaxis()

ax4.set_ylabel('Depth (km)')
ax4.set_xlabel('Vp (km/s)')

fig4.text(0.02, 0.96, '(d)')

plt.tight_layout()
fig4.savefig('./vel_modify_model.svg')

###############################################################

fig4 = plt.figure(figsize=(2.5, 6.5))
ax4 = fig4.add_subplot(111)

ax4.plot(
    vel_modify_model_vp[begin_vel_modify_layer_num : begin_vel_modify_layer_num + draw_vel_modify_layer_num],
    vel_modify_model_depth[begin_vel_modify_layer_num : begin_vel_modify_layer_num + draw_vel_modify_layer_num],
    color='black',
    marker=marker_para,
    markerfacecolor=markerfacecolor_para,
    markeredgecolor=markeredgecolor_para,
    markersize=markersize_para,
    linewidth=linewidth_para,
    label ='vel_modify_model'
    )

ax4.invert_yaxis()

ax4.set_ylabel('Depth (km)')
ax4.set_xlabel('Vp (km/s)')


plt.tight_layout()
fig4.savefig('./vel_modify_model_pic2.svg')
