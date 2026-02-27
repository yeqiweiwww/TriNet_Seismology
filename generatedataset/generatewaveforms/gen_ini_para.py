
'''

'''

import os

# path


datafilepath = os.path.dirname(os.path.abspath(__file__)).replace('generatedata_v','data/generatedata_v')

paths_info_dic = {
    'gen_data_dic' : {
        'temp_file' : '.',
        'qseis_path': './qseis06',
        'vel_base_model_path': './vel_base_model.dat',
        'inputfile_path': './inputfile.inp',
    },
    'modify_dic' : {
        'modify_velocity_model_path_dir': datafilepath + '/modified_modelfile',
        'modify_inputfile_path_dir': datafilepath + '/modified_inputfile',
        'modify_ttfile': datafilepath + '/modify_ttfile',
        'modify_tzfile': datafilepath + '/modify_tzfile',
        'modify_trfile': datafilepath + '/modify_trfile',
        'modify_otherdata': datafilepath + '/modify_otherdata',
        'modify_nd_file_path_dir': datafilepath + '/modify_nd_file',
        'modify_npz_file_path_dir': datafilepath + '/modify_npz_file',
    },
    'log_dic' : {
        'log_path_dir': datafilepath + '/log',
        'log_file_path_dir': './log_file',
        'log_gen_dir': './log_gen'
    },
}

# 输入文件参数

input_info_dic = {
    'SOURCE_PARAMETERS' : {
        'source_depth' : float(519),
    },
    'RECEIVER_PARAMETERS' : {
        'receiver_depth' : float(0.000),
        'sw_equidistant' : int(0),
        'sw_d_unit' : int(0),
        'no_distances' : int(45),
        'list_of_distances' : list([10.224929,10.611104,10.920886,11.46489,11.970286,12.31973,12.800243,13.10525,13.575499,13.894837,14.143772,14.746186,15.171263,15.423911,15.837851,16.208076,16.604109,17.114248,17.486032,18.220173,19.031988,19.243315,19.935616,20.271973,20.931608,21.394547,21.926945,22.317497,22.649956,22.96242,23.429052,23.855242,24.14646,24.604383,24.795444,25.123894,25.770329,26.291788,26.456755,26.830933,27.205534,27.497725,28.096323,29.022808,29.294538]),
        't_start' : float(100.0),
        't_window' : float(300.0),
        'no_t_samples' : int(601),
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
        'depth_range' : list([[0.0,5153.0,int(3)]]),
    },
    'SOURCE_TIME_FUNCTION_WAVELET_PARAMETERS' : {
        'wavelet_duration' : float(1.6),
        'sw_wavelet' : int(1),
        'no_w_samples' : int(100),
        'w_samples' : list([]),
    },
    'FILTER_PARAMETERS_OF_RECEIVERS' : {
        'constant_coefficient' : float(1.0),
        # 'constant_coefficient' : tuple((1.0,0.0)),
        'number_of_roots' : int(0),
        'list_of_the_roots' : list([(0.0,0.0)]),
        'number_of_poles' : int(1),
        'list_of_the_poles' : list([(0.0,0.0)]),
    },
    'OUTPUT_FILES_FOR_GREENS_FUNCTIONS' : {
        'source_types' : list([int(1),int(1),int(1),int(0),int(0),int(0)]),
        'names_of_types_base' : list(['ex','ss','ds','cl','fz','fh']),
    },
    'OUTPUT_FILES_FOR_AN_ARBITRARY_POINT_DISLOCATION_SOURCE' : {
        'moment_tensor_type' : int(1),
        'moment_tensor' : list([1.410,-1.460,0.055,-2.410,2.580,1.290]),
        'seis_name_base' : str('seis'),
        'switch_for_azimuth_distribution' : int(1),
        'list_of_the_azimuth_angles' : list([263.7338,263.19855,262.55646,264.8294,264.41965,262.1525,265.0716,262.47604,265.141,259.2523,257.33218,256.53027,268.69073,267.08383,260.3167,264.36975,264.49207,257.18427,264.08902,259.545,255.6468,263.9922,256.02863,264.94562,265.3539,259.69626,265.32266,258.3724,265.0072,269.72787,265.18146,264.88324,263.19025,264.65964,259.935,255.01736,265.00516,259.0525,257.49588,270.62653,265.10596,257.22012,273.01685,255.30807,265.56317]),
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
        'inp_depth_of_used_model_layer' : float(1500),
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
        'inp_depth_of_used_model_layer' : float() ,
    },
}


# velocity model

vel_model_info_dic = {
    'modify_depth_layer_depth' : 660.0,
    'modify_depth_changed_range' : 30.0,
    'interpolation_start_depth' : 510.0,
    'interpolation_end_depth' : 800.0,
    'interpolation_each_layer_depth' : 20.0,
    'modify_velocity_percent' : 0.03,
    'modify_start_depth' : 510.0,
    'modify_end_depth' : 1000.0,
}


# gen_data

echo = 900
server_name = '_seis_'

azi1,azi2 = 255, 275

















