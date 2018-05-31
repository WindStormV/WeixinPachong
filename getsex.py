import itchat
import matplotlib.pyplot as plt

itchat.auto_login()
friends=itchat.get_friends(update=True)[0:]
user_nickname = friends[0]['NickName']

#获取性别
sex = {}   # 保存性别的字典


for friend in friends[1:]: # 不包括自己
	s = friend['Sex']
	if s == 1:
		sex['male'] = sex.get('male', 0) + 1   # get返回指定键值，不存在然后第二个参数
	elif s == 2:
		sex['female'] = sex.get('female', 0) + 1
	else:
		sex['unknown'] = sex.get('unknown', 0) + 1


sex_sum = len(friends) - 1

print("微信好友男性比例：%.2f%%" % (sex['male'] / sex_sum * 100) + '\n' +
      "微信好友女性比例：%.2f%%" % (sex['female'] / sex_sum * 100) + '\n' +
      "未知性别比例：%.2f%%" % (sex['female'] / sex_sum * 100))

labels = ['male', 'female', 'unknown']
fracs = [sex['male'], sex['female'], sex['unknown']]
plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
plt.pie(x=fracs, labels=labels,autopct='%3.1f %%',shadow=True,
        labeldistance=1.1, startangle = 90,pctdistance = 0.6)
#plt.title('%s微信好友性别比例'%user_nickname)
plt.show()

#####下一个功能

provinces = {}

for friend in friends[1:]: #不包括自己
	province = friend['Province']
	if province in provinces.keys():
		provinces[province] += 1
	else:
		provinces[province] = 1
print(provinces)
