import itchat
import numpy
import pandas
import matplotlib
import Levenshtein
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
from pandas import DataFrame


#登录
itchat.login()

#抓取好友信息
friends = itchat.get_friends(update=True)[0:]  #获取所有好友的个人信息
def get_var(var):
    variable = []
    for friend in friends:
        value = friend[var]
        variable.append(value)
    return variable

NickName = get_var('NickName')
Province = get_var('Province')

#绘制中国地图(台湾和中国)
font = {
    'family' : 'SimHel'
};
matplotlib.rc('font', **font);

flg = plt.figure()
ax = flg.add_subplot(111)

basemap = Basemap(
    llcrnrlon=72.558,
    llcrnrlat=17.159,
    urcrnrlon=135.77,
    urcrnrlat=55.561
)

chinaAdml = basemap.readshapefile(
    'D:\\Geany\\Python_work\\weixin_pachong\\gadm36_CHN_1',
    'china'
)

taiwanAdml = basemap.readshapefile(
    'D:\\Geany\\Python_work\\weixin_pachong\\gadm36_TWN_0',
    'taiwan'
)




data={
      'NickName':NickName,   #昵称
      'Province':Province    #省份
}

#将省份信息保存在表格中，并按省份统计
frame = DataFrame(data)
aggResult = frame.groupby(by=['Province'])['NickName'].agg(
                                         { '人数':numpy.size})

aggResult['好友数'] = aggResult.人数.astype(int)
aggResult['地区'] = aggResult.index

#将省份好友数的数据归一化
aggResult['scala'] = aggResult.好友数/aggResult.好友数.max()


print(aggResult)     #显示数据表格

#地图数据处理
mapData1 = pandas.DataFrame(basemap.china_info)  #将中国地图信息保存在表格中
mapData2 = pandas.DataFrame(basemap.taiwan_info)# 将台湾地图信息保存在表格中
mapDatas = [mapData1, mapData2]
mapData = pandas.concat(mapDatas)  # 合并中国和台湾地图信息

#得到地图省份信息
mapData = mapData.groupby(
          'NL_NAME_1')['NL_NAME_1'].agg({
               'NL_NAMW_1':numpy.size
          })

mapData['NL_NAME_1'] = mapData.index

print(mapData)

#将地图省份信息和好友省份信息进行相似度匹配，使其index列相同，再用merge函数合并2个表
#模糊匹配

suitSource = []
suitTarget = []
suitRatio = []

for aggResultIndex, aggResultRow in aggResult.iterrows():#获取每行index,row
    for mapDataIndex, mapDataRow in mapData.iterrows():
        if Levenshtein.ratio(mapDataRow['NL_NAME_1'], aggResultRow['地区']) != 0:
            suitSource.append(aggResultRow['地区'])
            suitTarget.append(mapDataRow['NL_NAME_1'])
            suitRatio.append(Levenshtein.ratio(mapDataRow['NL_NAME_1'], aggResultRow['地区']))

suitDataFrame = pandas.DataFrame({
        'NL_NAME_1':suitTarget,
        'suitRatio':suitRatio,
        'suitSource':suitSource
})

print(suitDataFrame)

#将匹配度最高的行保留
#排序
suitDataFrame = suitDataFrame.sort_values(
        ['suitSource', 'suitRatio'],
        ascending = [1, 0]
        )
       
#rnColumn = suitDataFrame.groupby(
#        'suitSource'
#        ).rank(
#                method = 'first'
#                numeric_only = True,
#                ascending = False
#                )
             
#suitDataFrame['rn'] = rnColumn;
suitDataFrame.drop_duplicates(subset='suitSource', keep='first', inplace=True)
print(suitDataFrame)

#合并数据框
aggResult = aggResult.merge(
        suitDataFrame,
        left_on = '地区',
        right_on = 'suitSource'
        )
print(aggResult)
del aggResult['suitRatio'];
del aggResult['suitSource'];


row = aggResult.loc[0]
print(row)
print('%%%%%%%%%%%%%%%%%')
row1 = aggResult.loc[1]
print(row1)


#定义涂色函数

for i in range(len(aggResult)):
    row = aggResult.loc[i]
    mainColor = (1, 0, 0) #row['scala'], 0)
    patches = []
    for info, shape in zip(basemap.china_info, basemap.china):
        if info['NL_NAME_1'] == row['NL_NAME_1']:
            patches.append(Polygon(numpy.array(shape), True))
    ax.add_collection(
        PatchCollection(
            patches, facecolor = mainColor,
            edgecolor = mainColor, linewidths = 1, zorder = 2
        )
    )
#apply(plotProvince, aggResult)   python3不支持apply
#plotProvince(**aggResult)
plt.show()


