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

def listProcess(article_list):
    preArticleYear = 9999
    #默认空缺值
    for article in article_list:
        if article['yr'] == 2000:
            print (article)
        if not article['yr']:
            article['yr'] = preArticleYear
            #填补空缺值
        preArticleYear = article['yr']
        if not article['kw']:
            article['kw'] = ['NoKeyword']
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

def showArticleByYear(article_list):
    #数据可视化-历年载文折线图
    years = getYears(article_list)
    yl = [str(yr) for yr in years]
    #年份列表
    countdic = dict().fromkeys(yl)
    for article in article_list:
        if(not countdic[str(article['yr'])]):
            countdic[str(article['yr'])] = 1
        else:
            countdic[str(article['yr'])] += 1
    yl = [key for key in countdic]
    articlenum = [countdic[key] for key in countdic ]
    #每年发文数
    plt.plot(yl, articlenum, linewidth= 3)
    plt.title("Trends", fontsize=24)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Papers", fontsize=14)
    # 设置刻度标记的大小
    plt.tick_params(axis='both',labelsize= 8)
    #设置底部数字标签

    x = yl
    y=articlenum
    for a,b in zip(x,y):
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=12)
    #设置每个项目的标签
    plt.grid(ls='--')
    #设置网格
    plt.show()

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

def getKeyWordByPeriod(article_list):

    firstPeriod = dict() #2000~2011
    secondPeriod = dict() #2012～2018
    allPeriod = dict() #for all
    years = getYears(article_list)
    periodList = [years[:12],years[12:]]
    for article in article_list:
        if article['yr'] in periodList[0]:
            #isFirstPeriod
            for kw in article['kw']:
                if kw == '数据挖掘' or kw =='NoKeyword':
                    continue
                else:
                    if kw in firstPeriod:
                        firstPeriod[kw] += 1
                    else:
                        firstPeriod[kw] = 1
                    if kw in allPeriod:
                        allPeriod[kw] += 1
                    else:
                        allPeriod[kw] = 1

        elif article['yr'] in periodList[1]:
            #isSecondPeriod
            for kw in article['kw']:
                if kw == '数据挖掘' or kw =='NoKeyword':
                    continue
                else:
                    if kw in secondPeriod:
                        secondPeriod[kw] += 1
                    else:
                        secondPeriod[kw] = 1
                    if kw in allPeriod:
                        allPeriod[kw] += 1
                    else:
                        allPeriod[kw] = 1
        else:
            continue

    firstPeriod = sorted(firstPeriod.items(),key = lambda item:item[1],reverse=False)
    secondPeriod = sorted(secondPeriod.items(),key = lambda item:item[1],reverse=False)
    #thridPeriod = sorted(thridPeriod.items(),key = lambda item:item[1],reverse=False)
    allPeriod = sorted(allPeriod.items(),key = lambda item:item[1],reverse=True)
    periodList = [firstPeriod,secondPeriod]
    return periodList, allPeriod

def showKeyWord(periodList):
    i = 1
    for period in periodList:
        print('#PERIOD '+str(i))
        for word in period:
            print(word[0]+" "+str(word[1]))
        labels = [item[0] for item in period ]
        sizes = [item[1] for item in period ]
        labels = labels[-29:]
        sizes = sizes[-29:]
        plt.style.use('fivethirtyeight')
        fig, ax = plt.subplots()
        ax.barh(labels, sizes)
        fig.set_size_inches(9, 12)
        plt.title("Keywords Ranking " + str(i), fontsize=18)
        plt.tick_params(axis='both',labelsize= 7)
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
        # 指定默认字体
        plt.show()
        i += 1





#####################
#main function
#####################
def main():

    list = []
    readText(list)
    listProcess(list)
    #处理文件
    sorted_list = sortList(list)
    #把结果按年份排序

    showArticleByYear(sorted_list)
    #jd = getJournal(list)
    #print(jd)

    periodList,allPeriod = getKeyWordByPeriod(list)
    showKeyWord(periodList)

    exit()

#############
#Execute Script
##############
if __name__ == '__main__':
    main()
