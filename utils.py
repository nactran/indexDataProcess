import re
from config import thesaurus
import glob

#################
#Methods -Read Cnki Data
#################
def wordMerge(word):
    #词语规范化 规范化规则在 config.thesaurus 中设置
    if word in thesaurus:
        word = thesaurus[word]
    else:
        pass
    return word

def keyWordProcess(word_list):
    newlist = []
    for word in word_list:
        word = wordMerge(word)
        newlist.append(word)
    return newlist

def readText(article_list):
    '''
    for i in range(1,5):
        file = open("cnki/download"+str(i)+".txt")
    '''
    txt_filenames = glob.glob('cnki/*.txt')
    for filename in txt_filenames:
        file = open(filename,'r')
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

def readCnkiData():

    list = []
    readText(list)
    listProcess(list)
    #处理文件
    list = sortList(list)
    #把结果按年份排序
    return list

CnkiData = readCnkiData()

#############
#Execute Script
##############
if __name__ == '__main__':
    readCnkiData()
