

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.lines import Line2D

from obspy.taup import TauPyModel

from draw_pic1_util import vel_base, read_three_raypath, get_rebuild_data, add_aligned_text

############################################


font_path = '../../fonts/timesnewroman/times.ttf'
fm.fontManager.addfont(font_path)


plt.rcParams['font.family'] = 'Times New Roman'


plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10

plt.rcParams['svg.fonttype'] = 'none'

# fig = plt.figure(figsize=(7.5,7.5))
fig = plt.figure(figsize=(7.5,7.5),dpi=900)
gs = fig.add_gridspec(4, 5)

ax2 = fig.add_subplot(gs[0:3,1:5])
ax4 = fig.add_subplot(gs[0:2,0])
ax3 = fig.add_subplot(gs[1:4,1:5])
ax1 = fig.add_subplot(gs[2:4,0])

ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()

ax3.yaxis.set_label_position("right")
ax3.yaxis.tick_right()
ax3.set_xlabel('temp')
ax3.set_ylabel('temp')

ax1.set_xlabel('temp')
ax1.set_ylabel('temp')
ax4.set_xlabel('temp')
ax4.set_ylabel('temp')

fig.tight_layout()

ax1_pos = ax1.get_position()
ax2_pos = ax2.get_position()
ax3_pos = ax3.get_position()
ax4_pos = ax4.get_position()

fig.clf()

############################################
############################################

ax2_factor = 1.9

dis_linewidth = 2
dis_linecolor = 'black'

raypath_linewidth = 1.5
raypath_linealpha = 0.8
raypath_linecolor1 = (255/255, 0/255, 0/255) # ab
raypath_linecolor2 = (0/255, 255/255, 0/255) # bc
raypath_linecolor3 = (0/255, 0/255, 255/255) # cd
# raypath_linecolor1 = '#72b043' # ab
# raypath_linecolor2 = '#e12729' # bc
# raypath_linecolor3 = '#0c8fc7' # cd

source_markercolor = 'black'
source_markersize = 150
sta_markercolor = 'black'


ax2_pos_width = ax2_pos.width*ax2_factor
ax2_pos_height = ax2_pos.height*ax2_factor
ax2_pos_x0 = ax2_pos.x0 - (ax2_pos_width - ax2_pos.width) / 2
ax2_pos_y0 = ax2_pos.y0 - (ax2_pos_height - ax2_pos.height) - 0.01

ax2 = fig.add_axes([ax2_pos_x0, ax2_pos_y0, ax2_pos_width, ax2_pos_height],projection='polar')

ak135_raypath_file_path = '../pic1_tauppath/ak135_interpo.gmt'

num = 5000

sta_dis = 20
source_depth = 519

x_min = 75/180*np.pi
x_max = 105/180*np.pi

y_factor = 1
x_plus = 100 # degree

rad_ear = 6371
rad_0 = rad_ear - 0
rad_410 = rad_ear - 410
rad_660 = rad_ear - 660
rad_source_depth = rad_ear - source_depth

rad_0 = rad_0**y_factor
rad_410 = rad_410**y_factor
rad_660 = rad_660**y_factor
rad_source_depth = rad_source_depth**y_factor

dis_0_y = np.full(num, rad_0)
dis_410_y = np.full(num, rad_410)
dis_660_y = np.full(num, rad_660)

dis_0_x = np.linspace(x_min, x_max, num)
dis_410_x = np.linspace(x_min, x_max, num)
dis_660_x = np.linspace(x_min, x_max, num)


sta_line = 100
sta_angles_1 = (x_plus-sta_dis)/180*np.pi
sta_rad_1 = rad_0

sta_rad_2 = np.sqrt(sta_line**2 + rad_0**2 - 2*sta_line*rad_0*np.cos(150/180*np.pi))
dis_angle = np.arccos((sta_rad_2**2 + rad_0**2 - sta_line**2)/(2*sta_rad_2*rad_0))

sta_angles_2 = sta_angles_1 - dis_angle
sta_angles_3 = sta_angles_1 + dis_angle

sta_rad_3 = sta_rad_2

# raypath

raypath_x_all_ak135, raypath_y_all_ak135 = read_three_raypath(ak135_raypath_file_path, x_plus, y_factor)

ax2.plot(dis_0_x, dis_0_y, color=dis_linecolor, linewidth=dis_linewidth)
ax2.plot(dis_410_x, dis_410_y, color=dis_linecolor, linewidth=dis_linewidth)
ax2.plot(dis_660_x, dis_660_y, color=dis_linecolor, linewidth=dis_linewidth)

ax2.plot(raypath_x_all_ak135[1], raypath_y_all_ak135[1], color=raypath_linecolor1, linewidth=raypath_linewidth, alpha=raypath_linealpha, zorder=3, label='AB')
ax2.plot(raypath_x_all_ak135[2], raypath_y_all_ak135[2], color=raypath_linecolor2, linewidth=raypath_linewidth, alpha=raypath_linealpha, zorder=2, label='BC')
ax2.plot(raypath_x_all_ak135[0], raypath_y_all_ak135[0], color=raypath_linecolor3, linewidth=raypath_linewidth, alpha=raypath_linealpha, zorder=1, label='CD')

ax2.scatter(x_plus/180*np.pi, (rad_ear-source_depth)**y_factor, marker='*', c=source_markercolor, s=source_markersize, zorder=4)

ax2.fill([sta_angles_1, sta_angles_2, sta_angles_3], [sta_rad_1, sta_rad_2, sta_rad_3], color=sta_markercolor, zorder=4)

ax2.text((x_plus+5)/180*np.pi, (rad_ear-source_depth)**y_factor-20, "Earthquake", fontsize=10)
ax2.text((x_plus-sta_dis+2)/180*np.pi, rad_0+100, "Station", fontsize=10)

ax2.legend(loc='upper right', bbox_to_anchor=[ax2_pos.x0+ax2_pos.width+0.005, ax2_pos.y0+ax2_pos.height+0.005], bbox_transform=fig.transFigure)

ax2.set_xlim(x_min-5/180*np.pi, x_max+5/180*np.pi)
ax2.set_ylim(0, (rad_ear+100)**y_factor)

ax2.set_axis_off()

############################################

ak135_model_linestyle = '-'
ak135_model_linewidth = 1.5
ak135_model_linecolor = 'gray'
ak135_model_dashset = []

model_li_model_linestyle = '-'
model_li_model_linewidth = ak135_model_linewidth
model_li_model_linecolor = 'red'
model_li_model_maker = None
model_li_model_makercolor = None
model_li_model_makersize = None
model_li_model_dashset = []
# model_li_model_dashset = []


ax1 = fig.add_axes([ax1_pos.x0, ax1_pos.y0, ax1_pos.width, ax1_pos.height])

model_ak135 = vel_base('../ak135/modified_modelfile/modify_model_ak135.dat')
model_li = vel_base('../model_li/modified_modelfile/modify_model_model_li.dat')

depth_ak135 = model_ak135['depth']
depth_li = model_li['depth']
vp_ak135 = model_ak135['vp']
vp_li = model_li['vp']

draw_depth = [450, 1050]

start_index_ak135 = next((i for i, x in enumerate(depth_ak135) if x > draw_depth[0]), None)
end_index_ak135 = next((i for i, x in enumerate(depth_ak135) if x > draw_depth[1]), None)

start_index_li = next((i for i, x in enumerate(depth_li) if x > draw_depth[0]), None)
end_index_li = next((i for i, x in enumerate(depth_li) if x > draw_depth[1]), None)

ax1.plot(vp_ak135[start_index_ak135:end_index_ak135], depth_ak135[start_index_ak135:end_index_ak135], linestyle=ak135_model_linestyle, dashes=ak135_model_dashset, linewidth = ak135_model_linewidth, label='ak135', color=ak135_model_linecolor)
ax1.plot(vp_li[start_index_li:end_index_li],depth_li[start_index_li:end_index_li], linestyle=model_li_model_linestyle, dashes=model_li_model_dashset, linewidth = model_li_model_linewidth, label='li_2013', color=model_li_model_linecolor, marker=model_li_model_maker, markerfacecolor=model_li_model_makercolor, markeredgecolor=model_li_model_makercolor, markersize = model_li_model_makersize)
ax1.invert_yaxis()

ax1.set_ylabel('Depth (km)')
ax1.set_xlabel('Vp (km/s)')
# ax1.legend(loc='upper right')


############################################

reduction_v = 10

ak135_seis_linecolor = ak135_model_linecolor
ak135_seis_linewidth = 2
ak135_seis_linestyle = ak135_model_linestyle
ak135_seis_dashset = ak135_model_dashset

model_li_seis_linecolor = model_li_model_linecolor
model_li_seis_linewidth = ak135_seis_linewidth
model_li_seis_linestyle = model_li_model_linestyle
model_li_seis_dashset = model_li_model_dashset

ax3 = fig.add_axes([ax3_pos.x0, ax3_pos.y0, ax3_pos.width, ax3_pos.height])

pro_time_ak135, pro_vp_data_ak135, sta_location_ak135, use_index_ak135 = get_rebuild_data('../ak135/seis_rebuild_data/rebuild_vp_seis_ak135.dat')

for i in range(len(sta_location_ak135)):
    locrv = sta_location_ak135[i]
    for j in range(len(pro_vp_data_ak135[i])):
        pro_vp_data_ak135[i][j] = pro_vp_data_ak135[i][j]/2 + locrv

index_label = 0
for i in range(len(sta_location_ak135)):
    if i in use_index_ak135:
        if index_label == 0 and i%2 == 0:
            ax3.plot(pro_time_ak135[i], pro_vp_data_ak135[i], color=ak135_seis_linecolor, linewidth=ak135_seis_linewidth, linestyle=ak135_seis_linestyle, dashes=ak135_seis_dashset, label='AK135')
            index_label += 1
        elif i%2 == 0:
            ax3.plot(pro_time_ak135[i], pro_vp_data_ak135[i], color=ak135_seis_linecolor, linewidth=ak135_seis_linewidth, linestyle=ak135_seis_linestyle, dashes=ak135_seis_dashset)


pro_time_model_li, pro_vp_data_model_li, sta_location_model_li, use_index_model_li = get_rebuild_data('../model_li/seis_rebuild_data/rebuild_vp_seis_model_li.dat')

for i in range(len(sta_location_model_li)):
    locrv = sta_location_model_li[i]
    for j in range(len(pro_vp_data_model_li[i])):
        pro_vp_data_model_li[i][j] = pro_vp_data_model_li[i][j]/2 + locrv

index_label = 0
for i in range(len(sta_location_model_li)):
    if i in use_index_model_li:
        if index_label == 0 and i%2 == 0:
            ax3.plot(pro_time_model_li[i], pro_vp_data_model_li[i], color=model_li_seis_linecolor, linewidth=model_li_seis_linewidth, linestyle=model_li_seis_linestyle, dashes=model_li_seis_dashset, label='Li_2013')
            index_label += 1
        elif i%2 == 0:
            ax3.plot(pro_time_model_li[i], pro_vp_data_model_li[i], color=model_li_seis_linecolor, linewidth=model_li_seis_linewidth, linestyle=model_li_seis_linestyle, dashes=model_li_seis_dashset)

ax3.text(26,30.3,'D',fontsize=10)
ax3.text(46,11,'C',fontsize=10)
ax3.text(41.2,25,'B',fontsize=10)
ax3.text(36.5,11,'A',fontsize=10)

ax3.set_xlim(25, 50)
ax3.set_ylim(9,31)

ax3.set_yticks([10,12,14,16,18,20,22,24,26,28,30],['10','','','','','20','','','','','30'])

ax3.yaxis.set_label_position("right")
ax3.yaxis.tick_right()
ax3.set_ylabel('Distance (deg)')
ax3.set_xlabel('t-'+'Distance'+str(reduction_v)+' (s)')
# ax3.legend(loc='upper right', bbox_to_anchor=[ax3_pos.x0+ax3_pos.width+0.005, ax3_pos.y0+ax3_pos.height+0.005], bbox_transform=fig.transFigure)
handles = [
    Line2D([0], [0], color=ak135_seis_linecolor, linestyle=ak135_seis_linestyle, linewidth=ak135_seis_linewidth, label='AK135'),
    Line2D([0], [0], color=model_li_seis_linecolor, linestyle=model_li_seis_linestyle, linewidth=model_li_seis_linewidth, dashes=model_li_seis_dashset, label='Li_2013')
]

plt.legend(handles=handles, handlelength=3, handletextpad=1.0, loc='upper right', bbox_to_anchor=[ax3_pos.x0+ax3_pos.width+0.005, ax3_pos.y0+ax3_pos.height+0.005], bbox_transform=fig.transFigure)
############################################

ak135_arri_time_linewidth = 1.5
ak135_arri_time_linealpha = 1
ak135_arri_time_color1 = raypath_linecolor1
ak135_arri_time_color2 = raypath_linecolor2
ak135_arri_time_color3 = raypath_linecolor3

model_li_arri_time_linewidth = 1.5
model_li_arri_time_linetype = model_li_seis_linestyle
model_li_arri_time_dashset = model_li_seis_dashset
model_li_arri_time_alpha = 1
model_li_arri_time_color1 = ak135_arri_time_color1
model_li_arri_time_color2 = ak135_arri_time_color2
model_li_arri_time_color3 = ak135_arri_time_color3

ax4 = fig.add_axes([ax4_pos.x0, ax4_pos.y0, ax4_pos.width, ax4_pos.height])


model = TauPyModel(model='../pic1_tauppath/ak135_interpo.npz',cache=False)

arr_re = 0

arri_time_1 = []
dis_1 = []
for i in range(101):
    arrivals = model.get_travel_times(source_depth_in_km=519, phase_list=['p','P'], distance_in_degree=i/5+10)
    if i/5+10<16.7:
        arri_time_1.append(arrivals[0].time-reduction_v*arrivals[0].distance-arr_re)
        dis_1.append(arrivals[0].distance)
    if i/5+10>16.7 and i/5+10<21.3:
        arri_time_1.append(arrivals[1].time-reduction_v*arrivals[1].distance-arr_re)
        dis_1.append(arrivals[1].distance)

arri_time_3 = []
dis_3 = []
for i in range(101):
    arrivals = model.get_travel_times(source_depth_in_km=519, phase_list=['p','P'], distance_in_degree=i/5+10)
    if i/5+10<16.7 and i/5+10>12.1:
        arri_time_3.append(arrivals[1].time-reduction_v*arrivals[1].distance-arr_re)
        dis_3.append(arrivals[1].distance)
    if i/5+10>16.7:
        arri_time_3.append(arrivals[0].time-reduction_v*arrivals[0].distance-arr_re)
        dis_3.append(arrivals[0].distance)

arri_time_2 = []
dis_2 = []
for i in range(101):
    arrivals = model.get_travel_times(source_depth_in_km=519, phase_list=['p','P'], distance_in_degree=i/5+10)
    if i/5+10<21.3 and i/5+10>12.1:
        arri_time_2.append(arrivals[2].time-reduction_v*arrivals[2].distance-arr_re)
        dis_2.append(arrivals[2].distance)

ax4.plot(arri_time_1, dis_1, color=ak135_arri_time_color1, linewidth=ak135_arri_time_linewidth, alpha=ak135_arri_time_linealpha, zorder=3)
ax4.plot(arri_time_2, dis_2, color=ak135_arri_time_color2, linewidth=ak135_arri_time_linewidth, alpha=ak135_arri_time_linealpha, zorder=2)
ax4.plot(arri_time_3, dis_3, color=ak135_arri_time_color3, linewidth=ak135_arri_time_linewidth, alpha=ak135_arri_time_linealpha, zorder=1)



# model = TauPyModel(model='../pic1_tauppath/model_li_interpo.npz',cache=False)

# reduction_v = 10
# arr_re = 0

# arri_time_1 = []
# dis_1 = []
# for i in range(101):
#     arrivals = model.get_travel_times(source_depth_in_km=519, phase_list=['p','P'], distance_in_degree=i/5+10)
#     if i/5+10<18:
#         arri_time_1.append(arrivals[0].time-reduction_v*arrivals[0].distance-arr_re)
#         dis_1.append(arrivals[0].distance)
#     if i/5+10>18 and i/5+10<25.25:
#         arri_time_1.append(arrivals[1].time-reduction_v*arrivals[1].distance-arr_re)
#         dis_1.append(arrivals[1].distance)

# arri_time_2 = []
# dis_2 = []
# for i in range(101):
#     arrivals = model.get_travel_times(source_depth_in_km=519, phase_list=['p','P'], distance_in_degree=i/5+10)
#     if i/5+10<18 and i/5+10>15.4:
#         arri_time_2.append(arrivals[1].time-reduction_v*arrivals[1].distance-arr_re)
#         dis_2.append(arrivals[1].distance)
#     if i/5+10>18:
#         arri_time_2.append(arrivals[0].time-reduction_v*arrivals[0].distance-arr_re)
#         dis_2.append(arrivals[0].distance)

# arri_time_3 = []
# dis_3 = []
# for i in range(101):
#     arrivals = model.get_travel_times(source_depth_in_km=519, phase_list=['p','P'], distance_in_degree=i/5+10)
#     if i/5+10<25.25 and i/5+10>15.4:
#         arri_time_3.append(arrivals[2].time-reduction_v*arrivals[2].distance-arr_re)
#         dis_3.append(arrivals[2].distance)

# ax4.plot(arri_time_1, dis_1, color=model_li_arri_time_color1, linewidth=model_li_arri_time_linewidth, linestyle=model_li_arri_time_linetype, dashes=model_li_arri_time_dashset, alpha=model_li_arri_time_alpha, zorder=3, label='ak135')
# ax4.plot(arri_time_2, dis_2, color=model_li_arri_time_color2, linewidth=model_li_arri_time_linewidth, linestyle=model_li_arri_time_linetype, dashes=model_li_arri_time_dashset, alpha=model_li_arri_time_alpha, zorder=6)
# ax4.plot(arri_time_3, dis_3, color=model_li_arri_time_color3, linewidth=model_li_arri_time_linewidth, linestyle=model_li_arri_time_linetype, dashes=model_li_arri_time_dashset, alpha=model_li_arri_time_alpha, zorder=4)

# arri_time = []
# dis = []
# for i in range(101):
#     arrivals = model.get_travel_times(source_depth_in_km=519, phase_list=['p','P'], distance_in_degree=i/5+10)
#     for j in range(len(arrivals)):
#         arri_time.append(arrivals[j].time-reduction_v*arrivals[j].distance-arr_re)
#         dis.append(arrivals[j].distance)
# ax3.scatter(arri_time, dis, color=(0/255,194/255,0/255), s=2, alpha=0.7, zorder=3)

ax4.text(arri_time_1[0]+1,dis_1[0],'A')
ax4.text(arri_time_1[-1]+1,dis_1[-1]-0.5,'B')
ax4.text(arri_time_3[0]-3,dis_3[0],'C')
ax4.text(arri_time_3[-1]+1,dis_3[-1]-0.5,'D')

ax4.set_ylabel('Distance (deg)')
ax4.set_xlabel('t-'+str(reduction_v)+'*Distance(s)')
ax4.set_xticks(ticks=[25,35,45],labels=['25','35','45'])
ax4.set_yticks(ticks=[13,20,27],labels=['13','20','27'])
# ax4.legend(loc='upper right')


############################################



subploticonfontsize = 12

add_aligned_text(fig, ax1_pos, '(c)', subploticonfontsize, -0.033, -0.005)
add_aligned_text(fig, ax2_pos, '(b)', subploticonfontsize, -0.033, -0.005)
add_aligned_text(fig, ax3_pos, '(d)', subploticonfontsize, -0.033, -0.005)
add_aligned_text(fig, ax4_pos, '(a)', subploticonfontsize, -0.033, -0.005)

fig.savefig('pic1_v2.2.svg')
# fig.savefig('pic1_v2.2.jpg')





