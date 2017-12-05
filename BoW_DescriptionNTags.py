from nltk.stem import WordNetLemmatizer
from sets import Set
import os
import re

allDescriptionsFiles = [os.path.join('data/descriptions_test', filename) for filename in
                        os.listdir('data/descriptions_test') if filename.endswith('.txt')]
allTagFiles = [os.path.join('data/tags_test', filename) for filename in os.listdir('data/tags_test') if
               filename.endswith('.txt')]

BoW_vec_file = open('data/BoW_test_v2.txt', 'wb+')

allDescriptionsFiles.sort(key=lambda x: int(x[x.rindex('/') + 1:-4]))
allTagFiles.sort(key=lambda x: int(x[x.rindex('/') + 1:-4]))
de_nonletter = re.compile('[^a-zA-Z]')

WordDict = [line[:-1] for line in open('data/BoW_dict.txt', 'r+')]
WordDictSet = set(WordDict)
wl = WordNetLemmatizer()

for i in range(len(allDescriptionsFiles)):
    print(allDescriptionsFiles[i])
    descriptionFile = open(allDescriptionsFiles[i], 'r+')
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

# def getWordDictFromDescriptions():
#     for file in allDescriptionsFiles:
#         wordLines = [line.split(' ') for line in open(file, 'r+')]
#         for words in wordLines:
#             for word in words:
#                 validWord = wl.lemmatize(de_nonletter.sub('', word.lower()))
#                 if len(validWord) > 2:
#                     if WordDict.has_key(validWord):
#                         WordDict[validWord] += 1
#                     else:
#                         WordDict[validWord] = 1
#     for file in allTagFiles:
#         wordLines = [line for line in open(file, 'r+')]
#         for line in wordLines:
#             validTag = de_nonletter.sub('', line.split(':')[1])
#             WordDict[validTag] = 3
#
#
# getWordDictFromDescriptions()
#
# dictFile = open('data/BoW_dict.txt', 'wb+')
# for key in WordDict.keys():
#     if WordDict[key] > 2:
#         dictFile.write(key + '\n')
