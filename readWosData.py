##############
#Dependencies
##############
import re
import csv
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

#################
#Configurations
#################


#################
#Methods
#################
def readCsvData(article_list):
    with open('uForeignPapers.csv','r',encoding='iso-8859-1') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            tmpdict = dict()
            #必须放循环里面 不然只会插入最后一个dict
            tmpdict['ti'] = row[8]
            tmpdict['de'] = row[19]
            tmpdict['id'] = row[20]
            if row[44] == '5-Jul':
                tmpdict['py'] = '2013'
                #年份格式错误 只在2013年里有过
            else:
                tmpdict['py'] = row[44]
            article_list.append(tmpdict)
    return article_list[1:-5]

def sortList(article_list):
    #对文章按照进行排序
    sortedList = sorted(article_list,key = lambda x:x['py'])
    return sortedList

def keyWordProcess(article_list):
    for article in article_list:
        article['kw'] = []
        if not article['id'] and not article['de']:
            continue
        else:
            if article['id']:
                for word in article['id'].split(';'):
                    word = word.strip()
                    if word == 'SYSTEMS':
                        word = word.rstrip('S')
                    article['kw'].append(word)
            if article['de']:
                for word in article['de'].split(';'):
                    word = word.strip()
                    word = word.upper()
                    if word == 'SYSTEMS':
                        word = word.rstrip('S')
                    if word not in article['kw']:
                        article['kw'].append(word)
    return article_list

def getYears(article_list):
    #返回一个按时间排序的年份列表
    years = [article['py'] for article in article_list]
    years = list(set(years))
    sorted_years = sorted(years,key = lambda x:x)
    #一定要排序，不然顺序是乱的
    #具体原因未知
    return sorted_years

def showArticleByYear(article_list):
    #数据可视化-历年载文折线图
    yl = getYears(article_list)
    #获取年份列表
    countdic = dict().fromkeys(yl)
    #初始化字典
    for article in article_list:
        #统计载文量
        if(not countdic[article['py']]):
            countdic[article['py']] = 1
        else:
            countdic[article['py']] += 1
    #yl = [key for key in countdic]
    #横轴-年份
    articlenum = [countdic[key] for key in countdic ]
    #纵轴-每年发文数

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

def getKeyWordByPeriod(article_list):
    firstPeriod = dict() #1997~2011
    secondPeriod = dict() #2012～2018
    allPeriod = dict() #for all
    years = getYears(article_list)
    periodList = [years[:15],years[15:]]
    for article in article_list:
        if article['py'] in periodList[0]:
            #isFirstPeriod
            for kw in article['kw']:
                if kw == 'DATA MINING' or kw =='EDUCATION':
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

        elif article['py'] in periodList[1]:
            #isSecondPeriod
            for kw in article['kw']:
                if kw == 'DATA MINING' or kw =='EDUCATION':
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
    showKeyWord(periodList)
    return allPeriod

def showKeyWord(periodList):
    i = 1
    for period in periodList:
        print('#PERIOD '+str(i))
        for word in period:
            print(word[0]+" "+str(word[1]))
        labels = [item[0] for item in period ]
        sizes = [item[1] for item in period ]
        labels = labels[-23:]
        sizes = sizes[-23:]
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
    list = readCsvData(list)
    list = sortList(list)
    list = keyWordProcess(list)
    #showArticleByYear(list)
    getKeyWordByPeriod(list)



#############
#Execute Script
##############
if __name__ == '__main__':
    main()


