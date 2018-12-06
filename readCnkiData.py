##############
#Dependencies
##############
import re
from collections import defaultdict
import matplotlib.pyplot as plt


#################
#Configurations
#################


#################
#Methods
#################
def readText(article_list):
    for i in range(1,5):
        file = open("cnki/download"+str(i)+".txt")
        while True:
            line = file.readline()
            if not line:
                break
            newArticle = re.match(r"RT\s(.*)",line)
            if(newArticle):
                tmpdic = dict().fromkeys(['ti', 'yr','kw','jf'])

            kw = re.match(r"K1\s(.*;)",line)
            if (kw):
                keywords = kw.group(1).split(';')
                tmpdic['kw'] = keywords[:-1]

            ti = re.match(r"T1\s(.*)",line)
            if(ti):
                tmpdic['ti'] = ti.group(1)

            jf  = re.match(r"JF\s(.*)",line)
            if(jf):
                tmpdic['jf'] = jf.group(1)

            yr =re.match(r"YR\s(\d*)",line)
            if(yr):
                tmpdic['yr'] = int(yr.group(1))
            endOfArticle = re.match(r"DS\s(.*)",line)
            if(endOfArticle):
                article_list.append(tmpdic)
        file.close()
    return article_list

def wordMerge(word):
    if word == '教育领域':
        word = '教育'
    elif word == '教育资源库':
        word = '教育资源'
    elif word == '教学质量' or word == '教学评价' or word == '教育评价':
        word = '教学评估'
    elif word == '教学模式' or word == '教学改革':
        word = '教学'
    elif word == '现代远程教育' or word == '网络教育' or word == '在线教育' or word == '远程开放教育'or word == '网络课程'or word == '网络教学':
        word = '远程教育'
    elif word == 'Web数据挖掘':
        word = 'Web挖掘'
    elif word == '个性化推荐' or word == '个性化教育' or word == '个性化教学' or word == '个性化服务' or word =='个性化学习系统' or word == '个性化学习':
        word = '个性化'
    elif word == '高校':
        word = '高校教育'
    elif word == '高职教育'or word == '高职院校':
        word = '职业教育'
    elif word == '高校管理'or word == '教学管理':
        word = '教育管理'
    elif word == '大数据时代' or word == '大数据技术' or word == '大数据挖掘':
        word = '大数据'
    elif word == '教育决策支持系统' or word == '决策支持系统':
        word = '决策支持'
    elif word == '决策树算法':
        word = '决策树'
    elif word == '关联规则挖掘':
        word = '关联规则'
    elif word == '数据可视化':
        word = '可视化'
    elif word == '网络学习行为分析' or word == '学习行为分析' or word == '网络学习行为':
        word = '学习行为'
    elif word == '自适应' or word =='自适应学习系统':
        word = '自适应学习'
    else:
        pass
    return word

def keyWordProcess(word_list):
    newlist = []
    for word in word_list:
        word = wordMerge(word)
        newlist.append(word)
    return newlist

def listProcess(article_list):
    preArticleYear = 9999
    #默认空缺值
    for article in article_list:
        if not article['yr']:
            article['yr'] = preArticleYear
            #填补空缺值
        preArticleYear = article['yr']
        if not article['kw']:
            article['kw'] = ['NoKeyword']
        else :
            article['kw'] = keyWordProcess(article['kw'])
            #清洗关键词
        if not article['jf']:
            article['jf'] = 'NoJournal'
    return article_list

def sortList(article_list):
    #对文章按照进行排序
    sortedList = sorted(article_list,key = lambda x:x['yr'])
    return sortedList

def getYears(article_list):
    #返回一个按时间排序的年份列表
    years = [article['yr'] for article in article_list]
    years = list(set(years))
    sorted_years = sorted(years,key = lambda x:x)
    return sorted_years

def getJournal(article_list):
    jncountdic = dict()
    for article in article_list:
        if re.search('计算机',article['jf']):
            continue
        elif article['jf'] in jncountdic:
            jncountdic[article['jf']] += 1
        else:
            jncountdic[article['jf']] = 1
    jncountdic = sorted(jncountdic.items(),key = lambda item:item[1],reverse=False)
    labels = [item[0] for item in jncountdic ]
    sizes = [item[1] for item in jncountdic ]
    labels = labels[-50:]

    sizes = sizes[-50:]
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots()
    ax.barh(labels, sizes)
    fig.set_size_inches(9, 12)
    plt.tick_params(axis='both',labelsize= 7)
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS'] # 指定默认字体
    plt.show()
    return jncountdic




#####################
#main function
#####################
def readCnikData():

    list = []
    readText(list)
    listProcess(list)
    #处理文件
    list = sortList(list)
    #把结果按年份排序




    #print(allWordList[:48])
    #coWordMatrix = generateCoWordMatrix(allWordList[:48],list)
    #前47个高频

    return list

#############
#Execute Script
##############
if __name__ == '__main__':
    readCnikData()
