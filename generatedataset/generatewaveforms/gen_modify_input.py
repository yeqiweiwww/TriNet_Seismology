
'''
This file is used to modify the input files so that they conform to the requirements of this study.
'''

import random
from copy import deepcopy
from pandas import DataFrame
import numpy as np

from gen_util import *

class modify_inputfile():
    def __init__(self, inputfile_info_dic, path_info_dic):
        self.inputfile_info_dic = inputfile_info_dic
        self.path_info_dic = path_info_dic


    def get_modify_vel_mod(
            self, 
            vel_model_path = None,
            inp_depth_used = None,
    ):
        '''
        '''

        # 获取参数
        if vel_model_path == None:
            vel_model_path = deepcopy(self.path_info_dic['modify_dic']['modify_velocity_model_path'])
        else:
            vel_model_path = vel_model_path
        if inp_depth_used == None:
            inp_depth_used = deepcopy(self.inputfile_info_dic['LAYERED_EARTH_MODEL_1']['inp_depth_of_used_model_layer'])
        else:
            inp_depth_used = inp_depth_used

        # 获取速度结构
        modify_velocity_model_dic = get_modify_model_data(vel_model_path)
        depth_modify_velocity_model = modify_velocity_model_dic['depth']
        number_of_used_model_layer = next((i for i, x in enumerate(depth_modify_velocity_model) if x>inp_depth_used), None)-2

        self.inputfile_info_dic['LAYERED_EARTH_MODEL_1']['no_model_lines'] = int(number_of_used_model_layer)

        modify_velocity_model_dic['no'] = modify_velocity_model_dic['no'][:number_of_used_model_layer]
        modify_velocity_model_dic['depth'] = modify_velocity_model_dic['depth'][:number_of_used_model_layer]
        modify_velocity_model_dic['vp'] = modify_velocity_model_dic['vp'][:number_of_used_model_layer]
        modify_velocity_model_dic['vs'] = modify_velocity_model_dic['vs'][:number_of_used_model_layer]
        modify_velocity_model_dic['ro'] = modify_velocity_model_dic['ro'][:number_of_used_model_layer]
        modify_velocity_model_dic['qp'] = modify_velocity_model_dic['qp'][:number_of_used_model_layer]
        modify_velocity_model_dic['qs'] = modify_velocity_model_dic['qs'][:number_of_used_model_layer]
        
        self.modify_velocity_model_dic = modify_velocity_model_dic

        return self.modify_velocity_model_dic


    def generate_inp_content(
            self,
            vel_mod_dic = None,
            inp_info_dic = None,
    ):
        
        '''
        '''

        # 获取参数
        if vel_mod_dic == None:
            vel_mod_dic = deepcopy(self.modify_velocity_model_dic)
        else:
            vel_mod_dic = vel_mod_dic
        if inp_info_dic == None:
            inp_info_dic = deepcopy(self.inputfile_info_dic)
        else:
            inp_info_dic = inp_info_dic

        # 生成输入文件内容
        inp_content = ''

        # begin
        inp_content = inp_content + '#---------------------------------begin of all inputs--------------------------\n'
        inp_content = inp_content + '#---------------------------------------qseis06--------------------------------\n'

        # SOURCE PARAMETERS
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# SOURCE PARAMETERS\n# =================\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['SOURCE_PARAMETERS']['source_depth']) + '     |dble: source_depth;\n'
        inp_content = inp_content + '#------------------------------------------------------------------------------\n'

        # RECEIVER PARAMETERS
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# RECEIVER PARAMETERS\n# =================\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['RECEIVER_PARAMETERS']['receiver_depth']) + '     |dble: receiver_depth;\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['RECEIVER_PARAMETERS']['sw_equidistant']) + '   ' + str(inp_info_dic['RECEIVER_PARAMETERS']['sw_d_unit']) + '     |dble: receiver_distance;\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['RECEIVER_PARAMETERS']['no_distances']) + '     |int: no_distances;\n'
        txt = ''
        for i in range(len(inp_info_dic['RECEIVER_PARAMETERS']['list_of_distances'])):
            txt = txt + str(inp_info_dic['RECEIVER_PARAMETERS']['list_of_distances'][i]) + ' '
        inp_content = inp_content + ' ' + txt + '     |dble: d_1,d_n; or d_1,d_2, ...(no comments in between!);\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['RECEIVER_PARAMETERS']['t_start']) + '   ' + str(inp_info_dic['RECEIVER_PARAMETERS']['t_window']) + '   ' + str(inp_info_dic['RECEIVER_PARAMETERS']['no_t_samples']) + '     |dble: t_start,t_window; int: no_t_samples;\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['RECEIVER_PARAMETERS']['sw_t_reduce']) + '   ' + str(inp_info_dic['RECEIVER_PARAMETERS']['t_reduce']) + '     |int: sw_t_reduce; dble: t_reduce;\n'
        inp_content = inp_content + '#------------------------------------------------------------------------------\n'

        # WAVENUMBER INTEGRATION PARAMETERS
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# WAVENUMBER INTEGRATION PARAMETERS\n# ================\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['WAVENUMBER_INTEGRATION_PARAMETERS']['sw_algorithm']) + '     |int: sw_algorithm;\n'
        txt = ''
        for i in range(len(inp_info_dic['WAVENUMBER_INTEGRATION_PARAMETERS']['sw_cut_off'])):
            txt = txt + str(inp_info_dic['WAVENUMBER_INTEGRATION_PARAMETERS']['sw_cut_off'][i]) + '  '
        inp_content = inp_content + ' ' + txt + '     |dble: slw(1-4);\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['WAVENUMBER_INTEGRATION_PARAMETERS']['sample_rate']) + '     |dble: sample_rate;\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['WAVENUMBER_INTEGRATION_PARAMETERS']['supp_factor']) + '     |dble: supp_factor;\n'
        # inp_content = inp_content + ' ' + str(inp_info_dic['WAVENUMBER_INTEGRATION_PARAMETERS']['source_radius']) + '     ||dble: source_radius;\n'
        inp_content = inp_content + '#------------------------------------------------------------------------------\n'

        # OPTIONS FOR PARTIAL SOLUTIONS
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# OPTIONS FOR PARTIAL SOLUTIONS\n# ==========================\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['OPTIONS_FOR_PARTIAL_SOLUTIONS']['isurf']) + '     |int: isurf;\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['OPTIONS_FOR_PARTIAL_SOLUTIONS']['sw_path_filter']) + '   ' + str(inp_info_dic['OPTIONS_FOR_PARTIAL_SOLUTIONS']['shallow_depth_limit']) + '     |int: sw_path_filter; dble:shallow_depth_limit;\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['OPTIONS_FOR_PARTIAL_SOLUTIONS']['no_of_depth_ranges']) + '     |int: no_of_depth_ranges;\n'
        if not inp_info_dic['OPTIONS_FOR_PARTIAL_SOLUTIONS']['no_of_depth_ranges'] == 0 :
            txt = ''
            for i in range(len(inp_info_dic['OPTIONS_FOR_PARTIAL_SOLUTIONS']['depth_ranges'])):
                txt = txt + ' '
                for j in range(len(inp_info_dic['OPTIONS_FOR_PARTIAL_SOLUTIONS']['depth_ranges'][i])):
                    txt = txt + str(inp_info_dic['OPTIONS_FOR_PARTIAL_SOLUTIONS']['depth_ranges'][i][j]) + '  '
                txt = txt + '\n'
            inp_content = inp_content + txt
        inp_content = inp_content + '#------------------------------------------------------------------------------\n'

        # OURCE TIME FUNCTION (WAVELET) PARAMETERS
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# SOURCE TIME FUNCTION (WAVELET) PARAMETERS\n# ===============================\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['SOURCE_TIME_FUNCTION_WAVELET_PARAMETERS']['wavelet_duration']) + '   ' + str(inp_info_dic['SOURCE_TIME_FUNCTION_WAVELET_PARAMETERS']['sw_wavelet']) + '     |int:dble: wavelet_duration; sw_wavelet;\n'
        if inp_info_dic['SOURCE_TIME_FUNCTION_WAVELET_PARAMETERS']['sw_wavelet'] == 0:
            inp_content = inp_content + ' ' + str(inp_info_dic['SOURCE_TIME_FUNCTION_WAVELET_PARAMETERS']['no_w_samples']) + '     |int: no_w_samples; below dble: w_samples;\n'
            txt = ''
            for i in range(len(inp_info_dic['SOURCE_TIME_FUNCTION_WAVELET_PARAMETERS']['w_samples'])):
                txt = txt + str(inp_info_dic['SOURCE_TIME_FUNCTION_WAVELET_PARAMETERS']['w_samples'][i]) + '  '
            txt = txt + '\n'
            inp_content = inp_content + txt
        inp_content = inp_content + '#------------------------------------------------------------------------------\n'

        # FILTER PARAMETERS OF RECEIVERS (SEISMOMETERS OR HYDROPHONES)
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# FILTER PARAMETERS OF RECEIVERS (SEISMOMETERS OR HYDROPHONES)\n# =====================================\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['FILTER_PARAMETERS_OF_RECEIVERS']['constant_coefficient']) + '\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['FILTER_PARAMETERS_OF_RECEIVERS']['number_of_roots']) + '\n'
        if inp_info_dic['FILTER_PARAMETERS_OF_RECEIVERS']['number_of_roots'] == 0:
            inp_content = inp_content + '# \n'
        else:
            txt = ''
            for i in range(len(inp_info_dic['FILTER_PARAMETERS_OF_RECEIVERS']['list_of_the_roots'])):
                txt = txt + str(inp_info_dic['FILTER_PARAMETERS_OF_RECEIVERS']['list_of_the_roots'][i]) + ', '
            txt = txt + '\n'
            inp_content = inp_content + ' ' + txt
        inp_content = inp_content + ' ' + str(inp_info_dic['FILTER_PARAMETERS_OF_RECEIVERS']['number_of_poles']) + '\n'
        if inp_info_dic['FILTER_PARAMETERS_OF_RECEIVERS']['number_of_poles'] == 0:
            inp_content = inp_content + '# \n'
        else:
            txt = ''
            for i in range(len(inp_info_dic['FILTER_PARAMETERS_OF_RECEIVERS']['list_of_the_poles'])):
                txt = txt + str(inp_info_dic['FILTER_PARAMETERS_OF_RECEIVERS']['list_of_the_poles'][i]) + ', '
            txt = txt + '\n'
            inp_content = inp_content + ' ' + txt
        inp_content = inp_content + '#------------------------------------------------------------------------------\n'

        # 	OUTPUT FILES FOR GREEN'S FUNCTIONS (Note 4)
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# OUTPUT FILES FOR GREENS FUNCTIONS\n# =====================================\n'
        txt = ''
        for i in range(len(inp_info_dic['OUTPUT_FILES_FOR_GREENS_FUNCTIONS']['source_types'])):
            txt = txt + str(inp_info_dic['OUTPUT_FILES_FOR_GREENS_FUNCTIONS']['source_types'][i]) + '     '
        inp_content = inp_content + '   ' + txt + '     |int\n'
        txt = ''
        for i in range(len(inp_info_dic['OUTPUT_FILES_FOR_GREENS_FUNCTIONS']['names_of_types'])):
            txt = txt + "'" + str(inp_info_dic['OUTPUT_FILES_FOR_GREENS_FUNCTIONS']['names_of_types'][i]) + "'" + '     '
        inp_content = inp_content + '   ' + txt + '     |char\n'
        inp_content = inp_content + '#------------------------------------------------------------------------------\n'

        # OUTPUT FILES FOR AN ARBITRARY POINT DISLOCATION SOURCE
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# OUTPUT FILES FOR AN ARBITRARY POINT DISLOCATION SOURCE\n# =====================================\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['moment_tensor_type'])
        txt = ''
        for i in range(len(inp_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['moment_tensor'])):
            txt = txt + str(inp_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['moment_tensor'][i]) + '  '
        inp_content = inp_content + '  ' + txt + ' ' + "'" + str(inp_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['seis_name']) + "'" + '\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['switch_for_azimuth_distribution']) + '\n'
        txt = ''
        for i in range(len(inp_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['list_of_the_azimuth_angles'])):
            txt = txt + str(inp_info_dic['OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE']['list_of_the_azimuth_angles'][i]) + '  '
        inp_content = inp_content + ' ' + txt + '\n'
        inp_content = inp_content + '#------------------------------------------------------------------------------\n'

        # GLOBAL MODEL PARAMETERS
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# GLOBAL MODEL PARAMETERS\n# ======================\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['GLOBAL_MODEL_PARAMETERS']['sw_flat_earth_transform']) + '     |int: sw_flat_earth_transform;\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['GLOBAL_MODEL_PARAMETERS']['vp_res']) + '  ' + str(inp_info_dic['GLOBAL_MODEL_PARAMETERS']['vs_res']) + '  ' + str(inp_info_dic['GLOBAL_MODEL_PARAMETERS']['ro_res']) + '     |dble: vp_res, vs_res, ro_res;\n'

        # LAYERED EARTH MODEL (SHALLOW SOURCE + UNIFORM DEEP SOURCE/RECEIVER STRUCTURE)
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# LAYERED EARTH MODEL (SHALLOW SOURCE + UNIFORM DEEP SOURCE/RECEIVER STRUCTURE)\n# =====================================\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['LAYERED_EARTH_MODEL_1']['no_model_lines']) + '     |int: no_model_lines;\n'
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# MULTILAYERED MODEL PARAMETERS (source site)\n# =====================================\n# no  depth[km]  vp[km/s]  vs[km/s]  ro[g/cm^3] qp      qs\n#------------------------------------------------------------------------------\n'
        txt = ''
        for i in range(len(vel_mod_dic['no'])):
            txt = txt + str(vel_mod_dic['no'][i]) + '   ' + str(vel_mod_dic['depth'][i]) + '   ' + str(vel_mod_dic['vp'][i]) +'   ' + str(vel_mod_dic['vs'][i]) +'   ' + str(vel_mod_dic['ro'][i]) + '   ' + str(vel_mod_dic['qp'][i]) + '   ' + str(vel_mod_dic['qs'][i]) + '\n'
        inp_content = inp_content + txt
        inp_content = inp_content + '#------------------------------------------------------------------------------\n'

        # LAYERED EARTH MODEL (ONLY THE SHALLOW RECEIVER STRUCTURE)
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# LAYERED EARTH MODEL (ONLY THE SHALLOW RECEIVER STRUCTURE)\n# =====================================\n'
        inp_content = inp_content + ' ' + str(inp_info_dic['LAYERED_EARTH_MODEL_2']['no_model_lines']) + '     |int: no_model_lines;\n'
        inp_content = inp_content + '#------------------------------------------------------------------------------\n# MULTILAYERED MODEL PARAMETERS (receiver site)\n# =====================================\n# no  depth[km]  vp[km/s]  vs[km/s]  ro[g/cm^3] qp      qs\n#------------------------------------------------------------------------------\n'
        txt =''
        for i in range(len(inp_info_dic['LAYERED_EARTH_MODEL_2']['MULTILAYERED_MODEL_PARAMETERS']['no'])):
            txt = txt + ' %d   %f   %f   %f   %f   %f   %f\n' % (inp_info_dic['LAYERED_EARTH_MODEL_2']['MULTILAYERED_MODEL_PARAMETERS']['no'][i], inp_info_dic['LAYERED_EARTH_MODEL_2']['MULTILAYERED_MODEL_PARAMETERS']['depth'][i], inp_info_dic['LAYERED_EARTH_MODEL_2']['MULTILAYERED_MODEL_PARAMETERS']['vp'][i], inp_info_dic['LAYERED_EARTH_MODEL_2']['MULTILAYERED_MODEL_PARAMETERS']['vs'][i], inp_info_dic['LAYERED_EARTH_MODEL_2']['MULTILAYERED_MODEL_PARAMETERS']['ro'][i], inp_info_dic['LAYERED_EARTH_MODEL_2']['MULTILAYERED_MODEL_PARAMETERS']['qp'][i], inp_info_dic['LAYERED_EARTH_MODEL_2']['MULTILAYERED_MODEL_PARAMETERS']['qs'][i])
        inp_content = inp_content + txt
        inp_content = inp_content + '#------------------------------------------------------------------------------\n'

        # end
        inp_content = inp_content + '#---------------------------------end of all inputs----------------------------\n'

        self.inp_content = inp_content

        return self.inp_content


    def write_modify_inputfile(self, modify_inputfile_path=None, inputfile_content=None):
        '''
        '''
        if modify_inputfile_path == None:
            modify_inputfile_path = deepcopy(self.path_info_dic['modify_dic']['modify_inputfile_path'])
        else:
            modify_inputfile_path = modify_inputfile_path
        if inputfile_content == None:
            inputfile_content = deepcopy(self.inp_content)
        else:
            inputfile_content = inputfile_content

        modify_inputfile_file = open(modify_inputfile_path, 'w')
        modify_inputfile_file.write(inputfile_content)
        modify_inputfile_file.close()


if __name__ == '__main__':

    paths_info_dic = {
        'gen_data_dic' : {
            'qseis_path': '../../qseis06/qseis06',
            'vel_base_model_path': './vel_base_model.dat',
            'inputfile_path': './inputfile.inp',
        },
        'log_dic' : {
            'log_path': './log',
            'log_file_path': './log_file',
            'log_gen': './log_gen'
        },
    }

    input_info_dic = {
        'SOURCE_PARAMETERS' : {
            'source_depth' : float(519),
        },
        'RECEIVER_PARAMETERS' : {
            'receiver_depth' : float(0.000),
            'sw_equidistant' : int(0),
            'sw_d_unit' : int(0),
            'no_distances' : int(7),
            'list_of_distances' : list([1,2,3,4,5,6,7]),
            't_start' : float(100.0),
            't_window' : float(600.0),
            'no_t_samples' : int(1201),
            'sw_t_reduce' : int(0),
            't_reduce' : float(0.0),
        },
        'WAVENUMBER_INTEGRATION_PARAMETERS' : {
            'sw_algorithm' : int(1),
            'sw_cut_off' : list([0.008,0.020,4.000,4.500]),
            'sample_rate' : float(2.50),
            'supp_factor' : float(0.01),
            # 'source_radius' : float(-1.0),
        },
        'OPTIONS_FOR_PARTIAL_SOLUTIONS' : {
            'isurf' : int(0),
            'sw_path_filter' : int(0),
            'shallow_depth_limit' : float(500.0),
            'no_of_depth_ranges' : int(0),
            'depth_range' : list([[0.0,5153.0,3]]),
        },
        'SOURCE_TIME_FUNCTION_WAVELET_PARAMETERS' : {
            'wavelet_duration' : 1.6,
            'sw_wavelet' : int(1),
            'no_w_samples' : int(100),
            'w_samples' : list([]),
        },
        'FILTER_PARAMETERS_OF_RECEIVERS' : {
            'constant_coefficient' : float(1.0),
            'number_of_roots' : int(0),
            'list_of_the_roots' : list([(0.0,0.0)]),
            'number_of_poles' : int(1),
            'list_of_the_poles' : list([(0.0,0.0)]),
        },
        'OUTPUT_FILES_FOR_GREENS_FUNCTIONS' : {
            'source_types' : list([1,1,1,0,0,0]),
            'names_of_types' : list(['ex','ss','ds','cl','fz','fh']),
        },
        'OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE' : {
            'moment_tensor_type' : int(1),
            'moment_tensor' : list([1.410,-1.460,0.055,-2.410,2.580,1.290]),
            'seis_name' : str('seis'),
            'switch_for_azimuth_distribution' : int(0),
            'list_of_the_azimuth_angles' : list([123]),
        },
        'GLOBAL_MODEL_PARAMETERS' : {
            'sw_flat_earth_transform' : int(1),
            'vp_res' : float(0.1),
            'vs_res' : float(0.1),
            'ro_res' : float(0.1),
        },
        'LAYERED_EARTH_MODEL_1' : {
            'no_model_lines' : int(),
            'MULTILAYERED_MODEL_PARAMETERS' : {},
            'inp_depth_of_used_model_layer' : 1500
        },
        'LAYERED_EARTH_MODEL_2' : {
            'no_model_lines' : int(0),
            'MULTILAYERED_MODEL_PARAMETERS' : {
                'no' : [1,2,3,4,5,6,7,8,9],
                'depth' : [0.000,2.000,2.000,7.000,7.000,17.000,17.000,35.000,35.000],
                'vp' : [2.900,2.900,5.400,5.400,6.160,6.160,6.630,6.630,8.0400],
                'vs' : [1.676,1.676,3.121,3.121,3.561,3.561,3.832,3.832,4.4700],
                'ro' : [2.600,2.600,2.600,2.600,2.600,2.600,2.900,2.900,3.3198],
                'qp' : [92.00,92.00,92.00,92.00,576.00,576.00,576.00,576.00,1340.00],
                'qs' : [41.00,41.00,41.00,41.00,256.00,256.00,256.00,256.00,600.00]
            },
        },
    }


    m_i = modify_inputfile(input_info_dic, paths_info_dic)
    modify_velocity_model_dic = m_i.get_modify_vel_mod(vel_model_path='./vel_modify_velocity.dat',)
    inputfile_content = m_i.generate_inp_content()
    m_i.write_modify_inputfile(modify_inputfile_path='./mod_inp.inp')






