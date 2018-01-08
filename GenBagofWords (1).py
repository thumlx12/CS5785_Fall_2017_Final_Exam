import numpy as np
import os
from sets import Set
from NP_Extraction import *
import threading


def calBOWVector(fileNames, descriptors, targetFile):
    for fileName in fileNames:
        print(fileName)
        npSet = Set()
        for sent in open(fileName, 'r+'):
            NPs = find_nps(sent[:-1]) if sent.endswith('\n') else find_nps(sent)
            for NP in NPs:
                npSet.add(NP)
        BOW_vector = np.array([0 for i in range(len(descriptors))])
        for NP in npSet:
            oneNP_vec = np.array([cmpNP(de_word, NP) for de_word in descriptors])
            BOW_vector.__add__(oneNP_vec)

        BOW_string = fileName + ':'
        BOW_string = BOW_string.join((str(item) + ' ') for item in BOW_vector)
        targetFile.write(BOW_string + '\n')


BOW_vector_data = open('data/BOW_vectors.txt', 'wb+')

de_words = [line.split(',') for line in open('data/obj_in_descriptions.txt', 'r+')][0]

description_path = 'data/descriptions_train'
tag_path = 'data/tags_train'

allFiles = []
for filename in os.listdir(description_path):
    if filename.endswith('.txt'):
        allFiles.append(os.path.join(description_path, filename))

threads = []
for i in range(8):
    start = i * 1250
    end = (i + 1) * 1250
    t = threading.Thread(target=calBOWVector, args=(allFiles[start:end], de_words, BOW_vector_data))
    threads.append(t)
    t.start()

# BOW_vector_data.close()
