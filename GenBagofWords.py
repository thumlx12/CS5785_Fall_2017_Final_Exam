import numpy as np
import os
from sets import Set
from NP_Extraction import *
import threading
import sys


def cmpWord(s, t):
    return (1 if s == t else 0)


def calBOWVector(prefix, fileNames, descriptors, targetPath):
    targetFile = open(targetPath, 'wb+')
    for i in range(len(fileNames)):
        print(fileNames[i])
        npSet = Set()
        for sent in open(os.path.join(prefix, fileNames[i]), 'r+'):
            sent = sent[:-1] if sent.endswith('\n') else sent
            NPs = findNoun(sent)
            for NP in NPs:
                npSet.add(NP)

        BOW_vector = sum(np.array([cmpWord(de_word, NP) for de_word in descriptors]) for NP in npSet)

        BOW_string = ''.join((str(item) + ',') for item in BOW_vector)
        targetFile.write(BOW_string[:-1] + '\n')
    targetFile.close()


# BOW_vector_path = str(sys.argv[1])
# description_path = str(sys.argv[2])
# descriptive_words = str(sys.argv[3])

BOW_vector_path = 'data/BoW_test.txt'
description_path = 'data/descriptions_test/'
descriptive_words = 'data/NounDict.txt'

allFiles = [filename for filename in os.listdir(description_path) if filename.endswith('.txt')]
allFiles.sort(key=lambda x: int(x[:-4]))

de_words = [line[:-1] for line in open(descriptive_words, 'r+') if line != '\n']

calBOWVector(description_path, allFiles, de_words, BOW_vector_path)

# threads = []
# threadNum = 4
# eachPartSize = len(allFiles) / threadNum
# for i in range(threadNum):
#     start = i * eachPartSize
#     end = (i + 1) * eachPartSize
#     curPath = BOW_vector_path
#     if curPath.endswith('/'):
#         curPath += 'part_' + str(i)
#     else:
#         curPath += '/part_' + str(i)
#
#     t = threading.Thread(target=calBOWVector,
#                          args=(description_path,
#                                allFiles[start:end],
#                                de_words,
#                                curPath))
#     threads.append(t)
#     t.start()
#
# for t in threads:
#     t.join()
