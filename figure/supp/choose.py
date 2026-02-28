


corr_path=''

corr_noise005_path=''
corr_noise010_path=''
corr_noise020_path=''
corr_noise025_path=''

corr_sta007_path=''
corr_sta015_path=''
corr_sta023_path=''
corr_sta039_path=''

loss_path=''

loss_noise005_path=''
loss_noise010_path=''
loss_noise020_path=''
loss_noise025_path=''

loss_sta007_path=''
loss_sta015_path=''
loss_sta023_path=''
loss_sta039_path=''


def get_corr(file_path, tag, dic):
    f = open(file_path,'r')
    f_c = f.readlines()
    f.close()

    for i in range(len(f_c)-1):
        nam = f_c[i].split('---')[0].replace('pre_model','').replace('.dat','')
        val = float(f_c[i].split(',')[-2])
        testset_dic[nam][tag]['corr']=val

def get_loss(file_path, tag, dic):
    f = open(file_path,'r')
    f_c = f.readlines()
    f.close()

    for i in range(len(f_c)):
        nam = f_c[i].split('---')[0].replace('pre_model','').replace('.dat','')
        val = float(f_c[i].split('---')[1].split(':')[1])
        testset_dic[nam][tag]['loss']=val


testset_dic = {}

f = open(corr_path,'r')
f_c = f.readlines()
f.close()

for i in range(len(f_c)-1):
    nam = f_c[i].split('---')[0].replace('pre_model','').replace('.dat','')
    testset_dic[nam]={
        'ori':{'loss':0, 'corr':1},
        'noise005':{'loss':0, 'corr':1},
        'noise010':{'loss':0, 'corr':1},
        'noise020':{'loss':0, 'corr':1},
        'noise025':{'loss':0, 'corr':1},
        'sta007':{'loss':0, 'corr':1},
        'sta015':{'loss':0, 'corr':1},
        'sta023':{'loss':0, 'corr':1},
        'sta039':{'loss':0, 'corr':1},
    }

get_corr(corr_path, 'ori', testset_dic)
get_corr(corr_noise005_path, 'noise005', testset_dic)
get_corr(corr_noise010_path, 'noise010', testset_dic)
get_corr(corr_noise020_path, 'noise020', testset_dic)
get_corr(corr_noise025_path, 'noise025', testset_dic)
get_corr(corr_sta007_path, 'sta007', testset_dic)
get_corr(corr_sta015_path, 'sta015', testset_dic)
get_corr(corr_sta023_path, 'sta023', testset_dic)
get_corr(corr_sta039_path, 'sta039', testset_dic)

get_loss(loss_path, 'ori', testset_dic)
get_loss(loss_noise005_path, 'noise005', testset_dic)
get_loss(loss_noise010_path, 'noise010', testset_dic)
get_loss(loss_noise020_path, 'noise020', testset_dic)
get_loss(loss_noise025_path, 'noise025', testset_dic)
get_loss(loss_sta007_path, 'sta007', testset_dic)
get_loss(loss_sta015_path, 'sta015', testset_dic)
get_loss(loss_sta023_path, 'sta023', testset_dic)
get_loss(loss_sta039_path, 'sta039', testset_dic)


consi_nam = []

for k, v in testset_dic.items():
    # if (v['noise005']['loss']<v['noise010']['loss']) and (v['noise010']['loss']<v['ori']['loss']) and (v['ori']['loss']<v['noise020']['loss']) and (v['noise020']['loss']<v['noise025']['loss']) and (v['noise005']['corr']>v['noise010']['corr']) and (v['noise010']['corr']>v['ori']['corr']) and (v['ori']['corr']>v['noise020']['corr']) and (v['noise020']['corr']>v['noise025']['corr']):
    if (v['sta039']['loss']<v['ori']['loss']) and (v['ori']['loss']<v['sta023']['loss']) and (v['sta023']['loss']<v['sta015']['loss']) and (v['sta015']['loss']<v['sta007']['loss']) and (v['sta039']['corr']>v['ori']['corr']) and (v['ori']['corr']>v['sta023']['corr']) and (v['sta023']['corr']>v['sta015']['corr']) and (v['sta015']['corr']>v['sta007']['corr']):
        print(k)





