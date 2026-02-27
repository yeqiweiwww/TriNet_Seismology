

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from copy import deepcopy
##########################################################

def read_inputfile(inputfile_path):
    input_file = open(inputfile_path, 'r')
    input_content = input_file.readlines()
    input_file.close()

    return input_content

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

##########################################################

locnum_lin = 12
locdata_lin = 13

cut_time_start_time = 15
cut_time_windows = 40
reduction_v = 10

##########################################################
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


figsize_para=(6, 6)
color_para = 'blue'
marker_para='o'
markerfacecolor_para='red'
markeredgecolor_para='red'
markersize_para=6
linewidth_para=3

##########################################################


input_file_path = './modified_inputfile/modify_inputfile_example.inp'
input_content = read_inputfile(input_file_path)

locnum = int(input_content[locnum_lin].split()[0])
locdata = []
for j in range(locnum):
    locdata.append(float(input_content[locdata_lin].split()[j]))

##########################################################
file_path = './rebuild_vp_seis_example1.dat'

pro_time, pro_vp_data, sta_location, use_index = get_rebuild_data(file_path)

draw_data = []
for i in range(len(pro_vp_data)):
    draw_data.append([])
    for j in range(len(pro_vp_data[i])):
        draw_data[-1].append(pro_vp_data[i][j]/2+locdata[i])

fig1 = plt.figure(figsize=figsize_para)
ax1 = fig1.add_subplot()

for i in range(len(locdata)):
    if i in use_index:
        ax1.plot(pro_time[i], draw_data[i], 'k')

ax1.set_xlim(cut_time_start_time, cut_time_start_time+cut_time_windows)
ax1.set_ylim(9,31)
ax1.set_ylabel('Distance (deg)')
ax1.set_xlabel('t-'+'Distance*'+str(reduction_v)+' (s)')

# locdata_pic = [10.0,20.0,30.0]
# locdata_str=[]

# for i in range(len(locdata_pic)):
#     locdata_str.append(str(locdata_pic[i]))

ax1.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['10','','','','','20','','','','','30'])
# ax1.set_yticklabels(locdata_str)
# ax1.yaxis.tick_right()
# ax1.yaxis.set_label_position('right')
# ax1.set_title('Seismic wave')
fig1.text(0.02, 0.96, '(b)', fontsize=fig_text_size_para, va='top', ha='left')

fig_pic_path = './example1'
fig1.tight_layout()
fig1.savefig(fname=fig_pic_path+'.svg',format='svg')
##########################################################
file_path = './rebuild_vp_seis_example2.dat'

pro_time, pro_vp_data, sta_location, use_index = get_rebuild_data(file_path)

draw_data = []
for i in range(len(pro_vp_data)):
    draw_data.append([])
    for j in range(len(pro_vp_data[i])):
        draw_data[-1].append(pro_vp_data[i][j]/2+locdata[i])

fig1 = plt.figure(figsize=figsize_para)
ax1 = fig1.add_subplot()

for i in range(len(locdata)):
    if i in use_index:
        ax1.plot(pro_time[i], draw_data[i], 'k')

ax1.set_xlim(cut_time_start_time, cut_time_start_time+cut_time_windows)
ax1.set_ylim(9,31)
ax1.set_ylabel('Distance (deg)')
ax1.set_xlabel('t-'+'Distance*'+str(reduction_v)+' (s)')

# locdata_pic = [10.0,20.0,30.0]
# locdata_str=[]

# for i in range(len(locdata_pic)):
#     locdata_str.append(str(locdata_pic[i]))

ax1.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['10','','','','','20','','','','','30'])
# ax1.set_yticklabels(locdata_str)
# ax1.yaxis.tick_right()
# ax1.yaxis.set_label_position('right')
# ax1.set_title('Seismic wave')
fig1.text(0.02, 0.96, '(c)', fontsize=fig_text_size_para, va='top', ha='left')

fig_pic_path = './example2'
fig1.tight_layout()
fig1.savefig(fname=fig_pic_path+'.svg',format='svg')
##########################################################
file_path = './rebuild_vp_seis_example3.dat'

pro_time, pro_vp_data, sta_location, use_index = get_rebuild_data(file_path)

draw_data = []
for i in range(len(pro_vp_data)):
    draw_data.append([])
    for j in range(len(pro_vp_data[i])):
        draw_data[-1].append(pro_vp_data[i][j]/2+locdata[i])

fig1 = plt.figure(figsize=figsize_para)
ax1 = fig1.add_subplot()

for i in range(len(locdata)):
    if i in use_index:
        ax1.plot(pro_time[i], draw_data[i], 'k')

ax1.set_xlim(cut_time_start_time, cut_time_start_time+cut_time_windows)
ax1.set_ylim(9,31)
ax1.set_ylabel('Distance (deg)')
ax1.set_xlabel('t-'+'Distance*'+str(reduction_v)+' (s)')

# locdata_pic = [10.0,20.0,30.0]
# locdata_str=[]

# for i in range(len(locdata_pic)):
#     locdata_str.append(str(locdata_pic[i]))

ax1.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['10','','','','','20','','','','','30'])
# ax1.set_yticklabels(locdata_str)
# ax1.yaxis.tick_right()
# ax1.yaxis.set_label_position('right')
# ax1.set_title('Seismic wave')
fig1.text(0.02, 0.96, '(d)', fontsize=fig_text_size_para, va='top', ha='left')

fig_pic_path = './example3'
fig1.tight_layout()
fig1.savefig(fname=fig_pic_path+'.svg',format='svg')
##########################################################
file_path = './rebuild_vp_seis_example0.dat'

pro_time, pro_vp_data, sta_location, use_index = get_rebuild_data(file_path)

draw_data = []
for i in range(len(pro_vp_data)):
    draw_data.append([])
    for j in range(len(pro_vp_data[i])):
        draw_data[-1].append(pro_vp_data[i][j]/2+locdata[i])

fig1 = plt.figure(figsize=figsize_para)
ax1 = fig1.add_subplot()

for i in range(len(locdata)):
    if i in use_index:
        ax1.plot(pro_time[i], draw_data[i], 'k')

ax1.set_xlim(100, 400)
ax1.set_ylim(9,31)
ax1.set_ylabel('Distance (deg)')
ax1.set_xlabel('t (s)')

# locdata_pic = [10.0,20.0,30.0]
# locdata_str=[]

# for i in range(len(locdata_pic)):
#     locdata_str.append(str(locdata_pic[i]))

ax1.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['10','','','','','20','','','','','30'])
# ax1.set_yticklabels(locdata_str)
# ax1.yaxis.tick_right()
# ax1.yaxis.set_label_position('right')
# ax1.set_title('Seismic wave')
fig1.text(0.02, 0.96, '(a)', fontsize=fig_text_size_para, va='top', ha='left')

fig_pic_path = './example0'
fig1.tight_layout()
fig1.savefig(fname=fig_pic_path+'.svg',format='svg')
##########################################################
file_path = './rebuild_vp_seis_example3.dat'

pro_time, pro_vp_data, sta_location, use_index = get_rebuild_data(file_path)

draw_data = []
for i in range(len(pro_vp_data)):
    draw_data.append([])
    for j in range(len(pro_vp_data[i])):
        draw_data[-1].append(pro_vp_data[i][j]/2+locdata[i])

fig1 = plt.figure(figsize=figsize_para)
ax1 = fig1.add_subplot()

for i in range(len(locdata)):
    if i in use_index:
        ax1.plot(pro_time[i], draw_data[i], 'k')

ax1.set_xlim(15, 55)
ax1.set_ylim(9,31)
ax1.set_ylabel('Distance (deg)')
ax1.set_xlabel('t-'+'Distance*'+str(reduction_v)+' (s)')

# locdata_pic = [10.0,20.0,30.0]
# locdata_str=[]

# for i in range(len(locdata_pic)):
#     locdata_str.append(str(locdata_pic[i]))

ax1.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['10','','','','','20','','','','','30'])
# ax1.set_yticklabels(locdata_str)
# ax1.yaxis.tick_right()
# ax1.yaxis.set_label_position('right')
# ax1.set_title('Seismic wave')
# fig1.text(0.02, 0.96, '(d)', fontsize=fig_text_size_para, va='top', ha='left')
# ax1.set_axis_off()
fig_pic_path = './example_pic2'
fig1.tight_layout()
fig1.savefig(fname=fig_pic_path+'.svg',format='svg')
