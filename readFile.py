import sys
import numpy as np
from os import listdir
from os.path import isfile, join

def readFile(filePath):
    sentence = []
    sentences = []
    with open(filePath,'r') as file:
        for line in file:
            if ((not line.strip()) and (sentence != [])):
                sentences.append(sentence)
                sentence = []
            if (line.split() != []) :
                word,tag,chunkTag = line.split()
                word = word.upper()
                sentence.append((word,tag,chunkTag))
    sentences.append(sentence)
    return sentences

def getIndices(sentences):
    uniqWords = set()
    uniqTags = set()
    for sentence in sentences:
        for word,tag,_ in sentence:
            uniqWords.add(word)
            uniqTags.add(tag)

    map_symbol_index = {v: k for k, v in dict(enumerate(uniqWords)).items()}
    map_index_symbol =  {v: k for k, v in map_symbol_index.items()}
    map_pos_index = {v: k for k, v in dict(enumerate(uniqTags)).items()}
    map_index_pos =  {v: k for k, v in map_pos_index.items()}
    return map_index_pos,map_pos_index,map_index_symbol,map_symbol_index

def buildTranMat(map_index_pos,map_index_symbol,map_pos_index,dict_weights):
    N = len(map_index_pos)
    M = len(map_index_symbol)

    TPM = np.zeros(shape = (N * M, N), dtype = float)

    #format of input : dict(tag,[(feauture,weight)])
    dict_weights = {}
    uniqTags = list(map_index_pos.values())

    for x in uniqTags:
        weights = list((np.random.uniform(0,1,size =5)))
        dict_weights[x] = weights
        #print(x," ---> ",dict_weights[x])

    numFeautures = len((list(dict_weights.values())[0]))

    for pos_tag in uniqTags:
        for k in range(0, M):				# Current observation
            for j in range(0, N):
                i = map_pos_index[pos_tag]
            	# Current/target state
                TPM[i*M+k][j] = float(0)
                word = map_index_symbol[k]
                tag = map_index_pos[j]
                for l in range(0,numFeautures):
                    tempW = dict_weights[pos_tag][l]
                    #print (pos_tag ," ",l," ---> "," ",tempW)
                    TPM[i*M+k][j] += tempW * 1# insert feauture function here
                TPM[i*M+k][j] = np.exp(TPM[i*M+k][j])

            row_sum = np.sum(TPM[i*M+k])
            for j in range(0, N):			# Current/target state
                TPM[i*M+k][j] = TPM[i*M+k][j] / row_sum


    return TPM


if __name__ == '__main__':
    sentences = readFile('sample.txt')
    '''for x in sentences:
        for y in x:
            print(y[0].decode('utf-8'),end =' ')
        print("\n\n")'''
    map_index_pos,map_pos_index,map_index_symbol,map_symbol_index = getIndices(sentences)
    sampleDict = {} # dict(tag:[weights]) list of weights should be in order of feautures
    mat = buildTranMat(map_index_pos,map_index_symbol,map_pos_index,sampleDict)
    #print(mat)
