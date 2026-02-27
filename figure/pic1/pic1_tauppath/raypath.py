

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


num = 5000

factor = 1

rad_ear = 6371
rad_0 = rad_ear - 0
rad_410 = rad_ear - 410
rad_660 = rad_ear - 660

rad_0 = rad_0**factor
rad_410 = rad_410**factor
rad_660 = rad_660**factor

dis_0_y = np.full(num, rad_0)
dis_410_y = np.full(num, rad_410)
dis_660_y = np.full(num, rad_660)


dis_0_x = np.linspace(75/180*np.pi, 105/180*np.pi, num)
dis_410_x = np.linspace(75/180*np.pi, 105/180*np.pi, num)
dis_660_x = np.linspace(75/180*np.pi, 105/180*np.pi, num)


f = pd.read_csv('p1.dat', sep='\s+', header=None)
ray_path_1_x = f[0].tolist()
for i in range(len(ray_path_1_x)):
    ray_path_1_x[i] = (-ray_path_1_x[i]+100)/180*np.pi
ray_path_1_y = f[1].tolist()
for i in range(len(ray_path_1_y)):
    ray_path_1_y[i] = ray_path_1_y[i]**factor


f = pd.read_csv('p2.dat', sep='\s+', header=None)
ray_path_2_x = f[0].tolist()
for i in range(len(ray_path_2_x)):
    ray_path_2_x[i] = (-ray_path_2_x[i]+100)/180*np.pi
ray_path_2_y = f[1].tolist()
for i in range(len(ray_path_2_y)):
    ray_path_2_y[i] = ray_path_2_y[i]**factor

f = pd.read_csv('p3.dat', sep='\s+', header=None)
ray_path_3_x = f[0].tolist()
for i in range(len(ray_path_3_x)):
    ray_path_3_x[i] = (-ray_path_3_x[i]+100)/180*np.pi
ray_path_3_y = f[1].tolist()
for i in range(len(ray_path_3_y)):
    ray_path_3_y[i] = ray_path_3_y[i]**factor


sta_line = 800000
sta_angles_1 = (-20+100)/180*np.pi
sta_rad_1 = rad_0

sta_rad_2 = np.sqrt(sta_line**2 + rad_0**2 - 2*sta_line*rad_0*np.cos(150/180*np.pi))
dis_angle = np.arccos((sta_rad_2**2 + rad_0**2 - sta_line**2)/(2*sta_rad_2*rad_0))


sta_angles_2 = sta_angles_1 - dis_angle
sta_angles_3 = sta_angles_1 + dis_angle

sta_rad_3 = sta_rad_2


plt.figure(figsize=(12,12), dpi=1200)

ax = plt.subplot(111, projection='polar')

ax.plot(dis_0_x, dis_0_y, color='black', linewidth=2)
ax.plot(dis_410_x, dis_410_y, color='black', linewidth=2)
ax.plot(dis_660_x, dis_660_y, color='black', linewidth=2)


ax.plot(ray_path_1_x, ray_path_1_y, color=(255/255,38/255,0/255), linewidth=3, alpha=0.7, zorder=3)
ax.plot(ray_path_2_x, ray_path_2_y, color=(0/255,194/255,0/255), linewidth=3, alpha=0.7, zorder=1)
ax.plot(ray_path_3_x, ray_path_3_y, color=(0/255,119/255,255/255), linewidth=3, alpha=0.7, zorder=2)

ax.scatter(100/180*np.pi, (rad_ear-519)**factor, marker='*', c='black', s=150, zorder=4)

ax.fill([sta_angles_1, sta_angles_2, sta_angles_3], [sta_rad_1, sta_rad_2, sta_rad_3], color='black', zorder=4)

ax.set_xlim(70/180*np.pi, 110/180*np.pi)
ax.set_ylim(0, (rad_ear+100)**factor)


# ax.set_yticks((dis_0_y[0], dis_410_y[0], dis_660_y[0]))
# ax.set_yticklabels(('Surface', '410', '660'),fontsize=24)

# ax.text(70/180*np.pi, dis_0_y[0], 'Surface', horizontalalignment='left', verticalalignment='center')



ax.set_axis_off()
plt.savefig('raypath.svg')
