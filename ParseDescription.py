from NP_Extraction import *
import os

description_path = 'data/descriptions_train'

obj_file = open('data/NounDict.txt', 'wb+')

objs = Set()

for filename in os.listdir(description_path):
    print(filename)
    if filename.endswith('.txt'):
        oneFile = open(os.path.join(description_path, filename), 'r+')
        for sent in oneFile:
            sent = sent[:-1] if sent.endswith('\n') else sent
            nps = findNoun(sent)
            for np in nps:
                objs.add(np)
        oneFile.close()

for obj in objs:
    obj_file.write(obj + '\n')

obj_file.close()
