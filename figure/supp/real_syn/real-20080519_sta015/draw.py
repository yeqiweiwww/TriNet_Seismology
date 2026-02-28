
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from copy import deepcopy
from pandas.core.frame import DataFrame
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerBase
from matplotlib.text import Text

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

def get_rebuild_data_real(path):
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

class HandlerLineText(HandlerBase):
    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):

        line_y = ydescent + height * 1.30
        line = Line2D(
            [xdescent, xdescent + width],
            [line_y, line_y],
            linestyle=orig_handle.get_linestyle(),
            linewidth=orig_handle.get_linewidth(),
            color=orig_handle.get_color(),
            transform=trans
        )

        text_y = ydescent + height * -0.30
        text = Text(
            xdescent + width * 0.5,
            text_y,
            orig_handle.get_label(),
            ha="center",
            va="center",
            fontsize=fontsize,
            transform=trans
        )

        return [line, text]

##########################################################


cut_time_start_time = 15
cut_time_windows = 40
reduction_v = 10

##########################################################

font_path = '../../../fonts/timesnewroman/times.ttf'
fm.fontManager.addfont(font_path)

plt.rcParams['font.family'] = 'Times New Roman'

plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8

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
pre_ori_lin_type = '-'
pre_ori_lin_color = (66/255, 133/255, 244/255)
pre_ori_lin_model_wid = 1.3
pre_ori_lin_seis_wid = 1
pre_ori_lin_dashes = []
pre_new_lin_type = '-'
pre_new_lin_color = (219/255, 68/255, 55/255)
pre_new_lin_color_up_low = (244/255, 180/255, 0/255)
pre_new_lin_model_wid = 1.3
pre_new_lin_seis_wid = 1
pre_new_lin_dashes = []



handlelength=3
handletextpad=0.6
##########################################################
ak135_file_path = '../../ak135_inter.dat'

ak135_vel_dic = get_ak_vel_model(ak135_file_path)


pre_ori_vel_file_path = '../real-20080519/pre_vel.dat'

obs_rebuild_seis_file_path = '../real-20080519/rebuild_real.dat'


pre_ori_vel_dic = get_modi_vel_model(pre_ori_vel_file_path)

rebui_time_obs, rebui_vp_data_obs, rebui_sta_location_obs, rebui_use_index_obs = get_rebuild_data_real(obs_rebuild_seis_file_path)


locdata = rebui_sta_location_obs

draw_pre_ori_vel_depth = []
draw_pre_ori_vel_vp = []
for i in range(len(pre_ori_vel_dic['depth'])):
    if pre_ori_vel_dic['depth'][i]>draw_depth_para[0] and pre_ori_vel_dic['depth'][i]<draw_depth_para[1]:
        draw_pre_ori_vel_depth.append(pre_ori_vel_dic['depth'][i])
        draw_pre_ori_vel_vp.append(pre_ori_vel_dic['vp'][i])

draw_rebui_obs = []
for i in range(len(rebui_vp_data_obs)):
    draw_rebui_obs.append([])
    for j in range(len(rebui_vp_data_obs[i])):
        draw_rebui_obs[-1].append(rebui_vp_data_obs[i][j]/2+locdata[i])


##########################################################
pre_new_vel_file_path = './pre_vel.dat'
pre_new_vel_up_file_path = './pre_vel_up.dat'
pre_new_vel_low_file_path = './pre_vel_low.dat'

input_seis_file_path = './input_rebuild_seis.dat'
pre_new_rebuild_seis_file_path = './pre_rebuild.dat'

pre_new_vel_dic = get_pre_vel_model(pre_new_vel_file_path)
pre_new_up_vel_dic = get_pre_vel_model(pre_new_vel_up_file_path)
pre_new_low_vel_dic = get_pre_vel_model(pre_new_vel_low_file_path)

inp_rebui_time, inp_rebui_vp_data, inp_rebui_sta_location, inp_rebui_use_index = get_rebuild_data_real(input_seis_file_path)
pre_new_rebui_time, pre_new_rebui_vp_data, pre_new_rebui_sta_location, pre_new_rebui_use_index = get_rebuild_data(pre_new_rebuild_seis_file_path)

draw_pre_new_vel_depth = []
draw_pre_new_vel_vp = []
for i in range(len(pre_new_vel_dic['depth'])):
    if pre_new_vel_dic['depth'][i]>draw_depth_para[0] and pre_new_vel_dic['depth'][i]<draw_depth_para[1]:
        draw_pre_new_vel_depth.append(pre_new_vel_dic['depth'][i])
        draw_pre_new_vel_vp.append(pre_new_vel_dic['vp'][i])

draw_model_pre_new_depth_up = []
draw_model_pre_new_vp_up = []
for i in range(len(pre_new_up_vel_dic['depth'])):
    if pre_new_up_vel_dic['depth'][i]>draw_depth_para[0] and pre_new_up_vel_dic['depth'][i]<draw_depth_para[1]:
        draw_model_pre_new_depth_up.append(pre_new_up_vel_dic['depth'][i])
        draw_model_pre_new_vp_up.append(pre_new_up_vel_dic['vp'][i])

draw_model_pre_new_depth_low = []
draw_model_pre_new_vp_low = []
for i in range(len(pre_new_low_vel_dic['depth'])):
    if pre_new_low_vel_dic['depth'][i]>draw_depth_para[0] and pre_new_low_vel_dic['depth'][i]<draw_depth_para[1]:
        draw_model_pre_new_depth_low.append(pre_new_low_vel_dic['depth'][i])
        draw_model_pre_new_vp_low.append(pre_new_low_vel_dic['vp'][i])


draw_inp_rebui = []
for i in range(len(inp_rebui_vp_data)):
    draw_inp_rebui.append([])
    for j in range(len(inp_rebui_vp_data[i])):
        draw_inp_rebui[-1].append(inp_rebui_vp_data[i][j]/2+locdata[i])

draw_pre_new_rebui = []
for i in range(len(pre_new_rebui_vp_data)):
    draw_pre_new_rebui.append([])
    for j in range(len(pre_new_rebui_vp_data[i])):
        draw_pre_new_rebui[-1].append(pre_new_rebui_vp_data[i][j]/2+locdata[i])


fig = plt.figure(figsize=figsize_para,dpi=900)
gs = fig.add_gridspec(1, 5)

ax1 = fig.add_subplot(gs[:,0:2])
ax2 = fig.add_subplot(gs[:,2])
ax3 = fig.add_subplot(gs[:,3:5])


for i in range(len(draw_inp_rebui)):
    if i in inp_rebui_use_index:
        ax1.plot(rebui_time_obs[i], draw_inp_rebui[i], color=inp_lin_color, linestyle=inp_lin_type, dashes=inp_lin_dashes, linewidth=inp_lin_seis_wid)


ax1.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax1.set_ylim(9,31)
ax1.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['10','','','','','20','','','','','30'])
ax1.set_ylabel('Distance (deg)')
ax1.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')
ax1.text(48, 28.5, 'Sta:\n15', bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))

ax1.text(19, 29, '20080519', bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))

ax1.set_title('Input Seismic Waveform')


ax2.plot(draw_model_pre_new_vp_up, draw_model_pre_new_depth_up, color=pre_new_lin_color_up_low, linestyle=pre_new_lin_type, dashes=pre_new_lin_dashes, linewidth=pre_new_lin_model_wid, label='model_pre_up', zorder=1)
ax2.plot(draw_model_pre_new_vp_low, draw_model_pre_new_depth_low, color=pre_new_lin_color_up_low, linestyle=pre_new_lin_type, dashes=pre_new_lin_dashes, linewidth=pre_new_lin_model_wid, label='model_pre_low', zorder=1)
ax2.fill_betweenx(draw_model_pre_new_depth_up, draw_model_pre_new_vp_up, draw_model_pre_new_vp_low, color=pre_new_lin_color_up_low, alpha=0.3, zorder=1)
ax2.plot(draw_pre_ori_vel_vp, draw_pre_ori_vel_depth, color=pre_ori_lin_color, linestyle=pre_ori_lin_type, dashes=pre_ori_lin_dashes, linewidth=pre_ori_lin_model_wid, label='modi', zorder=2)
ax2.plot(draw_pre_new_vel_vp, draw_pre_new_vel_depth, color=pre_new_lin_color, linestyle=pre_new_lin_type, dashes=pre_new_lin_dashes, linewidth=pre_new_lin_model_wid, label='pre', zorder=3)

idx_b=17
idx_e=31
idx_6601=22
idx_6602=23

ak_vp=ak135_vel_dic['vp'][idx_b:idx_e+1]
ak6601=ak135_vel_dic['depth'][idx_6601]
ak6602=ak135_vel_dic['depth'][idx_6602]
akthi=ak6602-ak6601
pre_ori_vp=pre_ori_vel_dic['vp'][idx_b:idx_e+1]
pre_ori6601=pre_ori_vel_dic['depth'][idx_6601]
pre_ori6602=pre_ori_vel_dic['depth'][idx_6602]
pre_orithi=pre_ori6602-pre_ori6601
pre_new_vp=pre_new_vel_dic['vp'][idx_b:idx_e+1]
pre_new6601=pre_new_vel_dic['depth'][idx_6601]
pre_new6602=pre_new_vel_dic['depth'][idx_6602]
pre_newthi=pre_new6602-pre_new6601

all_loss = []
for i in range(len(pre_ori_vp)):
    all_loss.append(((pre_new_vp[i]-pre_ori_vp[i])/ak_vp[i]/0.03)**2)

all_loss.append(((pre_new6601-pre_ori6601)/30)**2)
all_loss.append(((pre_newthi-pre_orithi)/30)**2)

all_loss = np.sqrt(np.mean(all_loss))

ax2.text(10.2, 447, 'Diff:\n'+f"{all_loss:.3f}", bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))

handles = [
    Line2D([0], [0], color=pre_ori_lin_color, linestyle=pre_ori_lin_type, linewidth=pre_ori_lin_seis_wid, dashes=pre_ori_lin_dashes, label='Rawdata'),
    Line2D([0], [0], color=pre_new_lin_color, linestyle=pre_new_lin_type, linewidth=pre_new_lin_seis_wid, dashes=pre_new_lin_dashes, label='Sta015'),
]

ax2.legend(
    handles=handles,
    handler_map={Line2D: HandlerLineText()},
    labels=['',''],
    loc='lower left',
    handlelength=2,
    borderpad=1.2,
    labelspacing=1.2,
    handletextpad=0,
    frameon=True
)
ax2.set_xlim(8.8,11.8)
ax2.set_ylim(380, 990)

ax2.set_xticks([9,10,11])
ax2.set_yticks([400,500,600,700,800,900])

ax2.invert_yaxis()
ax2.set_ylabel('Depth (km)')
ax2.set_xlabel('Vp (km/s)')
ax2.set_title('Velocity Model')


for i in range(len(draw_rebui_obs)):
    ax3.plot(rebui_time_obs[i], draw_rebui_obs[i], color=pre_ori_lin_color, linestyle=pre_ori_lin_type, dashes=pre_ori_lin_dashes, linewidth=pre_ori_lin_seis_wid)

for i in range(len(draw_pre_new_rebui)):
    ax3.plot(rebui_time_obs[i], draw_pre_new_rebui[i], color=pre_new_lin_color, linestyle=pre_new_lin_type, dashes=pre_new_lin_dashes, linewidth=pre_new_lin_seis_wid)



ax3.set_xlim(cut_time_start_time_para, cut_time_start_time_para+cut_time_windows_para)
ax3.set_ylim(9,31)
ax3.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['10','','','','','20','','','','','30'])
ax3.set_ylabel('Distance (deg)')
ax3.set_xlabel('t-'+'Distance*'+str(reduction_v_para)+' (s)')

ax3.set_title('Seismic Waveform')


handles = [
    Line2D([0], [0], color=pre_ori_lin_color, linestyle=pre_ori_lin_type, linewidth=pre_ori_lin_seis_wid, dashes=pre_ori_lin_dashes, label='Observation'),
    Line2D([0], [0], color=pre_new_lin_color, linestyle=pre_new_lin_type, linewidth=pre_new_lin_seis_wid, dashes=pre_new_lin_dashes, label='Sta015'),
]

corr_all = []

for i in range(len(rebui_vp_data_obs)):
    corr_all.append(np.corrcoef(rebui_vp_data_obs[i], pre_new_rebui_vp_data[i])[0][1])

corr = np.mean(corr_all)


ax3.legend(handles=handles, handlelength=handlelength, handletextpad=handletextpad, loc='lower left')
ax3.text(46, 28.5, 'CC:\n'+f"{corr:.3f}", bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, boxstyle='round,pad=0.5'))
# ax3.text(43, 30.15, 'CC: 0.970')

fig.text(0.02, 0.96, '(a)')
fig.tight_layout()
fig.savefig('real_20080519_sta015.svg')

