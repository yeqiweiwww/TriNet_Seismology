

import numpy as np

from cal_corr_utils import read_seis_file, rebuild_seis_time_data, rebuild_seis_data_norm, get_rebuild_data_rebuild, get_rebuild_data_real


rebuild_real_reduce_time, rebuild_real_reduce_seis, _, _ = get_rebuild_data_real('../d/oridata/20090716/rebuild_data_real_v2.0_refine_use.dat')
rebuild_pre_rerun_reduce_time, rebuild_pre_rerun_reduce_seis, _, _ = get_rebuild_data_rebuild('../d/rerundata/20090716/rebuild_vp_seis_real_pre.dat')
rebuild_model_li_reduce_time, rebuild_model_li_reduce_seis, _, _ = get_rebuild_data_rebuild('../../pic7/d/oridata/li/rebuild_vp_seis_model_li_20080519.dat')


corr_all = [] 

for i in range(len(rebuild_pre_rerun_reduce_time)):
    corr_all.append(np.corrcoef(rebuild_pre_rerun_reduce_seis[i], rebuild_real_reduce_seis[i])[0][1])

pre_rerun_corr = np.mean(corr_all)
print('pre_rerun_corr',pre_rerun_corr)

################################

corr_all = []

for i in range(len(rebuild_model_li_reduce_time)):
    corr_all.append(np.corrcoef(rebuild_model_li_reduce_seis[i], rebuild_real_reduce_seis[i])[0][1])

model_li_corr = np.mean(corr_all)
print('model_li_corr',model_li_corr)

f = open('corr.dat','w')
f.write('model_li_corr:'+str(model_li_corr)+'\n')
f.write('pre_rerun_corr:'+str(pre_rerun_corr)+'\n')
f.close()
