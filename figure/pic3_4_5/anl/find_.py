

import os


f = open('./corr_anl/corr_all_logs/dl0_4_train0_0.txt','r')
f_c = f.readlines()
f.close()

all_corr_nam = []
all_corr = []

for i in range(len(f_c)-1):
    all_corr_nam.append(f_c[i].replace('\n','').split('---')[0])
    f_c_line_temp = f_c[i].replace('\n','').split('---')[1]
    f_c_line_list_temp = f_c_line_temp.split(',')[:-1]
    all_corr.append(float(f_c_line_list_temp[-1]))


sorted_indices = sorted(range(len(all_corr)), key=lambda i: all_corr[i])[:5]

print("min:")
for i, idx in enumerate(sorted_indices):
    print(f"{i+1}: ={all_corr[idx]}, ={all_corr_nam[idx]}")

#############################


f = open('./mse_anl/val_loss_mse_log/dl0_4_train0_0.dat','r')
f_c = f.readlines()
f.close()

all_mse_nam = []
all_mse = []

for i in range(len(f_c)):
    all_mse_nam.append(os.path.basename(f_c[i].replace('\n','').split('---')[0]))
    f_c_line_temp = f_c[i].replace('\n','').split('---')[xxx].split(':')[-1]
    all_mse.append(float(f_c_line_temp))


sorted_indices = sorted(range(len(all_mse)), key=lambda i: all_mse[i], reverse=True)[:5]

print("max:")
for i, idx in enumerate(sorted_indices):
    print(f"{i+1}: ={all_mse[idx]}, ={all_mse_nam[idx]}")