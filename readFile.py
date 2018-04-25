import sys
#import numpy as np
from os import listdir
from os.path import isfile, join

def readFile(filePath):
    sentence = []
    sentences = []
    with open(filePath,'rb') as file:
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

def getCount(sentences):
    uniqWords = set()
    uniqTags = set()
    for sentence in sentences:
        for word,tag,_ in sentence:
            uniqWords.add(word)
            uniqTags.add(tag)

    map_symbol_index = {v: k for k, v in dict(enumerate(uniqWords)).items()}
    print(map_symbol_index)
    map_index_symbol =  {v: k for k, v in map_symbol_index.items()}
    print("\n\n")
    print(map_index_symbol)
    return uniqWords,uniqTags


if __name__ == '__main__':
    sentences = readFile('sample.txt')
    '''for x in sentences:
        for y in x:
            print(y[0].decode('utf-8'),end =' ')
        print("\n\n")'''

    getCount(sentences)[1]
