from nltk.stem import WordNetLemmatizer
from sets import Set
import os
import re

descriptionPath = 'data/descriptions_test'
tagPath = 'data/tags_test'
BoW_save_path = 'data/BoW_test_noun_adj_verb_HF.txt'
dict_file_path = 'data/noun_adj_verb_HF.txt'

allDescriptionFiles = [os.path.join(descriptionPath, filename) for filename in
                       os.listdir(descriptionPath) if filename.endswith('.txt')]
allDescriptionFiles.sort(key=lambda x: int(x[x.rindex('/') + 1:-4]))

allTagFiles = [os.path.join(tagPath, filename) for filename in os.listdir(tagPath) if
               filename.endswith('.txt')]
allTagFiles.sort(key=lambda x: int(x[x.rindex('/') + 1:-4]))

BoW_vec_file = open(BoW_save_path, 'wb+')
de_nonletter = re.compile('[^a-zA-Z]')

WordDict = [line[:-1] for line in open(dict_file_path, 'r+')]
WordDictSet = set(WordDict)
wl = WordNetLemmatizer()

for i in range(len(allDescriptionFiles)):
    print(allDescriptionFiles[i])
    descriptionFile = open(allDescriptionFiles[i], 'r+')
    tagFile = open(allTagFiles[i], 'r+')
    BoW_vec = [0 for i in range(len(WordDict))]
    for line in descriptionFile:
        words = line.split(' ')
        for word in words:
            validWord = wl.lemmatize(de_nonletter.sub('', word.lower()))
            if WordDictSet.__contains__(validWord):
                BoW_vec[WordDict.index(validWord)] += 1
    for line in tagFile:
        tag = line.split(':')[1]
        validTag = de_nonletter.sub('', tag)
        BoW_vec[WordDict.index(validTag)] += 1
    outputStr = ",".join([str(i) for i in BoW_vec])
    BoW_vec_file.write(outputStr + '\n')
