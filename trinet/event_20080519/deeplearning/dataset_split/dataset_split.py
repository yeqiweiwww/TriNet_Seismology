

import os

workspace_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))
workspace_data_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))+'_data'

workspace_data_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))).replace('trinet','data/trinet') + '/' + workspace_data_name

# 设置路径
rebuild_seis_dic_path1 = workspace_data_path + '/data/data0/rebuild_seis_data/seis_rebuild_data'

train_techo_file_path = './train_techo_file.dat'
val_techo_file_path = './val_techo_file.dat'
test_techo_file_path = './test_techo_file.dat'

# 设置列表
rebuild_seis_dir1 = os.listdir(rebuild_seis_dic_path1)
rebuild_seis1 = []
for i in range(len(rebuild_seis_dir1)):
    rebuild_seis1.append(rebuild_seis_dic_path1 + '/' + rebuild_seis_dir1[i])

train_size = 6000
val_size = 600
test_size = 600

train_techo=[]
val_techo=[]
test_techo=[]

for i in range(train_size):
    t_echo = rebuild_seis1[i]
    train_techo.append(t_echo+'\n')
for i in range(train_size,train_size+val_size):
    t_echo = rebuild_seis1[i]
    val_techo.append(t_echo+'\n')
for i in range(train_size+val_size,train_size+val_size+test_size):
    t_echo = rebuild_seis1[i]
    test_techo.append(t_echo+'\n')

print('train_size:',len(train_techo))
print('val_size:',len(val_techo))
print('test_size:',len(test_techo))

f = open(train_techo_file_path,'w')
f.writelines(train_techo)
f.close()

f = open(val_techo_file_path,'w')
f.writelines(val_techo)
f.close()

f = open(test_techo_file_path,'w')
f.writelines(test_techo)
f.close()


