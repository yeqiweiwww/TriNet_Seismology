

import os
from copy import deepcopy

def read_techo_path_data(path):
    f = open(path,'r')
    f_c = f.readlines()
    f.close()

    t_echo_path_list = []

    for i in range(len(f_c)):
        t_echo_path_list.append(f_c[i])
    
    return t_echo_path_list

def techo_path_add(all_techo_path, ref_techo_path_train, ref_techo_path_val, ref_techo_path_test, new_num_train, new_num_val, new_num_test):

    if (new_num_train <= len(ref_techo_path_train)) or (new_num_val <= len(ref_techo_path_val)) or (new_num_test <= len(ref_techo_path_test)):
        raise ValueError(f"!")
    if new_num_train+new_num_val+new_num_test > len(all_techo_path):
        raise ValueError(f"!")

    add_techo_path_list = []
    for i in range(len(all_techo_path)):
        if (all_techo_path[i] not in ref_techo_path_train) and (all_techo_path[i] not in ref_techo_path_val) and (all_techo_path[i] not in ref_techo_path_test) :
            add_techo_path_list.append(all_techo_path[i])

    add_num_train = new_num_train - len(ref_techo_path_train)
    add_num_val = new_num_val - len(ref_techo_path_val)
    add_num_test = new_num_test - len(ref_techo_path_test)

    add_list_train = deepcopy(ref_techo_path_train)
    add_list_val = deepcopy(ref_techo_path_val)
    add_list_test = deepcopy(ref_techo_path_test)
    for i in range(add_num_train):
        add_list_train.append(add_techo_path_list[i])
    for i in range(add_num_train,add_num_train+add_num_val):
        add_list_val.append(add_techo_path_list[i])
    for i in range(add_num_train+add_num_val,add_num_train+add_num_val+add_num_test):
        add_list_test.append(add_techo_path_list[i])

    return add_list_train, add_list_val, add_list_test

def techo_path_remove(ref_techo_path_train, ref_techo_path_val, ref_techo_path_test, new_num_train, new_num_val, new_num_test):

    if (new_num_train >= len(ref_techo_path_train)) or (new_num_val >= len(ref_techo_path_val)) or (new_num_test >= len(ref_techo_path_test)):
        raise ValueError(f"!")

    remove_list_train = []
    remove_list_val = []
    remove_list_test = []

    for i in range(new_num_train):
        remove_list_train.append(ref_techo_path_train[i])
    for i in range(new_num_val):
        remove_list_val.append(ref_techo_path_val[i])
    for i in range(new_num_test):
        remove_list_test.append(ref_techo_path_test[i])

    return remove_list_train, remove_list_val, remove_list_test

def techo_path_mid(ref_techo_path_train_less, ref_techo_path_val_less, ref_techo_path_test_less, ref_techo_path_train_more, ref_techo_path_val_more, ref_techo_path_test_more, new_num_train, new_num_val, new_num_test):
    if (new_num_train <= len(ref_techo_path_train_less)) or (new_num_val <= len(ref_techo_path_val_less)) or (new_num_test <= len(ref_techo_path_test_less)):
        raise ValueError(f"!")
    if (new_num_train >= len(ref_techo_path_train_more)) or (new_num_val >= len(ref_techo_path_val_more)) or (new_num_test >= len(ref_techo_path_test_more)):
        raise ValueError(f"!")

    mid_techo_path_list_train = []
    for i in range(len(ref_techo_path_train_more)):
        if ref_techo_path_train_more[i] not in ref_techo_path_train_less:
            mid_techo_path_list_train.append(ref_techo_path_train_more[i])
    mid_techo_path_list_val = []
    for i in range(len(ref_techo_path_val_more)):
        if ref_techo_path_val_more[i] not in ref_techo_path_val_less:
            mid_techo_path_list_val.append(ref_techo_path_val_more[i])
    mid_techo_path_list_test = []
    for i in range(len(ref_techo_path_test_more)):
        if ref_techo_path_test_more[i] not in ref_techo_path_test_less:
            mid_techo_path_list_test.append(ref_techo_path_test_more[i])

    mid_num_train = new_num_train - len(ref_techo_path_train_less)
    mid_num_val = new_num_val - len(ref_techo_path_val_less)
    mid_num_test = new_num_test - len(ref_techo_path_test_less)

    mid_list_train = deepcopy(ref_techo_path_train_less)
    mid_list_val = deepcopy(ref_techo_path_val_less)
    mid_list_test = deepcopy(ref_techo_path_test_less)
    for i in range(mid_num_train):
        mid_list_train.append(mid_techo_path_list_train[i])
    for i in range(mid_num_val):
        mid_list_val.append(mid_techo_path_list_val[i])
    for i in range(mid_num_test):
        mid_list_test.append(mid_techo_path_list_test[i])

    return mid_list_train, mid_list_val, mid_list_test

def write_dataset_file(path, dataset):
    f = open(path,'w')
    f.writelines(dataset)
    f.close()

#######################################
#######################################
#######################################
# set para
workspace_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))
workspace_data_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))+'_data'

workspace_data_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))).replace('trinet','data/trinet') + '/' + workspace_data_name

# 设置路径
rebuild_seis_dic_path1 = workspace_data_path + '/data/data0/rebuild_seis_data/seis_rebuild_data'

# 设置列表
rebuild_seis_dir1 = os.listdir(rebuild_seis_dic_path1)
rebuild_seis1_path_list = []
for i in range(len(rebuild_seis_dir1)):
    rebuild_seis1_path_list.append(rebuild_seis_dic_path1 + '/' + rebuild_seis_dir1[i]+'\n')


#######################################
# 需要修改的部分
# 数量
train_size = 3000
val_size = 300
test_size = 300

dataset_update_type = 'remove' # add/remove/mid

if dataset_update_type == 'add':
    dataset_ref_dir_path = ['']
if dataset_update_type == 'remove':
    dataset_ref_dir_path = ['']
if dataset_update_type == 'mid': # less/more
    dataset_ref_dir_path = ['','']

train_techo_file_path = './train_techo_file.dat'
val_techo_file_path = './val_techo_file.dat'
test_techo_file_path = './test_techo_file.dat'

#######################################
#######################################
#######################################
# main

if dataset_update_type == 'add':

    ref_dataset_train_path_list = read_techo_path_data(dataset_ref_dir_path[0]+'/train_techo_file.dat')
    ref_dataset_val_path_list = read_techo_path_data(dataset_ref_dir_path[0]+'/val_techo_file.dat')
    ref_dataset_test_path_list = read_techo_path_data(dataset_ref_dir_path[0]+'/test_techo_file.dat')

    add_list_train, add_list_val, add_list_test = techo_path_add(rebuild_seis1_path_list, ref_dataset_train_path_list, ref_dataset_val_path_list, ref_dataset_test_path_list, train_size, val_size, test_size)

    for i in range(len(add_list_train)):
        if add_list_train[i] in add_list_val:
            raise ValueError(f"!")
        if add_list_train[i] in add_list_test:
            raise ValueError(f"!")
    for i in range(len(add_list_val)):
        if add_list_val[i] in add_list_test:
            raise ValueError(f"!")
    print('add_list_train',len(add_list_train))
    print('add_list_train set',len(list(set(add_list_train))))
    print('add_list_val',len(add_list_val))
    print('add_list_val set',len(list(set(add_list_val))))
    print('add_list_test',len(add_list_test))
    print('add_list_test set',len(list(set(add_list_test))))

    write_dataset_file(train_techo_file_path, add_list_train)
    write_dataset_file(val_techo_file_path, add_list_val)
    write_dataset_file(test_techo_file_path, add_list_test)

if dataset_update_type == 'remove':
    ref_dataset_train_path_list = read_techo_path_data(dataset_ref_dir_path[0]+'/train_techo_file.dat')
    ref_dataset_val_path_list = read_techo_path_data(dataset_ref_dir_path[0]+'/val_techo_file.dat')
    ref_dataset_test_path_list = read_techo_path_data(dataset_ref_dir_path[0]+'/test_techo_file.dat')

    remove_list_train, remove_list_val, remove_list_test = techo_path_remove(ref_dataset_train_path_list, ref_dataset_val_path_list, ref_dataset_test_path_list, train_size, val_size, test_size)

    for i in range(len(remove_list_train)):
        if remove_list_train[i] in remove_list_val:
            raise ValueError(f"!")
        if remove_list_train[i] in remove_list_test:
            raise ValueError(f"!")
    for i in range(len(remove_list_val)):
        if remove_list_val[i] in remove_list_test:
            raise ValueError(f"!")
    print('remove_list_train',len(remove_list_train))
    print('remove_list_train set',len(list(set(remove_list_train))))
    print('remove_list_val',len(remove_list_val))
    print('remove_list_val set',len(list(set(remove_list_val))))
    print('remove_list_test',len(remove_list_test))
    print('remove_list_test set',len(list(set(remove_list_test))))

    write_dataset_file(train_techo_file_path, remove_list_train)
    write_dataset_file(val_techo_file_path, remove_list_val)
    write_dataset_file(test_techo_file_path, remove_list_test)

if dataset_update_type == 'mid':
    ref_dataset_train_path_list_less = read_techo_path_data(dataset_ref_dir_path[0]+'/train_techo_file.dat')
    ref_dataset_val_path_list_less = read_techo_path_data(dataset_ref_dir_path[0]+'/val_techo_file.dat')
    ref_dataset_test_path_list_less = read_techo_path_data(dataset_ref_dir_path[0]+'/test_techo_file.dat')
    ref_dataset_train_path_list_more = read_techo_path_data(dataset_ref_dir_path[1]+'/train_techo_file.dat')
    ref_dataset_val_path_list_more = read_techo_path_data(dataset_ref_dir_path[1]+'/val_techo_file.dat')
    ref_dataset_test_path_list_more = read_techo_path_data(dataset_ref_dir_path[1]+'/test_techo_file.dat')


    mid_list_train, mid_list_val, mid_list_test = techo_path_mid(ref_dataset_train_path_list_less, ref_dataset_val_path_list_less, ref_dataset_test_path_list_less, ref_dataset_train_path_list_more, ref_dataset_val_path_list_more, ref_dataset_test_path_list_more, train_size, val_size, test_size)

    for i in range(len(mid_list_train)):
        if mid_list_train[i] in mid_list_val:
            raise ValueError(f"!")
        if mid_list_train[i] in mid_list_test:
            raise ValueError(f"!")
    for i in range(len(mid_list_val)):
        if mid_list_val[i] in mid_list_test:
            raise ValueError(f"!")
    print('mid_list_train',len(mid_list_train))
    print('mid_list_train set',len(list(set(mid_list_train))))
    print('mid_list_val',len(mid_list_val))
    print('mid_list_val set',len(list(set(mid_list_val))))
    print('mid_list_test',len(mid_list_test))
    print('mid_list_test set',len(list(set(mid_list_test))))

    write_dataset_file(train_techo_file_path, mid_list_train)
    write_dataset_file(val_techo_file_path, mid_list_val)
    write_dataset_file(test_techo_file_path, mid_list_test)
