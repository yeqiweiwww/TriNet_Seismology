

'''
'''
from copy import deepcopy
import random

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

class modify_vel_base_model():

    def __init__(
            self, 
            velocity_model_info_dic, 
            path_info_dic
    ):
        self.velocity_model_info_dic = velocity_model_info_dic
        self.path_info_dic = path_info_dic


    def read_vel_base(self, vel_base_model_path=None):
        '''
        '''

        if vel_base_model_path == None:
            vel_base_model_path = deepcopy(self.path_info_dic['gen_data_dic']['vel_base_model_path'])
        else:
            vel_base_model_path = vel_base_model_path

        vel_base_model_file = pd.read_csv(vel_base_model_path)
        vel_base_model_index = vel_base_model_file.columns[0]
        vel_base_model = vel_base_model_file[vel_base_model_index].str.split(pat = None, n = -1, expand = True )

        no_vel_base_model = []; depth_vel_base_model = []; vp_vel_base_model = []; vs_vel_base_model = []; ro_vel_base_model = []; qp_vel_base_model = []; qs_vel_base_model = []
        for i in range(len(vel_base_model)):
            no_vel_base_model.append(deepcopy(int(vel_base_model[0][i])))
            depth_vel_base_model.append(deepcopy(float(vel_base_model[1][i])))
            vp_vel_base_model.append(deepcopy(float(vel_base_model[2][i])))
            vs_vel_base_model.append(deepcopy(float(vel_base_model[3][i])))
            ro_vel_base_model.append(deepcopy(float(vel_base_model[4][i])))
            qp_vel_base_model.append(deepcopy(float(vel_base_model[5][i])))
            qs_vel_base_model.append(deepcopy(float(vel_base_model[6][i])))

        self.vel_base_model_dict_original = {
            'no':no_vel_base_model, 
            'depth':depth_vel_base_model, 
            'vp':vp_vel_base_model, 
            'vs':vs_vel_base_model, 
            'ro':ro_vel_base_model, 
            'qp':qp_vel_base_model, 
            'qs':qs_vel_base_model
            }

        return self.vel_base_model_dict_original


    def interpolation_model(
            self,
            interpolation_start_depth=None, 
            interpolation_end_depth=None, 
            modify_depth_layer_depth=None, 
            interpolation_each_layer_depth=None, 
            modify_depth_changed_range=None, 
            velocity_model_dict=None
    ):
        '''
        '''


        if interpolation_start_depth == None:
            interpolation_start_depth = deepcopy(self.velocity_model_info_dic['interpolation_start_depth'])
        else:
            interpolation_start_depth = interpolation_start_depth
        if interpolation_end_depth == None:
            interpolation_end_depth = deepcopy(self.velocity_model_info_dic['interpolation_end_depth'])
        else:
            interpolation_end_depth = interpolation_end_depth
        if modify_depth_layer_depth == None:
            modify_depth_layer_depth = deepcopy(self.velocity_model_info_dic['modify_depth_layer_depth'])
        else:
            modify_depth_layer_depth = modify_depth_layer_depth
        if interpolation_each_layer_depth == None:
            interpolation_each_layer_depth = deepcopy(self.velocity_model_info_dic['interpolation_each_layer_depth'])
        else:
            interpolation_each_layer_depth = interpolation_each_layer_depth
        if modify_depth_changed_range == None:
            modify_depth_changed_range = deepcopy(self.velocity_model_info_dic['modify_depth_changed_range'])
        else:
            modify_depth_changed_range = modify_depth_changed_range
        if velocity_model_dict == None:
            velocity_model_dict = deepcopy(self.vel_base_model_dict_original)
        else:
            velocity_model_dict = velocity_model_dict


        modify_depth_layer_depth_index = [i for i, x in enumerate(velocity_model_dict['depth']) if x == modify_depth_layer_depth]


        depth_velocity_model_interpolation= deepcopy(velocity_model_dict['depth'])
        vp_velocity_model_interpolation = deepcopy(velocity_model_dict['vp'])
        vs_velocity_model_interpolation = deepcopy(velocity_model_dict['vs'])
        ro_velocity_model_interpolation = deepcopy(velocity_model_dict['ro'])
        qp_velocity_model_interpolation = deepcopy(velocity_model_dict['qp'])
        qs_velocity_model_interpolation = deepcopy(velocity_model_dict['qs'])


        interpolation_start_index = next((i for i, x in enumerate(depth_velocity_model_interpolation) if x > interpolation_start_depth), None)
        interpolation_end_index = next((i for i, x in enumerate(depth_velocity_model_interpolation) if x >= interpolation_end_depth), None) - 1


        depth_velocity_model_interpolation_1 = []
        depth_velocity_model_interpolation_1.append(depth_velocity_model_interpolation[interpolation_start_index])

        while depth_velocity_model_interpolation_1[-1] + interpolation_each_layer_depth < depth_velocity_model_interpolation[modify_depth_layer_depth_index[0]] - modify_depth_changed_range:
            depth_velocity_model_interpolation_1.append(depth_velocity_model_interpolation_1[-1] + interpolation_each_layer_depth)

        depth_velocity_model_interpolation_1.append(depth_velocity_model_interpolation[modify_depth_layer_depth_index[0]] - modify_depth_changed_range)
        depth_velocity_model_interpolation_1.append(depth_velocity_model_interpolation[modify_depth_layer_depth_index[0]])

        x = depth_velocity_model_interpolation[interpolation_start_index:modify_depth_layer_depth_index[0]+1]
        y = vp_velocity_model_interpolation[interpolation_start_index:modify_depth_layer_depth_index[0]+1]
        f = interp1d(x, y, kind='linear')
        vp_velocity_model_interpolation_1 = list(f(depth_velocity_model_interpolation_1))

        y = vs_velocity_model_interpolation[interpolation_start_index:modify_depth_layer_depth_index[0]+1]
        f = interp1d(x, y, kind='linear')
        vs_velocity_model_interpolation_1 = list(f(depth_velocity_model_interpolation_1))

        y = ro_velocity_model_interpolation[interpolation_start_index:modify_depth_layer_depth_index[0]+1]
        f = interp1d(x, y, kind='linear')
        ro_velocity_model_interpolation_1 = list(f(depth_velocity_model_interpolation_1))

        y = qp_velocity_model_interpolation[interpolation_start_index:modify_depth_layer_depth_index[0]+1]
        f = interp1d(x, y, kind='linear')
        qp_velocity_model_interpolation_1 = list(f(depth_velocity_model_interpolation_1))

        y = qs_velocity_model_interpolation[interpolation_start_index:modify_depth_layer_depth_index[0]+1]
        f = interp1d(x, y, kind='linear')
        qs_velocity_model_interpolation_1 = list(f(depth_velocity_model_interpolation_1))


        depth_velocity_model_interpolation_2 = []
        depth_velocity_model_interpolation_2.append(depth_velocity_model_interpolation[modify_depth_layer_depth_index[1]])
        depth_velocity_model_interpolation_2.append(depth_velocity_model_interpolation[modify_depth_layer_depth_index[1]]+modify_depth_changed_range)

        while depth_velocity_model_interpolation_2[-1] + interpolation_each_layer_depth < depth_velocity_model_interpolation[interpolation_end_index]:
            depth_velocity_model_interpolation_2.append(depth_velocity_model_interpolation_2[-1] + interpolation_each_layer_depth)

        depth_velocity_model_interpolation_2.append(depth_velocity_model_interpolation[interpolation_end_index])

        x = depth_velocity_model_interpolation[modify_depth_layer_depth_index[1]:interpolation_end_index+1]
        y = vp_velocity_model_interpolation[modify_depth_layer_depth_index[1]:interpolation_end_index+1]
        f = interp1d(x, y, kind='linear')
        vp_velocity_model_interpolation_2 = list(f(depth_velocity_model_interpolation_2))

        y = vs_velocity_model_interpolation[modify_depth_layer_depth_index[1]:interpolation_end_index+1]
        f = interp1d(x, y, kind='linear')
        vs_velocity_model_interpolation_2 = list(f(depth_velocity_model_interpolation_2))

        y = ro_velocity_model_interpolation[modify_depth_layer_depth_index[1]:interpolation_end_index+1]
        f = interp1d(x, y, kind='linear')
        ro_velocity_model_interpolation_2 = list(f(depth_velocity_model_interpolation_2))

        y = qp_velocity_model_interpolation[modify_depth_layer_depth_index[1]:interpolation_end_index+1]
        f = interp1d(x, y, kind='linear')
        qp_velocity_model_interpolation_2 = list(f(depth_velocity_model_interpolation_2))

        y = qs_velocity_model_interpolation[modify_depth_layer_depth_index[1]:interpolation_end_index+1]
        f = interp1d(x, y, kind='linear')
        qs_velocity_model_interpolation_2 = list(f(depth_velocity_model_interpolation_2))


        depth_velocity_model_interpolation_1.extend(depth_velocity_model_interpolation_2)
        vp_velocity_model_interpolation_1.extend(vp_velocity_model_interpolation_2)
        vs_velocity_model_interpolation_1.extend(vs_velocity_model_interpolation_2)
        ro_velocity_model_interpolation_1.extend(ro_velocity_model_interpolation_2)
        qp_velocity_model_interpolation_1.extend(qp_velocity_model_interpolation_2)
        qs_velocity_model_interpolation_1.extend(qs_velocity_model_interpolation_2)


        depth_velocity_model_interpolation[interpolation_start_index:interpolation_end_index+1] = depth_velocity_model_interpolation_1
        vp_velocity_model_interpolation[interpolation_start_index:interpolation_end_index+1] = vp_velocity_model_interpolation_1
        vs_velocity_model_interpolation[interpolation_start_index:interpolation_end_index+1] = vs_velocity_model_interpolation_1
        ro_velocity_model_interpolation[interpolation_start_index:interpolation_end_index+1] = ro_velocity_model_interpolation_1
        qp_velocity_model_interpolation[interpolation_start_index:interpolation_end_index+1] = qp_velocity_model_interpolation_1
        qs_velocity_model_interpolation[interpolation_start_index:interpolation_end_index+1] = qs_velocity_model_interpolation_1
        

        no_velocity_model_interpolation = [i for i in range(1, len(depth_velocity_model_interpolation)+1)]

        self.vel_base_model_dict_interpolation = {
            'no':no_velocity_model_interpolation,
            'depth':depth_velocity_model_interpolation, 
            'vp':vp_velocity_model_interpolation, 
            'vs':vs_velocity_model_interpolation, 
            'ro':ro_velocity_model_interpolation, 
            'qp':qp_velocity_model_interpolation, 
            'qs':qs_velocity_model_interpolation
            }
        self.interpolation_each_layer_depth = interpolation_each_layer_depth

        return self.vel_base_model_dict_interpolation


    def modify_layer_depth(
            self, 
            modify_depth_changed_range=None, 
            modify_depth_layer_depth=None, 
            velocity_model_dict=None
    ):
        '''
        '''


        if modify_depth_changed_range == None:
            modify_depth_changed_range = deepcopy(self.velocity_model_info_dic['modify_depth_changed_range'])
        else:
            modify_depth_changed_range = modify_depth_changed_range
        if modify_depth_layer_depth == None:
            modify_depth_layer_depth = deepcopy(self.velocity_model_info_dic['modify_depth_layer_depth'])
        else:
            modify_depth_layer_depth = modify_depth_layer_depth
        if velocity_model_dict == None:
            velocity_model_dict = deepcopy(self.vel_base_model_dict_interpolation)
        else:
            velocity_model_dict = velocity_model_dict
        

        modify_depth_layer_depth_index = [i for i, x in enumerate(velocity_model_dict['depth']) if x == modify_depth_layer_depth]


        depth_velocity_model_modify_layer_depth = deepcopy(velocity_model_dict['depth'])


        depth_velocity_model_modify_layer_depth[modify_depth_layer_depth_index[0]] = modify_depth_layer_depth + random.uniform(-modify_depth_changed_range, modify_depth_changed_range)
        depth_velocity_model_modify_layer_depth[modify_depth_layer_depth_index[1]] = random.uniform(depth_velocity_model_modify_layer_depth[modify_depth_layer_depth_index[0]], modify_depth_layer_depth+modify_depth_changed_range)


        thickness = depth_velocity_model_modify_layer_depth[modify_depth_layer_depth_index[1]] - depth_velocity_model_modify_layer_depth[modify_depth_layer_depth_index[0]]


        self.vel_base_model_dict_modify_layer_depth = deepcopy(velocity_model_dict)
        self.vel_base_model_dict_modify_layer_depth['depth'] = depth_velocity_model_modify_layer_depth


        self.modify_depth_layer_depth = depth_velocity_model_modify_layer_depth[modify_depth_layer_depth_index[0]]
        self.thickness = thickness

        return self.vel_base_model_dict_modify_layer_depth, self.thickness


    def modify_velocity(
            self, 
            modify_velocity_percent=None, 
            modify_start_depth=None, 
            modify_end_depth=None, 
            modify_depth_layer_depth=None, 
            velcity_model_dict=None
    ):
        
        '''
        '''


        if modify_velocity_percent == None:
            modify_velocity_percent = self.velocity_model_info_dic['modify_velocity_percent']
        else:
            modify_velocity_percent = modify_velocity_percent
        if modify_start_depth == None:
            modify_start_depth = deepcopy(self.velocity_model_info_dic['modify_start_depth'])
        else:
            modify_start_depth = modify_start_depth
        if modify_end_depth == None:
            modify_end_depth = deepcopy(self.velocity_model_info_dic['modify_end_depth'])
        else:
            modify_end_depth = modify_end_depth
        if modify_depth_layer_depth == None:
            modify_depth_layer_depth = deepcopy(self.modify_depth_layer_depth)
        else:
            modify_depth_layer_depth = modify_depth_layer_depth
        if velcity_model_dict == None:
            velcity_model_dict = deepcopy(self.vel_base_model_dict_modify_layer_depth)
        else:
            velcity_model_dict = velcity_model_dict
        

        no_velocity_model_modify_velocity = deepcopy(velcity_model_dict['no'])
        vp_velocity_model_modify_velocity = deepcopy(velcity_model_dict['vp'])
        vs_velocity_model_modify_velocity = deepcopy(velcity_model_dict['vs'])


        modify_start_index = next((i for i, x in enumerate(velcity_model_dict['depth']) if x > modify_start_depth), None)
        modify_end_index = next((i for i, x in enumerate(velcity_model_dict['depth']) if x > modify_end_depth), None) -1


        vk_ran_vp = []
        vk_ran_vs = []

        for i in range(modify_start_index, modify_end_index):

            vk_ran_vp_u = random.uniform(1-modify_velocity_percent, 1+modify_velocity_percent)
            vk_ran_vp.append(vk_ran_vp_u-1)
            vk_ran_vs_u = random.uniform(1-modify_velocity_percent, 1+modify_velocity_percent)
            vk_ran_vs.append(vk_ran_vs_u-1)

            vp_velocity_model_modify_velocity[i] = vp_velocity_model_modify_velocity[i] * vk_ran_vp_u
            vs_velocity_model_modify_velocity[i] = vs_velocity_model_modify_velocity[i] * vk_ran_vs_u


        v_ran_change = {}
        v_ran_change['vp'] = vk_ran_vp
        v_ran_change['vs'] = vk_ran_vs


        self.vel_base_model_dict_modify_velocity = deepcopy(velcity_model_dict)
        self.vel_base_model_dict_modify_velocity['vp'] = vp_velocity_model_modify_velocity
        self.vel_base_model_dict_modify_velocity['vs'] = vs_velocity_model_modify_velocity


        self.changed_depth_no = no_velocity_model_modify_velocity[modify_start_index:modify_end_index]
        self.v_ran_change = v_ran_change

        return self.vel_base_model_dict_modify_velocity, self.v_ran_change


    def write_model_interpolation(
            self, 
            changed_depth_no=None, 
            velocity_model_dict=None, 
            write_path=None
    ):
        '''
        '''


        if write_path == None:
            write_path = deepcopy(self.path_info_dic['modify_dic']['interpolation_model_path'])
        else:
            write_path = write_path
        if velocity_model_dict == None:
            velocity_model_dict = deepcopy(self.vel_base_model_dict_interpolation)
        else:
            velocity_model_dict = velocity_model_dict
        if changed_depth_no == None:
            changed_depth_no = deepcopy(self.changed_depth_no)
        else:
            changed_depth_no = changed_depth_no


        with open(write_path, 'w') as f:
            f.write('  no   depth[km]   vp[km/s]   vs[km/s]   ro[g/cm^3]   qp   qs\n')
            for i in range(len(velocity_model_dict['no'])):
                f.write('%d   %f   %f   %f   %f   %f   %f\n' % (velocity_model_dict['no'][i], velocity_model_dict['depth'][i], velocity_model_dict['vp'][i], velocity_model_dict['vs'][i], velocity_model_dict['ro'][i], velocity_model_dict['qp'][i], velocity_model_dict['qs'][i]))
            # f.write('changed depth: %d \n' % len(changed_depth_no))
            # for i in range(len(changed_depth_no)):
            #     f.write('%d,' % changed_depth_no[i])


    def write_model_modify_layer_depth(
            self, 
            changed_depth_no=None, 
            velocity_model_dict=None, 
            write_path=None
    ):
        '''
        '''


        if write_path == None:
            write_path = deepcopy(self.path_info_dic['modify_dic']['modify_layer_depth_path'])
        else:
            write_path = write_path
        if velocity_model_dict == None:
            velocity_model_dict = deepcopy(self.vel_base_model_dict_modify_layer_depth)
        else:
            velocity_model_dict = velocity_model_dict
        if changed_depth_no == None:
            changed_depth_no = deepcopy(self.changed_depth_no)
        else:
            changed_depth_no = changed_depth_no


        with open(write_path, 'w') as f:
            f.write('  no   depth[km]   vp[km/s]   vs[km/s]   ro[g/cm^3]   qp   qs\n')
            for i in range(len(velocity_model_dict['no'])):
                f.write('%d   %f   %f   %f   %f   %f   %f\n' % (velocity_model_dict['no'][i], velocity_model_dict['depth'][i], velocity_model_dict['vp'][i], velocity_model_dict['vs'][i], velocity_model_dict['ro'][i], velocity_model_dict['qp'][i], velocity_model_dict['qs'][i]))
            # f.write('changed depth: %d \n' % len(changed_depth_no))
            # for i in range(len(changed_depth_no)):
            #     f.write('%d,' % changed_depth_no[i])


    def write_modify_velocity_model(
            self, 
            changed_depth_no=None, 
            velocity_model_dict=None, 
            write_path=None, 
            modify_depth_layer_depth=None
    ):
        '''
        '''


        if velocity_model_dict == None:
            velocity_model_dict = deepcopy(self.vel_base_model_dict_modify_velocity)
        else:
            velocity_model_dict = velocity_model_dict
        if changed_depth_no == None:
            changed_depth_no = deepcopy(self.changed_depth_no)
        else:
            changed_depth_no = changed_depth_no
        if write_path == None:
            write_path = deepcopy(self.path_info_dic['modify_dic']['modify_velocity_model_path'])
        else:
            write_path = write_path
        if modify_depth_layer_depth == None:
            modify_depth_layer_depth = deepcopy(self.modify_depth_layer_depth)
        else:
            modify_depth_layer_depth = modify_depth_layer_depth


        with open(write_path, 'w') as f:
            f.write('  no   depth[km]   vp[km/s]   vs[km/s]   ro[g/cm^3]   qp   qs\n')
            txt_t = ''
            for i in range(len(velocity_model_dict['no'])):
                txt_t = txt_t + str(velocity_model_dict['no'][i]) + '   ' + str(velocity_model_dict['depth'][i]) + '   ' + str(velocity_model_dict['vp'][i]) + '   ' + str(velocity_model_dict['vs'][i]) + '   ' + str(velocity_model_dict['ro'][i]) + '   ' + str(velocity_model_dict['qp'][i]) + '   ' + str(velocity_model_dict['qs'][i]) + '\n'
            f.write(txt_t)
            # f.write('changed depth:'+str(len(changed_depth_no)))
            # f.write('\n')
            # f.write('changed_depth_no:')
            # txt_t = ''
            # for i in range(len(changed_depth_no)):
            #     txt_t = txt_t + str(changed_depth_no[i]) + ','
            # f.write(txt_t)
            # f.write('\n')
            # f.write('660km:'+str(modify_depth_layer_depth))
            # f.write('\n')
            # f.write('thickness:'+str(self.thickness))
            # f.write('\n')
            # f.write('vp_change:')
            # txt_t = ''
            # for i in range(len(self.v_ran_change['vp'])):
            #     txt_t = txt_t + str(self.v_ran_change['vp'][i]) + ','
            # f.write(txt_t)
            # f.write('\n')
            # f.write('vs_change:')
            # txt_t = ''
            # for i in range(len(self.v_ran_change['vs'])):
            #     txt_t = txt_t + str(self.v_ran_change['vs'][i]) + ','
            # f.write(txt_t)

    def generate_nd_file(
            self, 
            velocity_model_dict=None, 
            write_path=None, 
    ):
        '''
        '''


        if velocity_model_dict == None:
            velocity_model_dict = deepcopy(self.vel_base_model_dict_modify_velocity)
        else:
            velocity_model_dict = velocity_model_dict
        if write_path == None:
            write_path = deepcopy(self.path_info_dic['modify_dic']['modify_nd_file_path'])
        else:
            write_path = write_path


        with open(write_path, 'w') as f:
            txt_t = ''
            for i in range(len(velocity_model_dict['no'])):
                txt_t = txt_t + ' ' + str(velocity_model_dict['depth'][i]) + ' ' + str(velocity_model_dict['vp'][i]) + ' ' + str(velocity_model_dict['vs'][i]) + ' ' + str(velocity_model_dict['ro'][i]) + ' ' + str(velocity_model_dict['qp'][i]) + ' ' + str(velocity_model_dict['qs'][i]) + '\n'
            f.write(txt_t)


if __name__ == '__main__':

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

    paths_info_dic = {
        'gen_data_dic' : {
            'vel_base_model_path': './vel_base_model.dat',
        },
    }

    mvbm = modify_vel_base_model(vel_model_info_dic, paths_info_dic)
    mvbm.read_vel_base()
    mvbm.interpolation_model()
    mvbm.modify_layer_depth()
    mvbm.modify_velocity()
    mvbm.write_model_interpolation(write_path='./vel_interpolation.dat')
    mvbm.write_model_modify_layer_depth(write_path='./vel_modify_layer_depth.dat')
    mvbm.write_modify_velocity_model(write_path='./vel_modify_velocity.dat')
    # mvbm.generate_nd_file(velocity_model_dict=vel_base_model_dict_interpolation, write_path='./vel_modify_nd_file.nd')


