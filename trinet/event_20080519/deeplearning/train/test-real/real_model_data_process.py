
from copy import deepcopy

from scipy.interpolate import interp1d

from real_para import modify_velocity_percent,label_range_vel, disc_660, range_660, label_range_dep
from real_utils import get_index
from gen_modify_vel_base import modify_vel_base_model


class model_data_process:
    def __init__(self):
        pass

    def mk_pre_model_data(self, outputdata, output_depth, output_thickness, vel_base_model_path, velocity_model_info_dic):

        path_info_dic = {}
        
        m_a_m = modify_vel_base_model(velocity_model_info_dic, path_info_dic)
        vel_base_model_dict_original = m_a_m.read_vel_base(vel_base_model_path)
        vel_base_model_dict_interpolation = m_a_m.interpolation_model()
        vel_base_model_dict_modify_layer_depth,thickness = m_a_m.modify_layer_depth()
        vel_base_model_dict_modify_velocity, v_ran_chan,changed_depth_no = m_a_m.modify_velocity()

        vel_base_vp = deepcopy(vel_base_model_dict_interpolation['vp'])
        vel_base_depth = vel_base_model_dict_interpolation['depth']

        for i in range(len(changed_depth_no)):
            vel_base_vp[changed_depth_no[i]-1]=vel_base_vp[changed_depth_no[i]-1]*outputdata[i]*modify_velocity_percent/label_range_vel+vel_base_vp[changed_depth_no[i]-1]

        depth_ind = get_index(vel_base_depth, disc_660)
        vel_base_depth[depth_ind[0]] = output_depth[0]*range_660/label_range_dep+disc_660
        vel_base_depth[depth_ind[0]+1] = output_thickness[0]*range_660/label_range_dep+range_660+vel_base_depth[depth_ind[0]]

        self.prediction_model_dic = {
            'no' : vel_base_model_dict_interpolation['no'],
            'depth' : vel_base_depth,
            'vp' : vel_base_vp,
            'vs' : vel_base_model_dict_interpolation['vs'],
            'ro' : vel_base_model_dict_interpolation['ro'],
            'qp' : vel_base_model_dict_interpolation['qp'],
            'qs' : vel_base_model_dict_interpolation['qs'],
        }

        return self.prediction_model_dic

    # write label prediction file
    def wr_vlb_pre_file(self,pre, prediction_model_path):
        self.prediction_model_dic=pre
        prediction_model = open(prediction_model_path, 'w')
        prediction_model.write('no   depth[km]   vp[km/s]   vs[km/s]   ro[g/cm^3]   qp   qs   \n')

        for i in range(len(self.prediction_model_dic['no'])):
            prediction_model.write(
                str(self.prediction_model_dic['no'][i])+'   '+
                str(self.prediction_model_dic['depth'][i])+'   '+
                str(self.prediction_model_dic['vp'][i])+'   '+
                str(self.prediction_model_dic['vs'][i])+'   '+
                str(self.prediction_model_dic['ro'][i])+'   '+
                str(self.prediction_model_dic['qp'][i])+'   '+
                str(self.prediction_model_dic['qs'][i])+'   '+
                '\n'
            )

        prediction_model.close()
