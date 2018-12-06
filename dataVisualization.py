##############
#Dependencies
##############
import matplotlib.pyplot as plt
import readCnkiData
import re
#################
#Methods
#################
def showArticleByYear():
    article_list = readCnkiData.readCnikData()
    #数据可视化-历年载文折线图
    years = readCnkiData.getYears(article_list)
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

def getKeyWordByPeriod():
    article_list = readCnkiData.readCnikData()
    firstPeriod = dict() #2000~2011
    secondPeriod = dict() #2012～2018
    years = readCnkiData.getYears(article_list)
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
        else:
            continue

    firstPeriod = sorted(firstPeriod.items(),key = lambda item:item[1],reverse=False)
    secondPeriod = sorted(secondPeriod.items(),key = lambda item:item[1],reverse=False)
    #thridPeriod = sorted(thridPeriod.items(),key = lambda item:item[1],reverse=False)
    periodList = [firstPeriod,secondPeriod]
    return periodList

def showKeyWord():
    periodList = getKeyWordByPeriod()
    i = 1
    for period in periodList:
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

def showJournal():
    article_list = readCnkiData.readCnikData()
    jncountdic = dict()
    for article in article_list:
        if article['jf'] == 'NoJournal':
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

#############
#Execute Script
##############
if __name__ == '__main__':
    showArticleByYear()
    showKeyWord()
    showJournal()
