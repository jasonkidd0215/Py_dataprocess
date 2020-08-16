import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)
pd.set_option('display.max_columns', 1000000)   # 可以在大数据量下，没有省略号
pd.set_option('display.max_rows', 1000000)
pd.set_option('display.max_colwidth', 1000000)
pd.set_option('display.width', 1000000)

df = pd.read_excel("data.xlsx")


##############################到期分布###########################
print("===============================交收本息==========================================")
dff_JSBX=pd.pivot_table(df,index=['资金交收日'],columns=['品种'],
                    values=df.columns[11],#交收本息
                    aggfunc=np.sum
                    )
dff_JSBX = dff_JSBX.fillna(value=0)
dff_JSBX['Col_sum'] = dff_JSBX.apply(lambda x: x.sum(), axis=1)
dff_JSBX_plot = dff_JSBX.iloc[0:,3:4]
dff_JSBX_plot.plot(kind='bar',figsize=(20,10))
plt.ticklabel_format(style='plain',axis='y')
plt.rcParams['font.sans-serif']=['SimHei']
font1 = {'size':23}
legend = plt.legend(["总计"],prop=font1)
plt.tick_params(labelsize=15)
plt.xlabel('交收日期',size=15)
plt.ylabel('交收本息（元）',size=15)
plt.show()

print("===============================到期本息==========================================")
dff_DQBX=pd.pivot_table(df,index=['产品到期日'],columns=['品种'],
                    values=df.columns[10],#到期本息
                    aggfunc=np.sum
                    )
dff_DQBX = dff_DQBX.fillna(value=0)
dff_DQBX['Col_sum'] = dff_DQBX.apply(lambda x: x.sum(), axis=1)
dff_DQBX_plot = dff_DQBX.iloc[0:,3:4]
dff_DQBX_plot.plot(kind='bar',figsize=(20,10))
plt.ticklabel_format(style='plain',axis='y')
plt.rcParams['font.sans-serif']=['SimHei']
font1 = {'size':23}
legend = plt.legend(["总计"],prop=font1)
plt.tick_params(labelsize=15)
plt.xlabel('到期日期',size=15)
plt.ylabel('到期本息（元）',size=15)
plt.show()

print("===============================到期续作本金==========================================")
dff_DQXZ=pd.pivot_table(df,index=['产品到期日'],columns=['品种'],
                    values=df.columns[8],#到期本息
                    aggfunc=np.sum
                    )
dff_DQXZ = dff_DQXZ.fillna(value=0)
dff_DQXZ['Col_sum'] = dff_DQXZ.apply(lambda x: x.sum(), axis=1)
dff_DQXZ_plot = dff_DQXZ.iloc[0:,3:4]
dff_DQXZ_plot.plot(kind='bar',figsize=(20,10))
plt.ticklabel_format(style='plain',axis='y')
plt.rcParams['font.sans-serif']=['SimHei']
font1 = {'size':23}
legend = plt.legend(["总计"],prop=font1)
plt.tick_params(labelsize=15)
plt.xlabel('到期日期',size=15)
plt.ylabel('到期续作本金（元）',size=15)
plt.show()


##############################客户续作明细############################
print("===================================客户续作明细==================================")
dff=pd.pivot_table(df,index=['资金交收日','客户ID'],columns=['品种'],
                   values=df.columns[8],#8-续作本金，11-交收本息
                   aggfunc=np.sum
                   )
dff = dff.fillna(value=0)

dff2=pd.pivot_table(df,index=['资金交收日'],columns=['品种'],
                    values=df.columns[8],
                    aggfunc=np.sum
                    )
dff2 = dff2.fillna(value=0)

j=0
for i in range(0,len(dff.index)):
    if dff.index[i][0]==dff2.index[j]:
        dff_temp1 = dff[0:i]
        dff_temp2 = dff[i:]
        dff = dff_temp1.append(dff2[j:j+1], ignore_index = False).append(dff_temp2, ignore_index = False)
        j+=1
dff.index.name = '资金交收日     客户ID'
dff['总计'] = dff.apply(lambda x: x.sum(), axis=1)
display(dff)

##########################客户集中度####################################
Show_count = 100
print("======================================客户集中度（前",Show_count,"）=================================")
dff_KHJZD=pd.pivot_table(df,index=['客户ID'],columns=['品种'],
                    values=df.columns[8],#到期本息
                    aggfunc=np.sum
                    )
dff_KHJZD = dff_KHJZD.fillna(value=0)
dff_KHJZD['总计'] = dff_KHJZD.apply(lambda x: x.sum(), axis=1)

Whole_sum = dff_KHJZD['总计'].sum()
dff_KHJZD['集中度'] = dff_KHJZD['总计'].map(lambda x: '%.5f%%' % ((x/Whole_sum)*100))
dff_KHJZD = dff_KHJZD.sort_values(['总计'], ascending = False)
display(dff_KHJZD)

dff_KHJZD_plot = dff_KHJZD.iloc[0:,3:4]
dff_KHJZD_plot = dff_KHJZD_plot[0:Show_count]
dff_KHJZD_plot.plot(kind='bar',figsize=(20,10))
plt.ticklabel_format(style='plain',axis='y')
plt.rcParams['font.sans-serif']=['SimHei']
font1 = {'size':23}
legend = plt.legend(["客户集中度"],prop=font1)
plt.tick_params(labelsize=8)
plt.xlabel('客户ID',size=15)
plt.ylabel('总计',size=15)
plt.show()

print('总存量:',Whole_sum)
print('前五客户集中度:', (dff_KHJZD['总计'][0:5].sum()/Whole_sum)*100,'%')
print('总客户数:',len(dff_KHJZD))
