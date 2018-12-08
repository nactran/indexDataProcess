import json
import re
from generateMatrix import generateWordList
def makeJsonFile(fileName,outputFilename = 'output/record.json'):
    #处理SPSS输出的坐标
    data = []
    for line in open(fileName):
        m = re.findall(r'-?\d?\.\d*', line)
        if(m):
            x = float(m[0])
            y = float(m[1])
            data.append([x,y])
        else:
            print('Can not match x y ')
            return None
    wordlist = generateWordList(len(data))
    for count in range(0,len(data)):
        data[count].append(wordlist[count])
    with open(outputFilename,"w") as f:
        json.dump(data,f,ensure_ascii=False)
    return data


#############
#Execute Script
##############
if __name__ == '__main__':
    file_name = 'output/Cordination.txt'
    makeJsonFile(file_name)
