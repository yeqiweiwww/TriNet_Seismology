



import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd

from copy import deepcopy


######################################
def mkdir(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

def add_aligned_text(fig, ax_pos, text, fontsize, x_plus=0, y_plus=0):

    fig.text(
        ax_pos.x0 + x_plus,
        ax_pos.y1 + y_plus,
        text,
        fontsize=fontsize,
        ha='left',
        va='top'
    )

######################################

def get_val_lossandmse_sta_dis(path, lossormse_name):

    f = open(path)
    content = f.readlines()
    f.close()

    nam = []
    for i in range(len(content)):
        temp_list = content[i].replace('\n','').split('---')
        nam.append(temp_list[0][:-8])

    nam = list(set(nam))

    lossormse = {}
    for indx_nam in range(len(nam)):
        lossormse[nam[indx_nam]]=[]
        for indx_content in range(len(content)):
            temp_list = content[indx_content].replace('\n','').split('---')
            if temp_list[0][:-8] == nam[indx_nam]:
                for indx_temp in range(len(temp_list)-1):
                    if (lossormse_name == 'loss_vel') or (lossormse_name == 'abs_loss_vel'):
                        if temp_list[indx_temp+1].split(':')[0].startswith('loss_vel') or temp_list[indx_temp+1].split(':')[0].startswith('abs_loss_vel'):
                            lossormse[nam[indx_nam]].append(float(temp_list[indx_temp+1].split(':')[1]))
                    else:
                        if temp_list[indx_temp+1].split(':')[0] == lossormse_name:
                            lossormse[nam[indx_nam]].append(float(temp_list[indx_temp+1].split(':')[1]))

    return nam, lossormse

######################################

def get_val_corr_sta_dis(path,index_loss=-1):


    f = open(path)
    f_c = f.readlines()
    f.close()

    nam = []
    for i in range(len(f_c)-1):
        temp_list = f_c[i].replace('\n','').split('---')
        nam.append(temp_list[0][:-8])

    nam = list(set(nam))

    corr_list = {}
    for indx_nam in range(len(nam)):
        corr_list[nam[indx_nam]] = []
        for i in range(len(f_c)-1):
            temp_list = f_c[i].replace('\n','').split('---')
            if temp_list[0][:-8] == nam[indx_nam]:
                corr_list[nam[indx_nam]].append(float(temp_list[1].split(',')[:-1][index_loss]))

    return nam, corr_list


######################################


val_sta_dis_path = '../anl/mse_anl/val_loss_mse_log/dl0_0_train0_0_testset_sta_dis.dat'
corr_sta_dis_path = '../anl/corr_anl/corr_all_logs/dl0_0_train0_0_testset_sta_dis.txt'

val_lossormse_name = 'loss_all'
val_corr_index = -1

nam = ['pre_model_seis2_20250809163912_847','pre_model_seis1_20250809165445_132','pre_model_seis1_20250809165436_533','pre_model_seis2_20250809163930_357','pre_model_seis2_20250809163921_336','pre_model_seis2_20250809163918_136','pre_model_seis1_20250809165433_550','pre_model_seis1_20250809165445_638','pre_model_seis2_20250809163915_533','pre_model_seis1_20250809165454_262']

######################################


######################################

fm_para = {
    'font.family': 'Times New Roman',
    'font.size': 8,
    'axes.titlesize': 8,
    'axes.labelsize': 8,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    }
draw_para = {
    'figsize_para': (7.5, 3.5),
    'linewidth_para': 1,
}

######################################

val_lossandmse_nam, val_lossormse_dic = get_val_lossandmse_sta_dis(val_sta_dis_path, val_lossormse_name)
val_corr_nam, val_corr_dic = get_val_corr_sta_dis(corr_sta_dis_path, index_loss=-1)

######################################


font_path = '../../fonts/timesnewroman/times.ttf'
fm.fontManager.addfont(font_path)


plt.rcParams['font.family'] = fm_para['font.family']


plt.rcParams['font.size'] = fm_para['font.size']
plt.rcParams['axes.titlesize'] = fm_para['axes.titlesize']
plt.rcParams['axes.labelsize'] = fm_para['axes.labelsize']
plt.rcParams['xtick.labelsize'] = fm_para['xtick.labelsize']
plt.rcParams['ytick.labelsize'] = fm_para['ytick.labelsize']
plt.rcParams['legend.fontsize'] = fm_para['legend.fontsize']
plt.rcParams['legend.fontsize'] = fm_para['legend.fontsize']

plt.rcParams['svg.fonttype'] = 'none'



figsize_para=draw_para['figsize_para']
linewidth_para=draw_para['linewidth_para']

############################################

nam_num = 5
# fig = plt.figure(figsize=figsize_para)
fig = plt.figure(figsize=figsize_para,dpi=900)

ax3 = fig.add_subplot()

positions = np.arange(nam_num)
offset=0.2

ax3_dataset = []
for i in range(nam_num):
    data = val_lossormse_dic[nam[i]]
    ax3_dataset.append(data)
    

    median_val = np.median(data)
    std_val = np.std(data)
    q1_val = np.percentile(data, 25)
    q3_val = np.percentile(data, 75)
    

    print(f"{nam[i]}")
    print(f" (Median): {median_val:.4f}")
    print(f" (Std): {std_val:.4f}")
    print(f"Q1: {q1_val:.4f}")
    print(f"Q3: {q3_val:.4f}")
    print(f"IQR: {q3_val-q1_val:.4f}")
    print("-" * 40)

bplot = ax3.boxplot(
    x=ax3_dataset,
    notch=False,
    vert=True,
    whis=1.5,
    positions=positions-offset,
    widths=0.3,
    patch_artist=True,
    meanline=False,
    showmeans=False,
    showcaps=True,
    showbox=True,
    showfliers=False,
    boxprops = {'edgecolor':'black','facecolor':(112/255, 151/255, 248/255),'linewidth':1,'alpha':1}, 
    flierprops = {'marker':'o','markerfacecolor':'red','markeredgecolor':'black'},
    medianprops = {'linestyle':'-','color':'black'},
    meanprops = {'marker':'D','markerfacecolor':'indianred'},
    capprops={'linestyle':'-','linewidth':1,'color':'black'},
    whiskerprops={'linestyle':'-','linewidth':1,'color':'black'},
)


# parts = ax3.violinplot(
#     ax3_dataset,
#     positions=positions-offset,
#     widths=0.4,
#     showextrema=True,
#     showmedians=True,
#     showmeans=False,
#     )

# for pc in parts['bodies']:
#     pc.set_facecolor((112/255, 151/255, 248/255))
#     pc.set_edgecolor('black')
#     pc.set_linewidth(1)
#     pc.set_alpha(1)

# parts['cmaxes'].set_color('black')
# parts['cmins'].set_color('black')
# parts['cbars'].set_color('black')
# # parts['cbars'].set_color(['black','blue','red','green','yellow','purple','orange'])
# parts['cmedians'].set_color('black')


ax4 = ax3.twinx()

ax4_dataset = []
for i in range(nam_num):
    data = val_corr_dic[nam[i]]
    ax4_dataset.append(data)
    

    median_val = np.median(data)
    std_val = np.std(data)
    q1_val = np.percentile(data, 25)
    q3_val = np.percentile(data, 75)
    

    print(f"{nam[i]}")
    print(f" (Median): {median_val:.4f}")
    print(f" (Std): {std_val:.4f}")
    print(f"Q1: {q1_val:.4f}")
    print(f"Q3: {q3_val:.4f}")
    print(f"IQR: {q3_val-q1_val:.4f}")
    print("-" * 40)

bplot = ax4.boxplot(
    x=ax4_dataset,
    notch=False,
    vert=True,
    whis=1.5,
    positions=positions+offset,
    widths=0.3,
    patch_artist=True,
    meanline=False,
    showmeans=False,
    showcaps=True,
    showbox=True,
    showfliers=False,
    boxprops = {'edgecolor':'black','facecolor':(233/255, 64/255, 38/255),'linewidth':1,'alpha':1}, 
    flierprops = {'marker':'o','markerfacecolor':'red','markeredgecolor':'black'},
    medianprops = {'linestyle':'-','color':'black'},
    meanprops = {'marker':'D','markerfacecolor':'indianred'},
    capprops={'linestyle':'-','linewidth':1,'color':'black'},
    whiskerprops={'linestyle':'-','linewidth':1,'color':'black'},
)

# parts = ax4.violinplot(
#     ax4_dataset,
#     positions=positions+offset,
#     widths=0.4,
#     showextrema=True,
#     showmedians=True,
#     showmeans=False,
#     )

# for pc in parts['bodies']:
#     pc.set_facecolor((233/255, 64/255, 38/255))
#     pc.set_edgecolor('black')
#     pc.set_linewidth(1)
#     pc.set_alpha(1)

# parts['cmaxes'].set_color('black')
# parts['cmins'].set_color('black')
# parts['cbars'].set_color('black')
# # parts['cbars'].set_color(['black','blue','red','green','yellow','purple','orange'])
# parts['cmedians'].set_color('black')

ax4.set_ylabel('CC')
ax4.set_ylim(0.58, 1.01)
ax4.set_yticks([0.6, 0.7, 0.8, 0.9, 1.0])

# ax3.set_xlim(positions[0]-0.6,positions[-1]+1.2)
ax3_label = []
for i in range(nam_num):
    ax3_label.append(str(i+1))

ax3.set_ylim(0, 0.78)
ax3.set_yticks([0.1,0.3,0.5,0.7])
ax3.set_xticks(positions,ax3_label)

ax3.set_ylabel('Loss')
ax3.set_xlabel('Random Samples of Test Set')
ax3.set_title('Test Set Loss and CC Distribution')

split_position = []
for i in range(len(positions)-1):
    split_position.append((positions[i]+positions[i+1])/2)

ax3.vlines(
    split_position,
    ymin=0.0,
    ymax=1.0,
    linestyles='--',
    color='black',
    linewidth=1,
)



from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=(112/255, 151/255, 248/255), edgecolor='black', label='Loss'),
    Patch(facecolor=(233/255, 64/255, 38/255), edgecolor='black', label='CC')
]
ax3.legend(handles=legend_elements, loc='lower right')

fig.tight_layout()


fig.savefig('pic5_3.svg')
# fig.savefig('pic9.jpg')

