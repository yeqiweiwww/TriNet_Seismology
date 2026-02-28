

# pygmt=0.14.0
import pygmt

from copy import deepcopy
import pandas as pd

pygmt.config(GMT_DATA_SERVER="https://mirror.nju.edu.cn/gmtdata/")

region_map = [90, 140, 25, 50]

fig = pygmt.Figure()

pygmt.makecpt(cmap="globe", series=[-10000, 6000])

fig.basemap(region=region_map, projection="M12c", frame="af")

grid_map = pygmt.datasets.load_earth_relief(resolution="15s", region=region_map)

fig.grdimage(grid=grid_map)

fig.colorbar(

    frame=["x+lElevation", "y+lm"],

)

##################################
f = open('./20080519_sta.info','r')
f_c = f.readlines()
f.close()

sta_nam_2008 = []
sta_stla_2008 = []
sta_stlo_2008 = []

for i in range(len(f_c)):
    sta_temp = f_c[i].replace('\n','').split()
    sta_nam_2008.append(sta_temp[0])
    sta_stla_2008.append(float(sta_temp[1]))
    sta_stlo_2008.append(float(sta_temp[2]))

f = open('./20090716_sta.info','r')
f_c = f.readlines()
f.close()

sta_nam_2009 = []
sta_stla_2009 = []
sta_stlo_2009 = []

for i in range(len(f_c)):
    sta_temp = f_c[i].replace('\n','').split()
    sta_nam_2009.append(sta_temp[0])
    sta_stla_2009.append(float(sta_temp[1]))
    sta_stlo_2009.append(float(sta_temp[2]))

sta_nam_draw = deepcopy(sta_nam_2008)
sta_stla_draw = deepcopy(sta_stla_2008)
sta_stlo_draw = deepcopy(sta_stlo_2008)

for i in range(len(sta_nam_2009)):
    if sta_nam_2009[i] in sta_nam_draw:
        continue
    else:
        sta_nam_draw.append(sta_nam_2009[i])
        sta_stla_draw.append(sta_stla_2009[i])
        sta_stlo_draw.append(sta_stlo_2009[i])

event1_info = {
    'event_name': '20080519',
    "mrr": 0.055,  # 径向分量
    "mtt": 1.410,  # 横向分量
    "mff": -1.460,  # 前向分量
    "mrt": 1.290,  # 径向-横向分量
    "mrf": -2.580,  # 径向-前向分量
    "mtf": 2.410,  # 横向-前向分量
    "exponent": 24,  # 指数项
    "longitude": 131.87,  # 震中经度
    "latitude": 42.50,  # 震中纬度
    "plot_longitude": 129.87,
    "plot_latitude": 43.50,
}
event2_info = {
    'event_name': '20090716',
    "mrr": -0.013,  # 径向分量
    "mtt": 0.76,  # 横向分量
    "mff": -0.748,  # 前向分量
    "mrt": 0.339,  # 径向-横向分量
    "mrf": -0.524,  # 径向-前向分量
    "mtf": -0.448,  # 横向-前向分量
    "exponent": 24,  # 指数项
    "longitude": 133.00,   # 震中经度
    "latitude": 42.37,   # 震中纬度
    "plot_longitude": 135.00,
    "plot_latitude": 43.37,
}

##################################

for i in range(len(sta_nam_2008)):
    fig.plot(x=[sta_stlo_2008[i],event1_info['longitude']], y=[sta_stla_2008[i],event1_info['latitude']],pen="0.5p,blue")
for i in range(len(sta_nam_2009)):
    fig.plot(x=[sta_stlo_2009[i],event2_info['longitude']], y=[sta_stla_2009[i],event2_info['latitude']],pen="0.5p,blue")


fig.plot(x=sta_stlo_draw, y=sta_stla_draw, style="t0.3c", fill='red', pen='1p,black')

fig.meca(
    spec=event1_info,
    scale="0.5c+o-0.05/0.2+f8p",
    labelbox=True,
    offset="+sa0.3c+p0.7p,black",
    compressionfill="red",
    extensionfill="white",
    pen="0.5p,black,solid",
)

fig.meca(
    spec=event2_info,
    scale="0.5c+o0.05/0.2+f8p",
    labelbox=True,
    offset="+sa0.3c+p0.7p,black",
    compressionfill="red",
    extensionfill="white",
    pen="0.5p,black,solid",
)

# fig.savefig('pic6_v2.0.jpg')
fig.savefig('pic6_v2.0.pdf')