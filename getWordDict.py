from nltk.stem import WordNetLemmatizer
from sets import Set
import os
import re

allDescriptionsFiles = [os.path.join('data/descriptions_train', filename) for filename in
                        os.listdir('data/descriptions_train') if filename.endswith('.txt')]
allTagFiles = [os.path.join('data/tags_train', filename) for filename in os.listdir('data/tags_train') if
               filename.endswith('.txt')]

allDescriptionsFiles.sort(key=lambda x: int(x[x.rindex('/') + 1:-4]))
allTagFiles.sort(key=lambda x: int(x[x.rindex('/') + 1:-4]))
de_nonletter = re.compile('[^a-zA-Z]')

WordDict = {}
wl = WordNetLemmatizer()

def getWordDictFromDescriptions():
    for file in allDescriptionsFiles:
        wordLines = [line.split(' ') for line in open(file, 'r+')]
        for words in wordLines:
            for word in words:
                validWord = wl.lemmatize(de_nonletter.sub('', word.lower()))
                if len(validWord) > 2:
                    if WordDict.has_key(validWord):
                        WordDict[validWord] += 1
                    else:
                        WordDict[validWord] = 1
    for file in allTagFiles:
        wordLines = [line for line in open(file, 'r+')]
        for line in wordLines:
            validTag = de_nonletter.sub('', line.split(':')[1])
            WordDict[validTag] = 3


getWordDictFromDescriptions()

dictFile = open('data/BoW_dict.txt', 'wb+')
for key in WordDict.keys():
    if WordDict[key] > 2:
        dictFile.write(key + '\n')
