from sets import Set
import os
import re
from NP_Extraction import *

descriptionPath = 'data/descriptions_train'
tagPath = 'data/tags_train'
dictFilePath = 'data/noun_adj_verb_HF.txt'
threshold = 15
word_type_list = ['NN', 'NNS', 'JJ', 'VB', 'VBD', 'VBP', 'VBZ']

allDescriptionsFiles = [os.path.join(descriptionPath, filename) for filename in os.listdir(descriptionPath) if
                        filename.endswith('.txt')]
allTagFiles = [os.path.join(tagPath, filename) for filename in os.listdir(tagPath) if
               filename.endswith('.txt')]

allDescriptionsFiles.sort(key=lambda x: int(x[x.rindex('/') + 1:-4]))
allTagFiles.sort(key=lambda x: int(x[x.rindex('/') + 1:-4]))
deleteNonletter = re.compile('[^a-zA-Z]')


def getWordDict():
    WordDict = {}
    for file in allDescriptionsFiles:
        sentences = [line for line in open(file, 'r+')]
        for sent in sentences:
            noun_adj = findTypeWord(sent, word_type_list)
            for word in noun_adj:
                if WordDict.has_key(word):
                    WordDict[word] += 1
                else:
                    WordDict[word] = 1
    for file in allTagFiles:
        sentences = [line for line in open(file, 'r+')]
        for sent in sentences:
            validTag = deleteNonletter.sub('', sent.split(':')[1])
            WordDict[validTag] = 1000
    return WordDict


word_dict = getWordDict()

dictFile = open(dictFilePath, 'wb+')
for key in word_dict.keys():
    if word_dict[key] >= threshold:
        dictFile.write(key + '\n')
