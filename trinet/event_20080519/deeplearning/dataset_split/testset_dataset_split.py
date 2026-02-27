

import os

f = open('./test_techo_file.dat','r')
f_c = f.readlines()
f.close()

t_echo_list = []

for i in range(len(f_c)):
    t_echo_list.append(os.path.basename(f_c[i].replace('\n','').replace('rebuild_vp_seis','').replace('.dat','')))

testset_dir_name = [
    'testset_rebuild_seis_data_noise005',
    'testset_rebuild_seis_data_noise010',
    'testset_rebuild_seis_data_noise020',
    'testset_rebuild_seis_data_noise025',
    'testset_rebuild_seis_data_sta7',
    'testset_rebuild_seis_data_sta15',
    'testset_rebuild_seis_data_sta23',
    'testset_rebuild_seis_data_sta39',
]

testset_techo_dir_path = ''

for i in range(len(testset_dir_name)):
    txt = ''
    for j in range(len(t_echo_list)):
        txt = txt + testset_techo_dir_path + '/' + testset_dir_name[i] + '/seis_rebuild_data/rebuild_vp_seis' + t_echo_list[j] +'.dat\n'

    testset_dataset_name = testset_dir_name[i] + '.dat'

    f = open(testset_dataset_name,'w')
    f.write(txt)
    f.close()