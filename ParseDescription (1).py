from NP_Extraction import *
import os

description_path = 'data/descriptions_train'

obj_file = open('data/obj_in_descriptions.txt', 'wb+')

objs = Set()

for filename in os.listdir(description_path):
    print(filename)
    if filename.endswith('.txt'):
        oneFile = open(os.path.join(description_path, filename), 'r+')
        for sent in oneFile:
            nps = find_nps(sent[:-1]) if sent.endswith('\n') else find_nps(sent)
            for np in nps:
                objs.add(np)
        oneFile.close()

for obj in objs:
    obj_file.write(obj + ',')

obj_file.close()
