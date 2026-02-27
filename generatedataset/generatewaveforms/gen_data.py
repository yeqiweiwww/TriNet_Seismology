

'''
This file is used to generate velocity structure models and seismic waveform data.
'''

import shutil
import os
import subprocess
import random
import time
import sys
from copy import deepcopy

# from obspy.taup.taup_create import build_taup_model


from gen_modify_vel_base import *
from gen_modify_input import *
from gen_util import *
from gen_ini_para import *

#-----------------------main proess------------------------
# set para
pro_time_start=time.time()

sysargv1 = sys.argv[1]
t = server_name + sysargv1 + '_'

logger_name = deepcopy(paths_info_dic['log_dic']['log_file_path_dir']) + '/log' + server_name + sysargv1 + '.dat'

logger = open(logger_name,'a')
logger.write(t+'\n')
logger.close()


qseis_path = paths_info_dic['gen_data_dic']['qseis_path']

for i in range(echo):

    echo_time_start=time.time()

    spe_sta_loc = []
    for j in range(41):
        spe_sta_loc.append(j*0.5+9.5+random.random()*0.5)

    input_info_dic['RECEIVER_PARAMETERS']['list_of_distances'] = deepcopy(spe_sta_loc)
    input_info_dic['RECEIVER_PARAMETERS']['no_distances'] = deepcopy(int(len(spe_sta_loc)))

    azimuth = []
    for j in range(41):
        azimuth.append(random.uniform(azi1,azi2))

    input_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['list_of_the_azimuth_angles'] = deepcopy(azimuth)
    if len(azimuth) > 1 :
        input_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['switch_for_azimuth_distribution'] = deepcopy(int(1))
    else:
        input_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['switch_for_azimuth_distribution'] = deepcopy(int(0))


    logger = open(logger_name,'a')
    logger.write(t+str(i)+' begin time:'+str(time.strftime('%m-%d-%H:%M:%S', time.localtime()))+'\n')
    logger.close()

    paths_info_dic['modify_dic']['modify_inputfile_path'] = deepcopy(paths_info_dic['modify_dic']['modify_inputfile_path_dir']) + '/modify_inputfile' + t + str(i) + '.inp'
    paths_info_dic['modify_dic']['modify_velocity_model_path'] = deepcopy(paths_info_dic['modify_dic']['modify_velocity_model_path_dir']) + '/modify_model' + t + str(i) + '.dat'
    # paths_info_dic['modify_dic']['modify_nd_file_path'] = deepcopy(paths_info_dic['modify_dic']['modify_nd_file_path_dir']) + '/modify_nd_file' + t + str(i) + '.nd'

    output_names_of_types = []
    for j in range(len(input_info_dic['OUTPUT_FILES_FOR_GREENS_FUNCTIONS']['names_of_types_base'])):
        output_names_of_types.append(deepcopy(input_info_dic['OUTPUT_FILES_FOR_GREENS_FUNCTIONS']['names_of_types_base'][j]) + t + str(i))
    input_info_dic['OUTPUT_FILES_FOR_GREENS_FUNCTIONS']['names_of_types'] = deepcopy(output_names_of_types)

    input_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['seis_name'] = deepcopy(input_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['seis_name_base']) + t + str(i)

    seis_file_name = input_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['seis_name']


    # 修改模型
    mvbm = modify_vel_base_model(vel_model_info_dic, paths_info_dic)
    mvbm.read_vel_base()
    mvbm.interpolation_model()
    mvbm.modify_layer_depth()
    mvbm.modify_velocity()
    mvbm.write_modify_velocity_model()
    # mvbm.generate_nd_file()

    # build_taup_model(filename = paths_info_dic['modify_dic']['modify_nd_file_path'], output_folder= paths_info_dic['modify_dic']['modify_npz_file_path_dir'])

    # 修改输入文件
    m_i = modify_inputfile(input_info_dic, paths_info_dic)
    modify_velocity_model_dic = m_i.get_modify_vel_mod()
    inputfile_content = m_i.generate_inp_content()
    m_i.write_modify_inputfile()

    # 运行qseis06
    qseis_time_start=time.time()
    run_qseis_log, run_qseis_err = subprocess.Popen(
        qseis_path,
        stdin=subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT
    ).communicate(
        input=paths_info_dic['modify_dic']['modify_inputfile_path'].encode(encoding="utf-8")
    )

    logfile_name = deepcopy(paths_info_dic['log_dic']['log_path_dir']) + '/log' + t + str(i) + '.log'
    logfile = open(logfile_name, 'w')
    logfile.write('run_qseis_log\n')
    if not run_qseis_log == None:
        logfile.write(run_qseis_log.decode(encoding="utf-8"))
    logfile.write('\n\n\n')
    logfile.write('run_qseis_err\n')
    if not run_qseis_err == None:
        logfile.write(run_qseis_err.decode(encoding="utf-8"))
    else:
        logfile.write('None')
    logfile.close()

    qseis_time_end=time.time()
    
    # print('qseis06_echo time' + str(i) + ':', (qseis_time_end-qseis_time_start)/60, 'min')

    shutil.move('./'+seis_file_name+'.tt', paths_info_dic['modify_dic']['modify_ttfile']+'/'+seis_file_name+'.tt')
    shutil.move('./'+seis_file_name+'.tz', paths_info_dic['modify_dic']['modify_tzfile']+'/'+seis_file_name+'.tz')
    shutil.move('./'+seis_file_name+'.tr', paths_info_dic['modify_dic']['modify_trfile']+'/'+seis_file_name+'.tr')

    move_file(paths_info_dic['gen_data_dic']['temp_file'], [t+str(i)+'.tt', t+str(i)+'.tr', t+str(i)+'.tv', t+str(i)+'.tz'], paths_info_dic['modify_dic']['modify_otherdata'])
    
    echo_time_end=time.time()

    
    # if i + 1 % 5 == 0:
    #     sleep_time = int(random.random()*10)*3
    #     # print('sleep',str(sleep_time))
    #     for j in range(sleep_time, 0, -1):
    #         # print("\r", "倒计时{}秒！".format(j), end="", flush=True)
    #         time.sleep(1)
    
    logger = open(logger_name,'a')
    logger.write(t+str(i)+' use time:'+str((echo_time_end-echo_time_start)/60)+'min'+'\n')
    logger.write(t+str(i)+' end time:'+str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))+'\n')
    # subprocess.call(['echo', t+str(i)+' use time:'+str((echo_time_end-echo_time_start)/60)+'min'])
    # subprocess.call(['echo', t+str(i)+' end time:'+str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))])
    logger.close()

pro_time_end=time.time()

logger = open(logger_name,'a')
logger.write(t+':'+str((pro_time_end-pro_time_start)/60/60)+'h'+'\n')
logger.write(t+'done\n')
logger.close()

f = open('./logging.dat','a')
f.write(t+'done\n')
f.close()


