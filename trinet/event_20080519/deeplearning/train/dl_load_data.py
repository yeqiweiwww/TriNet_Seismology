

'''

'''

import os
import numpy as np

from random import shuffle
from copy import deepcopy
from pandas.core.frame import DataFrame

import torch
import torchvision
from torch.utils.data import Dataset, DataLoader

from dl_utils import model_data_process, get_rebuild_data, gen_sta_dis_matrix



class load_mydataset(Dataset):
    def __init__(self, techo_file_path):


        text_temp = open(techo_file_path)
        files_path = text_temp.readlines()
        text_temp.close()
        
        self.files_path=[]
        for i in range(len(files_path)):
            self.files_path.append(files_path[i].replace('\n',''))

        self.seis_files = deepcopy(self.files_path)



    

    def __len__(self):
        return len(self.seis_files)
    

    def __getitem__(self, index):
        
        files_path = deepcopy(self.seis_files[index])
        techo = os.path.basename(files_path).replace('rebuild_vp_seis', '').replace('.dat', '')
        files_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(files_path)))
        input_rebuild_seis_file_path = deepcopy(files_path)

        mdp = model_data_process()
        self.modify_model_dic = mdp.read_modeldata(files_dir_path+'/modified_modelfile/modify_model'+techo+'.dat')

        pro_time, pro_vp_data, sta_location, use_index = get_rebuild_data(input_rebuild_seis_file_path)
        input_rebuild_seis_data = np.array(deepcopy(pro_vp_data), dtype=np.float64)


        rebuild_sta_location = gen_sta_dis_matrix(sta_location=sta_location, pro_vp_data=pro_vp_data, arr_type='relative')
        
        sta_loc_ten = deepcopy(rebuild_sta_location)
        sta_loc_ten = np.array(sta_loc_ten, dtype=np.float64)


        input_rebuild_seis_data = [sta_loc_ten,input_rebuild_seis_data]
        input_rebuild_seis_data = torch.FloatTensor(np.array(input_rebuild_seis_data, dtype=np.float64))


        vp = mdp.make_label()
        
        change_660 = mdp.get_change_660()

        thickness = mdp.get_change_thickness()

        label = deepcopy(vp)
        label.extend(change_660)
        label.extend(thickness)
        label = torch.FloatTensor(np.array(label, dtype=np.float64))

        return (input_rebuild_seis_data, label)#返回成对的数据

    def get_info(self):

        files_path = deepcopy(self.seis_files[0])
        techo = os.path.basename(files_path).replace('rebuild_vp_seis', '').replace('.dat', '')
        files_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(files_path)))
        input_rebuild_seis_file_path = deepcopy(files_path)

        mdp = model_data_process()
        self.modify_model_dic = mdp.read_modeldata(files_dir_path+'/modified_modelfile/modify_model'+techo+'.dat')

        pro_time, pro_vp_data, sta_location, use_index = get_rebuild_data(input_rebuild_seis_file_path)
        input_rebuild_seis_data = np.array(deepcopy(pro_vp_data), dtype=np.float64)


        rebuild_sta_location = gen_sta_dis_matrix(sta_location=sta_location, pro_vp_data=pro_vp_data, arr_type='relative')
        
        sta_loc_ten = deepcopy(rebuild_sta_location)
        sta_loc_ten = np.array(sta_loc_ten, dtype=np.float64)


        input_rebuild_seis_data = [sta_loc_ten,input_rebuild_seis_data]
        input_rebuild_seis_data = torch.FloatTensor(np.array(input_rebuild_seis_data, dtype=np.float64))


        vp = mdp.make_label()
        
        change_660 = mdp.get_change_660()

        thickness = mdp.get_change_thickness()

        label = deepcopy(vp)
        label.extend(change_660)
        label.extend(thickness)
        label = torch.FloatTensor(np.array(label, dtype=np.float64))

        label_each_len = [len(vp), len(change_660), len(thickness)]

        return (input_rebuild_seis_data, label, label_each_len)

if __name__ == '__main__':

    load_dataset_train = load_mydataset('../data/train_techo_file.dat')

    print(load_dataset_train.get_info()[0].shape)

