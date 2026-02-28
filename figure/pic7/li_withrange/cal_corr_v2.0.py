

import numpy as np

from cal_corr_utils import read_seis_file, rebuild_seis_time_data, rebuild_seis_data_norm, get_rebuild_data_rebuild, get_rebuild_data_real


rebuild_model_li_pre_rerun_reduce_time, rebuild_model_li_pre_rerun_reduce_seis, _, _ = get_rebuild_data_rebuild('../d/rerundata/li/rebuild_vp_seis_real_pre.dat')
rebuild_model_li_reduce_time, rebuild_model_li_reduce_seis, _, _ = get_rebuild_data_rebuild('../d/oridata/li/rebuild_vp_seis_model_li_20080519.dat')
rebuild_ak135_pre_rerun_reduce_time, rebuild_ak135_pre_rerun_reduce_seis, _, _ = get_rebuild_data_rebuild('../d/rerundata/ak/seis_rebuild_data/rebuild_vp_seis_real_pre.dat')
rebuild_ak135_reduce_time, rebuild_ak135_li_reduce_seis, _, _ = get_rebuild_data_rebuild('../d/oridata/ak/rebuild_vp_seis_ak135_20080519.dat')

corr_all = []

for i in range(len(rebuild_model_li_reduce_time)):
    corr_all.append(np.corrcoef(rebuild_model_li_reduce_seis[i], rebuild_model_li_pre_rerun_reduce_seis[i])[0][1])

model_li_corr = np.mean(corr_all)
print('model_li_corr',model_li_corr)


corr_all = []

for i in range(len(rebuild_ak135_reduce_time)):
    corr_all.append(np.corrcoef(rebuild_ak135_li_reduce_seis[i], rebuild_ak135_pre_rerun_reduce_seis[i])[0][1])

ak135_corr = np.mean(corr_all)
print('ak135_corr',ak135_corr)

f = open('corr.dat','w')
f.write('model_li_corr:'+str(model_li_corr)+'\n')
f.write('ak135_corr:'+str(ak135_corr)+'\n')
f.close()
