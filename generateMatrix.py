##############
#Dependencies
##############
import math
from readCnkiData import readCnikData
import csv

#################
#Configurations
#################
numOfFreqWord = 53
outPutPath = 'output/'

#################
#Methods
#################
def addWordIntoDict(word,dict):

    if word in dict:
        dict[word] += 1
    else:
        dict[word] = 1

def countKeyWord():
    article_list = readCnikData()
    allPeriod = dict()
    for article in article_list:
        for kw in set(article['kw']):
            if kw == '数据挖掘' or kw == '教育' or kw =='NoKeyword':
                continue
            else:
                addWordIntoDict(kw,allPeriod)

    allPeriod = sorted(allPeriod.items(),key = lambda item:item[1],reverse=True)
    return allPeriod

def generateWordList(end = 48):
    allWordList = countKeyWord()
    #得到的是个集合数列
    word_list = [i[0] for i in allWordList[:end] ]
    return word_list

def generateWordIndex(end = 48):
    word_list = generateWordList(end)
    wordIndex = dict()
    count = 0
    for word in word_list:
        wordIndex[word] = count
        count += 1
    return wordIndex

def generateCoWordMatrix(length = 48):
    article_list = readCnikData()
    word_list = generateWordList(length)
    coWordMatrix = []

    wordIndex = generateWordIndex(length)
    #生成一个高频词对应下标的字典

    for i in range(0,len(wordIndex)):
        #初始化共词矩阵
        coWordMatrix.append([])
        for j in range (0,len(wordIndex)):
            coWordMatrix[i].append(0)
    for article in article_list:
        for kw1 in set(article['kw']):
            if kw1 not in word_list:
                #不是高频词
                continue
            for kw2 in set(article['kw']):
                if kw2 not in word_list:
                    continue
                index1 = wordIndex[kw1]
                index2 = wordIndex[kw2]
                coWordMatrix[index1][index2] += 1

    return coWordMatrix

def generateSimilarDifferentMatrix(coWordMatrix):
    similarMatrix = []
    differentMatrix = []
    for i in range(0,len(coWordMatrix)):
        #初始化相似矩阵
        similarMatrix.append([])
        for j in range (0,len(coWordMatrix)):
            ochiia = coWordMatrix[i][j]/(math.sqrt(coWordMatrix[i][i])*math.sqrt(coWordMatrix[j][j]))
            #计算ochiia系数
            similarMatrix[i].append(round(ochiia+0.00000000000000001,4))

    for i in range(0,len(coWordMatrix)):
        #初始化相似矩阵
        differentMatrix.append([])
        for j in range (0,len(coWordMatrix)):
            differentMatrix[i].append(1-similarMatrix[i][j])
    return similarMatrix, differentMatrix

def saveAsCsv(matrix,filename,rowName = []):
    csvfile = open(outPutPath+filename+'.csv','w',encoding='utf-8')
    writer = csv.writer(csvfile)
    if(rowName):
        writer.writerow(rowName)
    writer.writerows(matrix)
    csvfile.close()

#############
#Execute Script
##############
if __name__ == '__main__':
    wordList = generateWordList(numOfFreqWord)
    cwm = generateCoWordMatrix(numOfFreqWord)
    sm, dm= generateSimilarDifferentMatrix(cwm)

    saveAsCsv(sm,'similar',wordList)
    saveAsCsv(dm,'different',wordList)


    wordIndex = generateWordIndex(numOfFreqWord)
    print(wordIndex)

