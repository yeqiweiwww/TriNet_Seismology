



import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd


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

def get_train_loss(file_path, loss_name):

    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if line.split(' ')[0] == 'step':
            step = [int(item) for item in line.split(' ')[1:-1]]
        if line.split(' ')[0] == loss_name:
            loss = [float(item) for item in line.split(' ')[1:-1]]

    return step, loss

def get_train_loss_dic(log_file_path_dic, loss_name):

    step_loss_dic = {'loss_name': loss_name}

    for index_file_path in range(len(log_file_path_dic)):
        out_log_name = os.path.basename(log_file_path_dic[index_file_path]).split('.')[0]
        step, loss = get_train_loss(log_file_path_dic[index_file_path], loss_name)
        loss = exponential_moving_average(loss, weight=0.7)
        step_loss_dic[out_log_name] = {}
        step_loss_dic[out_log_name]['step'] = step
        step_loss_dic[out_log_name]['loss'] = loss

    return step_loss_dic

def exponential_moving_average(loss_values, weight=0.6):
    """
    """

    smoothed_loss = []
    last = loss_values[0]
    smoothed_loss.append(last)

    for value in loss_values[1:]:
        smoothed_val = last * weight + (1 - weight) * value
        smoothed_loss.append(smoothed_val)
        last = smoothed_val
    
    return smoothed_loss

######################################

def get_val_lossandmse(path, lossormse_name):

    f = open(path)
    content = f.readlines()
    f.close()

    nam = []
    for i in range(len(content)):
        temp_list = content[i].replace('\n','').split('---')
        nam.append(temp_list[0])
        

    lossormse = []
    if (lossormse_name == 'loss_vel') or (lossormse_name == 'abs_loss_vel'):
        for i in range(len(content)):
            temp_list = content[i].replace('\n','').split('---')
            for j in range(len(temp_list)-1):
                if temp_list[j+1].split(':')[0].startswith('loss_vel') or temp_list[j+1].split(':')[0].startswith('abs_loss_vel'):
                    lossormse.append(float(temp_list[j+1].split(':')[1]))
    else:
        for i in range(len(content)):
            temp_list = content[i].replace('\n','').split('---')
            for j in range(len(temp_list)-1):
                if temp_list[j+1].split(':')[0] == lossormse_name:
                    lossormse.append(float(temp_list[j+1].split(':')[1]))

    return nam, lossormse

def make_val_loss_mse_vio_dataset(path_dic, lossormse_name):
    dataset = {'loss_name':lossormse_name}

    for i in range(len(path_dic)):
        name = os.path.basename(path_dic[i]).split('.')[0]
        nam, data_list = get_val_lossandmse(path_dic[i],lossormse_name)
        dataset[name]={}
        dataset[name]['nam'] = nam
        dataset[name][lossormse_name] = data_list

    return dataset
######################################

def get_val_corr(path_dic,index_loss=-1):

    corr_list = {'loss_index':index_loss}

    for index_path_dic in range(len(path_dic)):
        path = path_dic[index_path_dic]
        name = os.path.basename(path).split('.')[0]

        corr_list[name] = {}

        f = open(path)
        f_c = f.readlines()
        f.close()

        nam = []
        corr = []

        for i in range(len(f_c)-1):
            temp_list = f_c[i].split('---')
            nam.append(temp_list[0])
            corr.append(float(temp_list[1].split(',')[:-1][index_loss]))

        corr_list[name]['nam'] = nam
        corr_list[name]['corr'] = corr

    return corr_list


######################################

all_train_logs_save_dir_path = '../anl/log_anl/read_all_logs'
all_val_logs_save_dir_path = '../anl/mse_anl/val_loss_mse_log'
all_corr_logs_save_dir_path = '../anl/corr_anl/corr_all_logs'

train_loss_name1 = 'train_loss_all'
train_loss_name2 = 'validate_loss_all'

val_lossormse_name = 'loss_all'
val_corr_index = -1

######################################

file_name = ['dl0_0_train0_0_testset_noise025','dl0_0_train0_0_testset_noise020', 'dl0_0_train0_0', 'dl0_0_train0_0_testset_noise010', 'dl0_0_train0_0_testset_noise005']

draw_val_file_path = [
    all_val_logs_save_dir_path+'/dl0_0_train0_0.dat',
    all_val_logs_save_dir_path+'/dl0_0_train0_0_testset_noise005.dat',
    all_val_logs_save_dir_path+'/dl0_0_train0_0_testset_noise010.dat',
    all_val_logs_save_dir_path+'/dl0_0_train0_0_testset_noise020.dat',
    all_val_logs_save_dir_path+'/dl0_0_train0_0_testset_noise025.dat',
]
draw_val_corr_file_path = [
    all_corr_logs_save_dir_path+'/dl0_0_train0_0.txt',
    all_corr_logs_save_dir_path+'/dl0_0_train0_0_testset_noise005.txt',
    all_corr_logs_save_dir_path+'/dl0_0_train0_0_testset_noise010.txt',
    all_corr_logs_save_dir_path+'/dl0_0_train0_0_testset_noise020.txt',
    all_corr_logs_save_dir_path+'/dl0_0_train0_0_testset_noise025.txt',
]
draw_legend_name = {
    'dl0_0_train0_0':'0.15 (Test Set)',
    'dl0_0_train0_0_testset_noise005':'0.05',
    'dl0_0_train0_0_testset_noise010':'0.10',
    'dl0_0_train0_0_testset_noise020':'0.20',
    'dl0_0_train0_0_testset_noise025':'0.25',
}

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

val_lossormse_dic = make_val_loss_mse_vio_dataset(draw_val_file_path, val_lossormse_name)
val_corr_dic = get_val_corr(draw_val_corr_file_path, index_loss=-1)

val_dataset = []
for i in range(len(file_name)):
    for j in range(len(val_lossormse_dic[file_name[i]][val_lossormse_name])):
        val_dataset.append({'Model':draw_legend_name[file_name[i]],'Value':val_lossormse_dic[file_name[i]][val_lossormse_name][j],'Group':'val_loss'})
    for j in range(len(val_corr_dic[file_name[i]]['corr'])):
        val_dataset.append({'Model':draw_legend_name[file_name[i]],'Value':val_corr_dic[file_name[i]]['corr'][j],'Group':'val_corr'})

df_val_dataset = pd.DataFrame(val_dataset)
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
# fig = plt.figure(figsize=figsize_para)
fig = plt.figure(figsize=figsize_para,dpi=900)

ax3 = fig.add_subplot()

positions = np.arange(len(file_name))
offset=0.2

ax3_dataset = []
for i in range(len(file_name)):
    data = val_lossormse_dic[file_name[i]][val_lossormse_name]
    ax3_dataset.append(data)
    

    median_val = np.median(data)
    std_val = np.std(data)
    q1_val = np.percentile(data, 25)
    q3_val = np.percentile(data, 75)
    

    print(f"{draw_legend_name[file_name[i]]}")
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
for i in range(len(file_name)):
    data = val_corr_dic[file_name[i]]['corr']
    ax4_dataset.append(data)
    

    median_val = np.median(data)
    std_val = np.std(data)
    q1_val = np.percentile(data, 25)
    q3_val = np.percentile(data, 75)
    

    print(f"{draw_legend_name[file_name[i]]}")
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
for i in range(len(file_name)):
    ax3_label.append(draw_legend_name[file_name[i]])

ax3.set_ylim(-0.05, 0.71)
ax3.set_yticks([0.1,0.3,0.5,0.7])
ax3.set_xticks(positions,ax3_label)

ax3.set_ylabel('Loss')
ax3.set_xlabel('Noise Sigma')
ax3.set_title('Test Set Loss and CC Distribution')

split_position = []
for i in range(len(positions)-1):
    split_position.append((positions[i]+positions[i+1])/2)

ax3.vlines(
    split_position,
    ymin=-0.9,
    ymax=1.1,
    linestyles='--',
    color='black',
    linewidth=2,
)


from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=(112/255, 151/255, 248/255), edgecolor='black', label='Loss'),
    Patch(facecolor=(233/255, 64/255, 38/255), edgecolor='black', label='CC')
]
ax3.legend(handles=legend_elements, loc='lower right')

fig.tight_layout()


fig.savefig('pic5_1_v3.2.svg')
# fig.savefig('pic5_1_v3.2.jpg')

